import ctypes
import ctypes.wintypes as wintypes
from typing import cast as typing_cast

from tempdrive._byref import ByRef as ByRef

kernel32 = ctypes.windll.kernel32
mpr = ctypes.windll.mpr

kernel32.DefineDosDeviceW.argtypes = [wintypes.DWORD, wintypes.LPCWSTR, wintypes.LPCWSTR]
kernel32.DefineDosDeviceW.restype = wintypes.BOOL
def DefineDosDeviceW(flags: int, device_name: str, target_path: str | None) -> bool:
    return typing_cast(int, kernel32.DefineDosDeviceW(flags, device_name, target_path)) != 0 # BOOL is an int, we need to convert it to bool

kernel32.QueryDosDeviceW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
kernel32.QueryDosDeviceW.restype = wintypes.DWORD
def QueryDosDeviceW(device_name: str | None, buffer: ctypes.Array[ctypes.c_wchar], bufsize: int) -> int:
    return typing_cast(int, kernel32.QueryDosDeviceW(device_name, buffer, bufsize))

kernel32.GetLogicalDriveStringsW.argtypes = [wintypes.DWORD, wintypes.LPWSTR]
kernel32.GetLogicalDriveStringsW.restype = wintypes.DWORD
def GetLogicalDriveStringsW(bufferlength: int, buffer: ctypes.Array[ctypes.c_wchar]) -> int:
    return typing_cast(int, kernel32.GetLogicalDriveStringsW(bufferlength, buffer))

class NETRESOURCEW(ctypes.Structure):
    _fields_ = [
        ('dwScope', wintypes.DWORD),
        ('dwType', wintypes.DWORD),
        ('dwDisplayType', wintypes.DWORD),
        ('dwUsage', wintypes.DWORD),
        ('lpLocalName', wintypes.LPWSTR),
        ('lpRemoteName', wintypes.LPWSTR),
        ('lpComment', wintypes.LPWSTR),
        ('lpProvider', wintypes.LPWSTR),
    ]

mpr.WNetOpenEnumW.argtypes = [wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, ctypes.POINTER(NETRESOURCEW), ctypes.POINTER(wintypes.HANDLE)]
mpr.WNetOpenEnumW.restype = wintypes.DWORD
def WNetOpenEnumW(scope: int, type: int, usage: int, netresource: ByRef[NETRESOURCEW] | None, henum: ByRef[wintypes.HANDLE]) -> int:
    return typing_cast(int, mpr.WNetOpenEnumW(scope, type, usage, netresource, henum))

mpr.WNetEnumResourceW.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD), ctypes.c_void_p, ctypes.POINTER(wintypes.DWORD)]
mpr.WNetEnumResourceW.restype = wintypes.DWORD
def WNetEnumResourceW(henum: wintypes.HANDLE, count: ByRef[wintypes.DWORD], buffer: ctypes.Array[NETRESOURCEW], bufsize: ByRef[wintypes.DWORD]) -> int:
    return typing_cast(int, mpr.WNetEnumResourceW(henum, count, buffer, bufsize))
