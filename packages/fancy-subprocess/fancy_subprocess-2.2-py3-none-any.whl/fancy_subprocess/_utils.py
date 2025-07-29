__all__ = [
    'value_or',
]

import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Optional, TypeVar

import oslex
if sys.platform=='win32':
    from ntstatus import NtStatus, NtStatusSeverity, ThirtyTwoBits
else:
    import signal

T = TypeVar('T')
U = TypeVar('U')

def value_or(value: T | None, default: U) -> T | U:
    if value is None:
        return default
    else:
        return value

def oslex_join(cmd: Sequence[str | Path]) -> str:
    return oslex.join([str(arg) for arg in cmd])

def stringify_exit_code(exit_code: int) -> Optional[str]:
    if sys.platform=='win32':
        # Windows
        try:
            bits = ThirtyTwoBits(exit_code)
        except ValueError:
            return None

        try:
            code = NtStatus(bits)
            if code.severity!=NtStatusSeverity.STATUS_SEVERITY_SUCCESS:
                return code.name
        except ValueError:
            pass

        return f'0x{bits.unsigned_value:08X}'
    else:
        # POSIX
        if exit_code<0:
            try:
                return signal.Signals(-exit_code).name
            except ValueError:
                return 'unknown signal'

    return None
