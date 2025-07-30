__all__ = [
    'temporary_drive',
]

import contextlib
import ctypes
from collections.abc import Callable, Generator
from pathlib import Path
from typing import Optional

from tempdrive._exceptions import TempDriveError
from tempdrive._free_drive import get_free_drive_letters
from tempdrive._subst import subst, unsubst

@contextlib.contextmanager
def temporary_drive(path: Path, log: Optional[Callable[[str], None]] = None) -> Generator[Path]:
    """
    Context manager to create a new drive substitution (using `tempdrive.subst()`) for the specified path with an automatically chosen drive letter. Remove drive substitution on exit.

    When used in a `with` statement, the target of the `as` clause will be set to a `pathlib.Path` pointing to the newly created drive's root folder.

    This function can be useful if a script needs to work within a deeply nested folder, and it starts hitting the 260-character path length limit.

    Arguments:
    - `path: pathlib.Path`: Path the newly created drive substitution should point to.
    - `log: Callable[[str], None]`: Logging function to use for informational messages upon adding and removing the drive substitution. If unspecified or set to `None`, no messages are emitted.

    Raises `tempdrive.TempDriveError` if there is no available drive letter to use. Raises `OSError` if it runs into an error while calling WinAPI functions.
    """

    if log is None:
        log = lambda msg: None

    drives = get_free_drive_letters()
    if not drives:
        raise TempDriveError(f'Could not find a free drive letter to map {path} to')

    drive = drives[-1]

    log(f'Acquiring drive {drive} as alias to "{path}"...')
    subst(drive, path)
    try:
        yield drive.path
    finally:
        log(f'Releasing drive {drive}...')
        unsubst(drive)
