# pytest-dirty

*Static import analysis for thrifty testing.*

## Overview

With `pytest>=8.2` and `git`, one can easily find what Python files have been
changed and what test files to run.

```shell
# 1. List files changed in a pull request.
git diff --name-only main..<pr-branch> > changed.txt
# 2. Run `pytest-dirty` to know what chaned files of package `<package>` affect
tests in `tests` directory must be run.
pytest-dirty -s <package> -t tests changed.txt > affected.txt
# 3. Run tests with pytest.
pytest -s -vv @affected.txt
```
