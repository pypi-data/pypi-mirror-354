__all__ = [
    'split_path_list',
    'join_path_list',
    'deduplicate_path_list',
]

import os
from pathlib import Path
from typing import Sequence

import more_itertools

def split_path_list(path_string: str) -> list[Path]:
    """
    Split `PATH` string based on `os.pathsep` and convert each component to `pathlib.Path`.

    Empty components will be removed, i.e. leading, trailing or duplicated separators will not cause issues.

    In contrast to `str.split()`, if the string is empty, the function will return an empty list.
    """

    if path_string=='':
        return []

    return [Path(d) for d in path_string.split(os.pathsep) if d]

def join_path_list(path_list: Sequence[Path | str | None]) -> str:
    """
    Create `PATH` string (`os.pathsep`-separated string) from list of paths. The list is allowed to contain `Path` objects, strings and even `None`. Empty strings and `None`s will be removed before joining the list.
    """

    return os.pathsep.join(str(d) for d in path_list if d)

def deduplicate_path_list(path_list: Sequence[Path | str | None]) -> list[Path]:
    """
    Remove duplicates from path list, keeping only the first occurence. The list is allowed to contain `Path` objects, strings and even `None`. Empty strings and `None`s will be removed before deduplication, and the rest is converted to `Path`.
    """

    # Note that it's important to keep the relative order of directories in the PATH list, we simply want to remove
    # duplicates after the first instance.
    return list(more_itertools.unique_everseen(Path(d) for d in path_list if d))
