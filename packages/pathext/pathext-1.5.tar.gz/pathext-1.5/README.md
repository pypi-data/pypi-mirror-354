# pathext

`pathext` is a collection of functions working with `pathlib.Path`. They're often wrappers for standard library functionality with some extensions.

## Executable lookup

### `pathext.which()`

Wrapper for `shutil.which()` which returns the result as an absolute `Path` (or `None` if it fails to find the executable). It also has a couple extra features, see below.

Arguments (all of them except `name` are optional):
- `name: str` - Executable name to look up.
- `path: None | str | Sequence[Path]` - Directory list to look up `name` in. If set to `None`, or set to a string, then it is passed to `shutil.which()` as-is. If set to a list, concatenates the list items using `os.pathsep`, and passes the result to `shutil.which()`. Defaults to `None`. See `shutil.which()`'s documentation on exact behaviour of this argument.
- `cwd: Optional[Path]` - If specified, then changes the current working directory to `cwd` for the duration of the `shutil.which()` call. Note that since it is changing global state (the current working directory), it is inherently not thread-safe.

### `pathext.checked_which()`

Same as `pathext.which()`, except it raises `ValueError` instead of returning `None` if it cannot find the executable.

## Manipulating `PATH` strings

### `pathext.split_path_list()`

Split `PATH` string based on `os.pathsep` and convert each component to `pathlib.Path`.

Empty components will be removed, i.e. leading, trailing or duplicated separators will not cause issues.

In contrast to `str.split()`, if the string is empty, the function will return an empty list.

### `pathext.join_path_list()`

Create `PATH` string (`os.pathsep`-separated string) from list of paths. The list is allowed to contain `Path` objects, strings and even `None`. Empty strings and `None`s will be removed before joining the list.

### `pathext.deduplicate_path_list()`

Remove duplicates from path list, keeping only the first occurence. The list is allowed to contain `Path` objects, strings and even `None`. Empty strings and `None`s will be removed before deduplication, and the rest is converted to `Path`.

## Generic utilities

### `pathext.to_path()`

Simple function that converts a `str` to a `Path` (just like `Path`'s constructor), but also handles `None` by returning `None`. It can be used to convert the return value of functions that return `str | None` to `Path | None`.

### `pathext.temporary_directory()`

Context manager similar to `tempfile.TemporaryDirectory` except it returns the created directory's name as an absolute `pathlib.Path` instead of `str`.

Supports all arguments of `tempfile.TemporaryDirectory`, including `delete` introduced in Python 3.12. If `delete` is specified on Python 3.11 or older, ValueError is raised.

Note that the returned path is always absolute, even if the `dir` parameter is relative. This is consistent with how `tempfile.TemporaryDirectory` works starting with Python 3.12.

### `pathext.chdir_context()`

Non parallel-safe context manager to change the current working directory. If `path` is `None`, it does nothing. If `path` is not `None`, it changes the current working directory upon entering and restores the old one on exit.

Unlike `contextlib.chdir()`, this context manager is NOT reentrant or reusable.

See `contextlib.chdir()`'s documentation on notes about threaded and async contexts.
