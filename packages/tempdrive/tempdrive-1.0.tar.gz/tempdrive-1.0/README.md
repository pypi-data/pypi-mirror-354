# tempdrive

`tempdrive` is a Python library defining functions and context managers to create and remove Windows disk drive substitutions, i.e. virtual disk drives that act as an alias to a directory.

This functionality can be useful to get around the 260-character path length limit present in many Windows applications.

## Class `tempdrive.DriveLetter`

This class represents a Windows disk drive letter. It can be both initialized and queryied in a variety of formats. (See `DriveLetter.is_drive_string()`.)

Properties:
- `letter: str`: Just the uppercase drive letter, eg. `C`
- `device: str`: The uppercase drive letter, plus a colon, eg. `C:`
- `path: pathlib.Path`: Path of the root folder of the drive, eg. `C:\`

Static methods:
- `is_drive_string(s: str)`: Returns whether `s` is a valid drive string, i.e. one of the following (X can be any lower or upper case English letter): "X", "X:", "X:\", "X:/".

## Context manager `tempdrive.temporary_drive()`

Context manager to create a new drive substitution (using `tempdrive.subst()`) for the specified path with an automatically chosen drive letter. Remove drive substitution on exit.

When used in a `with` statement, the target of the `as` clause will be set to a `pathlib.Path` pointing to the newly created drive's root folder.

This function can be useful if a script needs to work within a deeply nested folder, and it starts hitting the 260-character path length limit.

Arguments:
- `path: pathlib.Path`: Path the newly created drive substitution should point to.
- `log: Callable[[str], None]`: Logging function to use for informational messages upon adding and removing the drive substitution. If unspecified or set to `None`, no messages are emitted.

Raises `tempdrive.TempDriveError` if there is no available drive letter to use. Raises `OSError` if it runs into an error while calling WinAPI functions.

## Function `tempdrive.subst()`

Creates new drive substitution, similarly to [subst.exe](https://ss64.com/nt/subst.html).

For example, `tempdrive.subst(tempdrive.DriveLetter("w:"), Path(r'c:\Windows'))` creates a virtual W: drive that acts as an alias to the Windows folder.

Substituted drives can be useful if an application starts hitting the 260-character path length limit.

Arguments:
- `drive: tempdrive.DriveLetter`: Drive letter to use for newly created drive substitution.
- `path: pathlib.Path`: Path the newly created drive substitution should point to.

Raises `tempdrive.TempDriveError` if drive is already in use. Raises `OSError` if it runs into an error while calling WinAPI functions.

## Function `tempdrive.unsubst()`

Removes a drive substitution created by `tempdrive.subst()`.

Arguments:
- `drive: tempdrive.DriveLetter`: Drive letter of substitution to remove.

Raises `tempdrive.TempDriveError` if the drive does not exist, or is not a substitution. Raises `OSError` if it runs into an error while calling WinAPI functions.

## Function `get_used_drive_letters()`

Returns the list of `tempdrive.DriveLetter` objects that represent all disk drives currently present in the system. This includes:
- Physical drives
- Virtual/substituted disk drives
- Connected network drives
- Disconnected but registered network drives
- ...

Raises `OSError` if it runs into an error while calling WinAPI functions.

## Function `get_free_drive_letters()`

Returns the list of `tempdrive.DriveLetter` objects that represent the unassigned drive letters of the system, available for drive substitution using `tempdrive.subst()`.

Note that this list never includes A: and B: because they were historically used for floppy disk drives, and Windows handles them specially, so it's ill-advised to use them for other purposes.

Raises `OSError` if it runs into an error while calling WinAPI functions.

## Licensing

This library is licensed under the MIT license.
