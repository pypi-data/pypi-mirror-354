#!/usr/bin/env python3
"""Simple routine to find dirty tests.

# Limitations

- No monkey patching, e.g. `sys.modules`.
- No dynamic importing, i.e. `__import__` or `importlib`.
- No path manipulations, i.e. `sys.path` or `__path__`.
- No crazy custom module loaders.
"""

import ast
import json
import logging
import os.path
import sys
from argparse import ArgumentParser, FileType, Namespace
from collections import OrderedDict, defaultdict
from contextlib import contextmanager
from dataclasses import astuple, dataclass, field
from importlib.machinery import EXTENSION_SUFFIXES, SOURCE_SUFFIXES
from os import getenv
from pathlib import Path
from typing import IO, Any, Iterable, Iterator, Literal, Self, cast

if sys.version_info < (3, 11):
    import tomli as toml
else:
    import tomllib as toml

SourceKind = Literal['source', 'ext', 'stub']

ALL_SUFFIXES: list[tuple[str, SourceKind]] = \
    [(s, 'source') for s in SOURCE_SUFFIXES] + \
    [(s, 'ext') for s in EXTENSION_SUFFIXES] + \
    [('.pyi', 'stub')]

LOG_LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warn': logging.WARNING,
    'error': logging.ERROR,
}

parser = ArgumentParser(description=__doc__)
parser.add_argument(
    '-c', '--config', type=Path, help='path to pyproject.toml')
parser.add_argument(
    '-p', '--package', action='append', type=str,
    help='known modules and packages to ignore')
parser.add_argument(
    '-s', '--source', action='append', type=Path,
    help='source code specification')
parser.add_argument(
    '-t', '--target', action='append', type=Path,
    help='target files or directories')
parser.add_argument(
    'changed', help='path to list of changed files (or stdin)')
parser.add_argument(
    'affected', nargs='?', help='path to list of affected files (or stdout)')

# Describe `diagnostics` group.
g_diag = parser.add_argument_group('diagnostics options')
g_diag_ex = g_diag.add_mutually_exclusive_group()
g_diag_ex.add_argument(
    '-d', '--dump-dirty', default=False, action='store_true',
    help='dump all dirty files with reason')
g_diag_ex.add_argument(
    '-g', '--dump-graph', default=False, action='store_true',
    help='dump dependency graph')
g_diag_ex.add_argument(
    '-u', '--dump-unresolved', default=False, action='store_true',
    help='dump modules with unresolved imports')

# Describe `logging` group.
g_log = parser.add_argument_group('logging options')
g_log.add_argument(
    '--log-level', default='error', choices=sorted(LOG_LEVELS.keys()),
    help='set logger verbosity level')
g_log.add_argument(
    '--log-output', default=sys.stderr, metavar='FILENAME', type=FileType('w'),
    help='set output file or stderr (-) for logging')


@dataclass
class Import:
    """Representate an imported symbol (attribute, function or module)."""

    fqmn: str

    level: int = 0

    def __hash__(self) -> int:
        return hash(astuple(self))

    @property
    def is_absolute(self) -> bool:
        return self.level == 0

    @property
    def is_relative(self) -> bool:
        return self.level > 0

    @property
    def parent(self) -> str:
        if len(parts := self.fqmn.rsplit('.', 1)) == 2:
            return parts[0]
        else:
            return ''

    @classmethod
    def from_fqmn(cls, name: str) -> Self:
        return cls(name, 0)

    @classmethod
    def from_relative_import(cls, relative_module: str | None, name: str,
                             level: int) -> Self:
        if relative_module:
            fqmn = f'{relative_module}.{name}'
        else:
            fqmn = name
        return cls(fqmn, level)


class ImportVisitor(ast.NodeVisitor):
    """A visitor over Python import statements.

    https://docs.python.org/3/reference/simple_stmts.html#the-import-statement
    """

    def __init__(self) -> None:
        super().__init__()
        self.imports: set[Import] = set()

    def visit_Import(self, node: ast.Import):
        self.imports |= {Import.from_fqmn(alias.name) for alias in node.names}

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.level == 0:
            module_name = cast(str, node.module)  # Since absolute import.
            self.imports.add(Import.from_fqmn(module_name))
        for alias in node.names:
            import_ = Import.from_relative_import(node.module, alias.name,
                                                  node.level)
            self.imports.add(import_)


@dataclass
class Module:

    name: str

    path: Path

    kind: SourceKind = 'source'

    imports: list[Import] = field(default_factory=list)


def get_module_name(path: Path) -> Module | None:
    for suffix, kind in ALL_SUFFIXES:
        if path.name.endswith(suffix):
            return Module(path.with_suffix('').name, path, kind)


class ModuleIndex(dict[Path, Module]):
    """Index of all seen modules."""

    def find_module(self, path: Path) -> Module | None:
        if (mod := self.get(path)) is not None:
            return mod
        if (mod := get_module_name(path)) is not None:
            self[path] = mod
            return mod

    @classmethod
    def from_paths(cls, *paths: Path) -> Self:
        if len(paths) == 0:
            return cls()

        modules: dict[Path, Module] = {}
        for path in paths:
            entries: Iterable[Path]
            if path.is_file():
                entries = [path]
            else:
                entries = path.rglob('*')
            for ent in entries:
                if not ent.is_file():
                    continue
                if (name := get_module_name(ent)) is not None:
                    modules[ent] = name
        return cls(modules)


class ModuleResolver(dict[str, Module]):
    """
    1. Build package structure.
    2. Find a module by fqmn.
    """

    def __init__(self, modules: dict[Path, Module], path: Path,
                 cache: dict[str, Module] = {}):
        super().__init__(cache or {})
        self.modules = modules
        self.path = path

    def resolve(self, import_: Import, path: Path | None = None):
        """Resolve symbol to module by its fully-qualified name."""
        # Resolve module as an absolute or relative symbol.
        if import_.is_absolute:
            result = self.resolve_absolute(import_)
        elif path is None:
            raise RuntimeError(
                f'Relative import statement `{import_.fqmn}` can not be '
                'resolved without path specification.')
        else:
            result = self.resolve_relative(import_, path)

        # Add resolved module to the cache.
        if result is not None:
            module, name = result
            if name not in self:
                self[name] = module

        return result

    def resolve_absolute(self, import_: Import):
        """Resolve symbol to module by its fully-qualified name."""
        # Firstly, try to find a name in cache of resolved modules.
        if (mod := self.get(import_.fqmn)) is not None:
            return mod, import_.fqmn

        *modules, last = import_.fqmn.split('.')

        # If there is not dot in module name, then its a package or a module.
        if not modules:
            for suffix, kind in ALL_SUFFIXES:
                key = self.path / f'{last}{suffix}'
                if key in self.modules:
                    return self.modules[key], last

            key = self.path / last / '__init__.py'
            if key in self.modules:
                return self.modules[key], f'{last}.__init__'

            # Otherwise, it is not an importable name.
            return None

        for i, _ in enumerate(modules):
            prefix = '/'.join(modules[:i + 1])

            # Secondly, if there is a single dot or no dots at all, then import
            # statement refers a python module (or extension).
            for suffix, kind in ALL_SUFFIXES:
                key = self.path / f'{prefix}{suffix}'
                if key not in self.modules:
                    continue

                # If we find a native extension, then import is resolved.
                if kind == 'ext':
                    module_name = '.'.join(modules[:i + 1])
                    return self.modules[key], module_name

                # If we find a stub file or source file, the current prefix
                # must be longest prefix (i.e. prefix.split('.') == modules).
                if i + 1 == len(modules):
                    module_name = '.'.join(modules)
                    return self.modules[key], module_name

                # Otherwise, we should throw ImportError.
                return

            # Thirdly, there might be a `prefix` directory with `__init__`
            # module inside.
            if (key := self.path / prefix / '__init__.py') not in self.modules:
                return

        prefix = '/'.join(modules)

        # Last segment might be a module (source or native extension).
        for suffix, kind in ALL_SUFFIXES:
            if (key := self.path / prefix / f'{last}{suffix}') in self.modules:
                return self.modules[key], import_.fqmn

        # Last segment might be a subpackage.
        if (key := self.path / prefix / last / '__init__.py') in self.modules:
            return self.modules[key], f'{import_.fqmn}.__init__'

        # Then take the parent subpackage.
        if (key := self.path / prefix / '__init__.py') in self.modules:
            package_name = '.'.join(modules)
            module_name = f'{package_name}.__init__'
            return self.modules[key], module_name

    def resolve_relative(self, import_: Import, path: Path):
        """Resolve symbol to module by its qualified relative name."""
        # Relative symbols are resolved with respect a search path which is a
        # prefix for an importing module (module that imports).
        if not path.is_relative_to(self.path):  # TODO(@daskol): Abs.
            return None

        if path.is_file():
            path = path.parent
        parents = path.relative_to(self.path).parts

        # TODO(@daskol): Raise an exeception? Broken import.
        if import_.level > len(parents):
            return None
        depth = len(parents) - import_.level + 1
        parent_package = '.'.join(parents[:depth])
        symbol_name = f'{parent_package}.{import_.fqmn}'

        # Finally, we have symbol name ...x.y.z. There are two cases: (a)
        # either ...x.y.z is a module (b) or ...x.y is module. Note, there is
        # at least one dot (.) since <relative-spec>.<symbol>.
        names = (symbol_name, symbol_name.rsplit('.', 1)[0])
        for name in names:
            if (result := self.resolve_absolute(Import(name))) is not None:
                return result

    @classmethod
    def from_packages(cls, modules: ModuleIndex, path: Path,
                      *packages: str) -> Self:
        cache = {}
        for package in OrderedDict.fromkeys(packages):
            for entry in (path / package).rglob('*'):
                if (mod := modules.find_module(entry)) is None:
                    continue
                parts = entry.relative_to(path).with_name(mod.name).parts
                name = '.'.join(parts)
                cache[name] = mod
        return cls(modules, path, cache)


def get_module_imports(mod: Module) -> set[Import]:
    """Parse module source and retrieve a set of imported symbols."""
    if mod.kind != 'source':
        return set()
    with open(mod.path) as fin:
        content = fin.read()
    tree = ast.parse(content, mod.path)
    visitor = ImportVisitor()
    visitor.visit(tree)
    return visitor.imports


def resolve_import(resolvers: dict[Path, ModuleResolver], import_: Import,
                   path: Path) -> tuple[Module, str] | None:
    for _, resolver in resolvers.items():
        if (result := resolver.resolve(import_, path)) is not None:
            return result


def resolve_parents(resolvers: dict[Path, ModuleResolver], module: Module,
                    name: str) -> list[tuple[Module, str]]:
    # Find package root directory first.
    modules = name.split('.')
    depth = len(modules) - 1
    path = module.path.parents[depth]
    resolver = resolvers[path]

    # Module name might end with module __init__. In this case we can exclude
    # it to save compute.
    if modules[-1] == '__init__':
        modules = modules[:-1]

    # Iterate over all superpackages and append module __init__.
    supers: list[tuple[Module, str]] = []
    for i, _ in enumerate(modules):
        super_name = '.'.join(modules[:i + 1])
        super_ = resolver.resolve(Import(super_name))
        if super_:
            supers.append(super_)
        else:
            logging.warning('failed to resolve parent package %s', super_name)
    return supers


def traverse_imports(module_ix: ModuleIndex, module: Module,
                     paths: list[Path]):
    """Recursively traverse dependencies of a module."""
    paths.insert(0, module.path.parent)

    # TODO(@daskol): Combine module index and resolvers into a single object.
    resolvers: dict[Path, ModuleResolver] = {}
    for path in paths:
        resolvers[path] = ModuleResolver(module_ix, path)

    # Mapping fomr fully-qualified module names to a `Module`.
    modules: dict[str, Module] = {}
    modules[module.name] = module

    # Collection of unresolved modules.
    unresolved: dict[Path, set[str]] = defaultdict(set)

    # Resolve module imports in Breadth-First Search (BFS) manner.
    queue: list[Module] = [module]
    while queue:
        head, queue = queue[0], queue[1:]
        imports = sorted(head.imports, key=lambda x: x.fqmn)
        for import_ in imports:
            result = resolve_import(resolvers, import_, head.path)
            if result is None:
                kind = 'absolute'
                if import_.is_relative:
                    kind = 'relative'
                logging.info('failed to resolve %s symbol %s from %s', kind,
                             import_.fqmn, head.path)
                unresolved[head.path].add(import_.fqmn)
                continue

            # TODO(@daskol): Collisions?
            mod, name = result
            if name not in modules:
                queue.append(mod)
                modules[name] = mod

            # Add all parent __init__ modules to queue.
            parents = resolve_parents(resolvers, mod, name)
            for parent_mod, parent_name in parents:
                if parent_name not in modules:
                    queue.append(parent_mod)
                    modules[parent_name] = parent_mod

    if unresolved:
        logging.info('module %s (%s) has %s unresolved symbols', module.name,
                     module.path, len(unresolved))

    return modules, unresolved


def reverse_edges(graph: dict[Path, set[Path]]) -> dict[Path, set[Path]]:
    result = defaultdict(set)
    for source, targets in graph.items():
        for target in targets:
            result[target].add(source)
    return {k: set(sorted(v)) for k, v in result.items()}


def dump_graph(path2target: dict, where):
    def json_dump_fn(obj):
        if isinstance(obj, Path):
            return str(obj)
        elif isinstance(obj, set):
            return list(obj)
        else:
            raise TypeError(f'No rule to serialize {type(obj)}.')

    def json_cast_keys(obj):
        if isinstance(obj, dict):
            return {str(k): json_cast_keys(v) for k, v in obj.items()}
        else:
            return obj

    obj = json_cast_keys(path2target)
    json.dump(obj, where, ensure_ascii=False, indent=2,
              default=json_dump_fn)


@contextmanager
def stdout_or_file(path_or_none: Path | str | None = None) -> Iterator[IO[str]]:
    if path_or_none:
        with open(path_or_none, 'w') as fout:
            yield fout
    else:
        yield sys.stdout


def load_config(ns: Namespace) -> tuple[dict[str, Any], Path]:
    config: dict[str, Any] = {}
    config_path = Path('pyproject.toml')
    if ns.config is None:
        if config_path.exists():
            with open('pyproject.toml', 'rb') as fin:
                config = toml.load(fin)
    else:
        config_path = Path(ns.config)
        if not config_path.exists():
            print(f'failed to load config from {config_path}')
            sys.exit(1)
        with open(config_path, 'rb') as fin:
            config = toml.load(fin)
    # Get content of [tool.pytest-dirty].
    config = config.get('tool', {}).get('pytest-dirty', {})
    return config, config_path


def main() -> None:
    ns: Namespace = parser.parse_args()

    config, config_path = load_config(ns)
    config_dir = config_path.parent

    if (packages := config.get('packages', [])):
        ns.package = packages + (ns.package or [])

    if (sources := config.get('sources', [])):
        sources = [config_dir / Path(s) for s in sources]
        ns.source = sources + (ns.source or [])

    if (targets := config.get('targets', [])):
        targets = [config_dir / Path(t) for t in targets]
        ns.target = targets + (ns.target or [])

    # Path are not in the common root.
    config_dir = config_dir.absolute()
    manual_deps: dict[Path, set[Path]] = defaultdict(set)
    for target_glob, sources in config.get('dependency', {}).items():
        if not sources:
            continue
        source_set = {config_dir / Path(s) for s in sources}
        for target in config_dir.glob(target_glob):
            manual_deps[target] |= source_set

    # Set up basic logging configuration.
    if (stream := ns.log_output) is None:
        stream = sys.stderr
    logging.basicConfig(format='%(module)s %(levelname)s %(message)s',
                        level=LOG_LEVELS[ns.log_level], stream=stream)

    source_paths: list[Path] = []
    for el in (ns.source or []):
        source_path = Path(el)
        source_paths.append(source_path)

    target_paths: list[Path] = []
    for el in (ns.target or []):
        target_path = Path(el)
        target_paths.append(target_path)

    # TODO(@daskol): Replace list with ordered set for better performance.
    paths: list[Path] = []
    if (value := getenv('PYTHONPATH')) is not None:
        parts = filter(None, value.split(':'))
        paths += [Path(p) for p in parts]
    paths += source_paths
    paths += target_paths

    # Filter and canonicalize paths.
    absolute_paths: list[Path] = []
    for path in paths:
        if not path.exists():
            logging.warn('path %s does not exist', path)
        absolute_paths.append(path.absolute())
    common_path: Path = Path.cwd()
    if absolute_paths:
        common_path = Path(os.path.commonpath([common_path] + absolute_paths))
    canonical_paths: list[Path] = [
        p.relative_to(common_path) for p in absolute_paths
    ]

    # TODO(@daskol): Read from stdin and guess single python source or
    # directory.
    input_paths: list[Path] = []
    if ns.changed == '-':
        input_paths += [Path(x.strip()) for x in sys.stdin]
    elif (input_path := Path(ns.changed)).suffix == '.py':
        input_paths.append(input_path)
    else:
        with open(ns.changed) as fin:
            input_paths += [Path(x.strip()) for x in fin]
    logging.info('assume changed files are %s', input_paths)

    logging.info('list all python modules recursively')
    module_ix = ModuleIndex.from_paths(*canonical_paths)
    logging.info('  %d modules found', len(module_ix))

    logging.info('load sources and parse import statements')
    module_blacklist = set(p.split('.', 1)[0] for p in ns.package if p)

    def filter_imports(import_: Import) -> bool:
        if import_.is_relative:
            return True
        topmost, *_ = import_.fqmn.split('.', 1)
        if topmost in sys.stdlib_module_names or topmost in module_blacklist:
            return False
        return True

    for mod in module_ix.values():
        imports = get_module_imports(mod)
        # Filter out system packages and installed packages before dependency
        # traversing.
        #
        # TODO(@daskol): This approach is unreliable since someone can shadow
        # system or installed packages but, for now, we assume that user does
        # not do this.
        mod.imports = [*filter(filter_imports, imports)]

    # Initialize dirty files.
    dirty: dict[Path, list[str]] = defaultdict(list)
    for input_path in input_paths:
        dirty[input_path].append('changed')
    unresolved_names: dict[Path, set[str]] = defaultdict(set)

    # Iterate over target files and directories in order to traverse module
    # dependencies.
    target2path: dict[Path, set[Path]] = defaultdict(set)
    for target_path in target_paths:
        target_entries: Iterable[Path]
        if target_path.is_file():
            target_entries = [target_path.absolute()]
        else:
            target_entries = target_path.rglob('*.py')

        for path in target_entries:
            path = path.absolute()
            if not path.is_relative_to(common_path):
                continue
            path = path.relative_to(common_path)

            module = module_ix[path]
            modules, unresolved = traverse_imports(
                module_ix, module, [source_path.parent])

            target_deps = {k: v.path for k, v in modules.items()}
            target2path[path] |= set(target_deps.values())

            if unresolved:
                logging.info('add module %s (%s) to a set of dirty files',
                             mod.name, mod.path)
                dirty[path] += ['unresolved']
                logging.info('unresolved symbols of %s (%s) are %s', mod.name,
                             mod.path, [*unresolved.keys()])
                for key, val in unresolved.items():
                    unresolved_names[key] |= val

    # Add manually specified dependencies to targets.
    for target, sources in manual_deps.items():
        if not target.is_relative_to(common_path):
            continue
        sources = {
            s.relative_to(common_path)
            for s in sources
            if s.is_relative_to(common_path)
        }
        target = target.relative_to(common_path)
        target2path[target] |= sources

    # Build mapping from target paths to path which the target depends on.
    path2target = reverse_edges(target2path)

    with stdout_or_file(ns.affected) as fout:
        if ns.dump_dirty:
            dump_graph(dirty, fout)
            return
        if ns.dump_graph:
            dump_graph(path2target, fout)
            return
        if ns.dump_unresolved:
            dump_graph(unresolved_names, fout)
            return

        dirty_targets: set[Path] = set()
        for dirty_path in dirty:
            # What if dirty_path is out of scope? We just ignore it.
            dirty_path = dirty_path.absolute().relative_to(common_path)
            if dirty_path not in module_ix:
                logging.warning('path %s is out of scope', dirty_path)
                continue
            # Dirty path does not affect target files (modules).
            if dirty_path not in path2target:
                continue
            dirty_targets |= path2target[dirty_path]
        for dirty_target in sorted(dirty_targets):
            print(dirty_target, file=fout)

    num_dirties = len(dirty_targets)
    num_total = len(target2path)
    print(f'{num_dirties} dirty targets of {num_total} total targets',
          file=sys.stderr)


if __name__ == '__main__':
    main()
