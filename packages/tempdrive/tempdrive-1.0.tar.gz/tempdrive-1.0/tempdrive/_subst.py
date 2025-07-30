__all__ = [
    'subst',
    'unsubst',
]

import ctypes
from pathlib import Path
from typing import Optional

from ntstatus import Win32Error

from tempdrive._drive_letter import DriveLetter
from tempdrive._exceptions import TempDriveError
from tempdrive._free_drive import get_used_drive_letters
from tempdrive._winapi import DefineDosDeviceW, QueryDosDeviceW

DDD_REMOVE_DEFINITION = 2

def subst(drive: DriveLetter, path: Path) -> None:
    """
    Creates new drive substitution, similarly to [subst.exe](https://ss64.com/nt/subst.html).

    For example, `tempdrive.subst(tempdrive.DriveLetter("w:"), Path(r'c:\Windows'))` creates a virtual W: drive that acts as an alias to the Windows folder.

    Substituted drives can be useful if an application starts hitting the 260-character path length limit.

    Arguments:
    - `drive: tempdrive.DriveLetter`: Drive letter to use for newly created drive substitution.
    - `path: pathlib.Path`: Path the newly created drive substitution should point to.

    Raises `tempdrive.TempDriveError` if drive is already in use. Raises `OSError` if it runs into an error while calling WinAPI functions.
    """

    if drive in get_used_drive_letters():
        raise TempDriveError(f'Drive letter is already in use: {drive.device}')

    success = DefineDosDeviceW(0, drive.device, str(path.absolute()))
    if not success:
        raise ctypes.WinError(ctypes.GetLastError())

def query_device(drive: DriveLetter) -> str:
    bufsize = 260
    while True:
        buffer = ctypes.create_unicode_buffer(bufsize)
        ret = QueryDosDeviceW(drive.device, buffer, bufsize)
        if ret != 0:
            # success -> return buffer contents
            return ctypes.wstring_at(buffer)

        last_error = ctypes.GetLastError()
        if last_error == Win32Error.ERROR_INSUFFICIENT_BUFFER:
            # buffer was too small, retry with larger buffer
            bufsize *= 2
        else:
            raise ctypes.WinError(last_error)

def unsubst(drive: DriveLetter) -> None:
    """
    Removes a drive substitution created by `tempdrive.subst()`.

    Arguments:
    - `drive: tempdrive.DriveLetter`: Drive letter of substitution to remove.

    Raises `tempdrive.TempDriveError` if the drive does not exist, or is not a substitution. Raises `OSError` if it runs into an error while calling WinAPI functions.
    """

    if drive not in get_used_drive_letters():
        raise TempDriveError(f'Drive does not exist: {drive.device}')

    if not query_device(drive).startswith('\\??\\'):
        raise TempDriveError(f'Drive is not DOS drive substitution: {drive.device}')

    success = DefineDosDeviceW(DDD_REMOVE_DEFINITION, drive.device, None)
    if not success:
        raise ctypes.WinError(ctypes.GetLastError())
