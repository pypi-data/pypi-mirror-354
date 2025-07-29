__all__ = [
    'to_path',
]

from pathlib import Path
from typing import Optional

def to_path(s: Optional[str]) -> Optional[Path]:
    """
    Simple function that converts a `str` to a `Path` (just like `Path`'s constructor), but also handles `None` by returning `None`. It can be used to convert the return value of functions that return `str | None` to `Path | None`.
    """

    if s is None:
        return None
    else:
        return Path(s)
