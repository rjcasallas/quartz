from enum import Enum
import traceback
import os
from quartz.log import Log
from typing import Any


class Error(Enum):

    Success         = 0x00
    Failed          = 0x01
    Invalid         = 0x02
    Missing         = 0x03
    Overflow        = 0x04
    Duplicated      = 0x05
    Open            = 0x06
    Read            = 0x07
    Write           = 0x08
    Parsing         = 0x09
    Unimplemented   = 0x0A
    Exit            = 0xFF

    @staticmethod
    def fail(message: str, code: int = 1) -> None:
        trace = traceback.extract_stack()
        for t in trace[:-1]:
            # filename = t.filename.removeprefix(prefix)
            prefix = os.getcwd() + "/"
            filename = t.filename.removeprefix(prefix)
            location = "{}:{}".format(filename, t.lineno)
            Log.list("{:64}\t{}".format(location, t.line), 1, "✕")
        Log.list(message, 2, "🚫")
        exit(code)

    @staticmethod
    def missing(what: str) -> None:
        Error.fail(f"Missing: {what}")

    @staticmethod
    def invalid(what: str, value: Any) -> None:
        Error.fail(f"Invalid {what} ({type(value)}): {value}")
