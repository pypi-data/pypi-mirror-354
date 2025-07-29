from pathlib import Path

from dirty import ModuleIndex, ModuleResolver

data_dir = Path(__file__).parent / 'testdata'


class ModuleResolverTest:

    def test_from_packages(self):
        modules = ModuleIndex()
        cache = ModuleResolver.from_packages(modules, data_dir, 'pkg1')
        assert len(cache) == 4
