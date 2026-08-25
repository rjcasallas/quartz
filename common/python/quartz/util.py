import traceback
import subprocess
import os
import re
from enum import Enum
from quartz.error import Error
from typing import Any
from quartz.log import Log


class Parse:

    @staticmethod
    def string(x) -> str:
        if x is None:
            return "∅"
        elif isinstance(x, str):
            return x
        elif isinstance(x, bool):
            return x and "●" or "○"
        elif isinstance(x, int):
            return str(x)
        elif isinstance(x, float):
            return str(x)
        elif isinstance(x, list):
            return ", ".join(map(Parse.string, x))
        elif isinstance(x, dict):
            return ", ".join(f"{k}: {v}" for k, v in x.items())
        elif isinstance(x, Enum):
            return x.name
        else:
            return str(x)

    @staticmethod
    def integer(x) -> int:
        if x is None:
            return 0
        elif isinstance(x, int):
            return x
        elif isinstance(x, str):
            if x.startswith("0x"):
                return int(x, 16)
            elif x.startswith("0o"):
                return int(x, 8)
            elif x.startswith("0b"):
                return int(x, 2)
            else:
                return int(x)
        else:
            return int(x)

    @staticmethod
    def float(x) -> float:
        if x is None:
            return 0.0
        elif isinstance(x, float):
            return x
        elif isinstance(x, str):
            return float(x)
        else:
            return float(x)

    @staticmethod
    def boolean(x) -> bool:
        if x is None:
            return False
        elif isinstance(x, bool):
            return x
        elif isinstance(x, str):
            return x.lower() in ["true", "1", "yes", "on"]
        else:
            return x and True or False

    @staticmethod
    def dict(x, default_tag="value"):
        # Comma-separated "xx:yy" pairs; xxx becomes default_tag
        if isinstance(x, dict):
            return x
        if not isinstance(x, str):
            return {}
        x = x.strip()
        if not x:
            return {}
        d = {}
        for part in x.split(","):
            part = part.strip()
            if not part:
                continue
            if ":" not in part:
                d[default_tag] = part
                continue
            k, v = part.split(":", 1)
            d[k.strip()] = v.strip()
        return d


class Format:

    @staticmethod
    def pascal(x) -> str:
        return "".join([s.capitalize() for s in re.split("_|-", Format.name(x))])

    @staticmethod
    def camel(x) -> str:
        if not x:
            return x
        parts = x.replace("-", "_").split("_")
        if len(parts) == 1:
            return parts[0].lower()
        return parts[0].lower() + "".join(word.capitalize() for word in parts[1:])

    @staticmethod
    def snake(x) -> str:
        return x.lower().replace(" ", "_").replace("-", "_")

    @staticmethod
    def kebab(x) -> str:
        return x.lower().replace(" ", "-").replace("_", "-")

    @staticmethod
    def name(text):
        s = text and str(text) or ""
        return re.sub(r"[^a-zA-Z0-9]", "_", s)

    @staticmethod
    def plural(x) -> str:
        s = Format.name(x)
        if s.endswith("child"):
            return s[:-5] + "children"
        elif "y" == s[-1]:
            return s[:-1] + "ies"
        elif s.endswith("ch"):
            return s + "es"
        elif s.endswith("as"):
            return s + "es"
        else:
            return s + "s"

    @staticmethod
    def abbreviate(name):
        if not isinstance(name, str):
            return "?"
        alias = ""
        parts = name.strip("_").split("_")
        # Concatenate the initials
        for p in parts:
            if len(p) > 0:
                alias += p[0].lower()
        return alias


class Command:
    BULLET = "‣"

    def __init__(
        self,
        filename=None,
        do_echo=True,
        do_silent=False,
        do_output=False,
        do_check=True,
    ):
        self.filename = filename
        self.do_echo = do_echo and (not do_silent)
        self.do_silent = do_silent
        self.do_output = do_output
        self.do_check = do_check

    def execute(self, args, header=None):
        cmd = " ".join(map(str, args))
        if self.filename is None:
            # Standard output
            if header:
                Log.info(str(header))
            if self.do_echo:
                Log.list(str(cmd), 1, Command.BULLET)
            if self.do_output:
                # Return command output
                return subprocess.check_output(cmd, shell=True).decode("utf-8")
            elif self.do_silent:
                # Return error code silently
                result = subprocess.run(
                    cmd, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL
                )
            else:
                # Return error code with output
                result = subprocess.run(cmd, shell=True, stderr=subprocess.STDOUT)
        else:
            # Filename
            with open(self.filename, "w") as f:
                if self.do_echo:
                    Log.list(str(cmd), 1, Command.BULLET)
                result = subprocess.run(cmd, shell=True, stderr=f, stdout=f)

        if self.do_check and (0 != result.returncode):
            if not self.do_echo:
                Log.list(str(cmd), 1, Command.BULLET)
            Error.fail("Command failed with code {}".format(result.returncode))

        return result.returncode
