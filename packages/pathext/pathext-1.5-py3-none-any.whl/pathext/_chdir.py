import contextlib
import os
from collections.abc import Generator
from pathlib import Path
from typing import Optional

@contextlib.contextmanager
def chdir_context(path: Optional[Path]) -> Generator[None]:
    """
    Non parallel-safe context manager to change the current working directory. If `path` is `None`, it does nothing. If `path` is not None, it changes the current working directory upon entering and restores the old one on exit.

    Unlike `contextlib.chdir()`, this context manager is NOT reentrant or reusable.

    See `contextlib.chdir()`'s documentation on notes about threaded and async contexts.
    """

    if path is None:
        yield None
    else:
        try:
            old_cwd = Path.cwd()
            os.chdir(path)
            yield None
        finally:
            os.chdir(old_cwd)
