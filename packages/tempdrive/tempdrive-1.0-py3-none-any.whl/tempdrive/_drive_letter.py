__all__ = [
    'DriveLetter',
]

import re
from dataclasses import dataclass
from typing import Final
from pathlib import Path

@dataclass(frozen=True, order=True)
class DriveLetter:
    """
    This class represents a Windows disk drive letter. It can be both initialized and queryied in a variety of formats. (See `DriveLetter.is_drive_string()`.)

    Properties:
    - `letter: str`: Just the uppercase drive letter, eg. `C`
    - `device: str`: The uppercase drive letter, plus a colon, eg. `C:`
    - `path: pathlib.Path`: Path of the root folder of the drive, eg. `C:\`

    Static methods:
    - `is_drive_string(s: str)`: Returns whether `s` is a valid drive string, i.e. one of the following (X can be any lower or upper case English letter): "X", "X:", "X:\", "X:/".
    """

    letter: str

    def __init__(self, drive_string: str) -> None:
        if not DriveLetter.is_drive_string(drive_string):
            raise ValueError(f'Not a valid drive string: "{drive_string}"')

        # Get around frozen=True's limitation
        # See details here: https://stackoverflow.com/a/58336722
        object.__setattr__(self, 'letter', drive_string[0].upper())

    def __str__(self) -> str:
        return self.device

    def __repr__(self) -> str:
        return f'DriveLetter("{self.device}")'

    @property
    def device(self) -> str:
        return f'{self.letter}:'

    @property
    def path(self) -> Path:
        return Path(f'{self.letter}:/')

    @staticmethod
    def is_drive_string(s: str) -> bool:
        """
        Returns whether s is a valid drive string, i.e. one of the following (X can be any lower or upper case English letter): "x", "x:", "x:\", "x:/".
        """

        return re.fullmatch(r'[a-zA-Z](:[\\/]?)?', s) is not None
