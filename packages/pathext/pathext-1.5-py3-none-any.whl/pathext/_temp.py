__all__ = [
    'temporary_directory',
]

import contextlib
import sys
import tempfile
from collections.abc import Generator
from pathlib import Path
from typing import Optional, TypedDict

if sys.version_info >= (3, 12):
    class DeleteKeyword(TypedDict, total=False):
        delete: bool
else:
    class DeleteKeyword(TypedDict, total=False):
        pass

@contextlib.contextmanager
def temporary_directory(
    suffix: Optional[str] = None,
    prefix: Optional[str] = None,
    dir: Optional[Path] = None,
    ignore_cleanup_errors: bool = False,
    delete: Optional[bool] = None,
) -> Generator[Path]:
    """
    Context manager similar to `tempfile.TemporaryDirectory` except it returns the created directory's name as an absolute `pathlib.Path` instead of `str`.

    Supports all arguments of `tempfile.TemporaryDirectory`, including `delete` introduced in Python 3.12. If `delete` is specified on Python 3.11 or older, ValueError is raised.

    Note that the returned path is always absolute, even if the `dir` parameter is relative. This is consistent with how `tempfile.TemporaryDirectory` works starting with Python 3.12.
    """

    delete_kwargs: DeleteKeyword = dict()
    if delete is not None:
        if sys.version_info >= (3, 12):
            delete_kwargs['delete'] = delete
        else:
            raise ValueError('tempfile.TemporaryDirectory() only supports the "delete" argument from Python 3.12')

    with tempfile.TemporaryDirectory(suffix, prefix, dir, ignore_cleanup_errors, **delete_kwargs) as tmp_dir:
        yield Path(tmp_dir).absolute()
