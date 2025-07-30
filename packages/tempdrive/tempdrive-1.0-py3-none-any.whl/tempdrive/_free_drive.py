__all__ = [
    'get_free_drive_letters',
    'get_used_drive_letters',
]

import ctypes
import ctypes.wintypes as wintypes
import itertools
import string
from collections.abc import Generator
from typing import Optional

from ntstatus import Win32Error

from tempdrive._drive_letter import DriveLetter
from tempdrive._winapi import ByRef, GetLogicalDriveStringsW, NETRESOURCEW, WNetEnumResourceW, WNetOpenEnumW

def get_logical_drives() -> Generator[DriveLetter]:
    bufsize = 260
    while True:
        buffer = ctypes.create_unicode_buffer(bufsize)
        ret = GetLogicalDriveStringsW(bufsize, buffer)
        if ret==0:
            # an error happened
            raise ctypes.WinError(ctypes.GetLastError())
        elif ret > bufsize:
            # buffer was too small, retry with properly sized buffer
            bufsize = ret
        else:
            # data fit in buffer -> break loop and process it
            break

    p = ctypes.addressof(buffer)
    while drive := ctypes.wstring_at(p):
        yield DriveLetter(drive)
        p += (len(drive) + 1)*2

RESOURCE_REMEMBERED = 3
RESOURCETYPE_DISK = 1

def get_network_drives() -> Generator[DriveLetter]:
    henum = ctypes.wintypes.HANDLE()
    ret = WNetOpenEnumW(RESOURCE_REMEMBERED, RESOURCETYPE_DISK, 0, None, ByRef(henum))
    if ret != Win32Error.ERROR_SUCCESS:
        raise ctypes.WinError(ret)

    array_size = 1
    while True:
        buffer = (NETRESOURCEW*array_size)()
        bufsize = ctypes.wintypes.DWORD(ctypes.sizeof(buffer))

        count = ctypes.wintypes.DWORD(-1)
        # print(f'WNetEnumResourceW(count={count.value}, bufsize={bufsize.value})')
        ret = WNetEnumResourceW(henum, ByRef(count), buffer, ByRef(bufsize))
        # print(f'ret={ret}, count={count.value}, bufsize={bufsize.value}')

        if ret==Win32Error.ERROR_NO_MORE_ITEMS:
            # Iteration done, yay
            return

        if ret in [Win32Error.ERROR_SUCCESS, Win32Error.ERROR_MORE_DATA] and count.value==0:
            # This is not documented properly, but if bufsize is too low, then one of two things may happen:
            # - the function returns ERROR_MORE_DATA, sets bufsize to the minimum size to receive one resource, and sets count to 0 (this is sane)
            # - the function returns ERROR_SUCCESS (NO_ERROR), does not touch bufsize and sets count to 0 (this is undocumented and frankly, insane)
            # Since apparently bufsize is not to be trusted, we simply double our buffer, and try again
            array_size *= 2
            continue

        if ret != Win32Error.ERROR_SUCCESS:
            raise ctypes.WinError(ret)

        for i in range(count.value):
            name = buffer[i].lpLocalName
            # Not all lpLocalNames are necessarily valid drive names -> check before calling the constructor
            if DriveLetter.is_drive_string(name):
                yield DriveLetter(name)

def get_used_drive_letters() -> list[DriveLetter]:
    """
    Returns the list of `tempdrive.DriveLetter` objects that represent all disk drives currently present in the system. This includes:
    - Physical drives
    - Virtual/substituted disk drives
    - Connected network drives
    - Disconnected but registered network drives
    - ...

    Raises `OSError` if it runs into an error while calling WinAPI functions.
    """

    # The core idea (take both the logical drives AND the network drives to account for disconnected network drives) is from here: https://stackoverflow.com/a/53618843/14442082
    return sorted(set(itertools.chain(get_logical_drives(), get_network_drives())))

def get_free_drive_letters() -> list[DriveLetter]:
    """
    Returns the list of `tempdrive.DriveLetter` objects that represent the unassigned drive letters of the system, available for drive substitution using `tempdrive.subst()`.

    Note that this list never includes A: and B: because they were historically used for floppy disk drives, and Windows handles them specially, so it's ill-advised to use them for other purposes.

    Raises `OSError` if it runs into an error while calling WinAPI functions.
    """

    all_drives = set(DriveLetter(letter) for letter in string.ascii_uppercase[2:]) # C..Z
    used_drives = set(get_used_drive_letters())

    return sorted(all_drives - used_drives)
