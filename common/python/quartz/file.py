import os
import time
import json
import yaml
from abc import ABC, abstractmethod
from quartz.log import Log


class Paths:

    def __init__(self, base: str = None):
        self._base = base or "."

    def base(self, path: str) -> str:
        return self.normalize(os.path.join(self._base, path))

    @staticmethod
    def quartz(path=None) -> str:
        quartz_dir = os.environ.get("QUARTZ_DIR")
        if quartz_dir:
            quartz_dir = Paths.normalize(quartz_dir)
        else:
            quartz_dir = Paths.normalize(os.path.dirname(__file__) + "/../../..")
        return Paths.normalize(os.path.join(quartz_dir, path or ""))

    @staticmethod
    def normalize(path):
        if path is None:
            return None
        return os.path.realpath(os.path.abspath(os.path.normpath(path or ".")))

    # Replace extension
    @staticmethod
    def replacex(path, ext=None):
        b, _ = os.path.splitext(path)
        return f"{b}.{ext}"

    @staticmethod
    def extension(path: str) -> str:
        return os.path.splitext(path)[1]

    @staticmethod
    def dir(path=None):
        if path is None:
            return os.getcwd()
        elif os.path.isfile(path):
            return os.path.dirname(path)
        elif os.path.isdir(path):
            return path
        # Non-existent path
        return None

    @staticmethod
    def split(path):
        dir = os.path.dirname(path)
        name, ext = os.path.splitext(os.path.basename(path))
        return (dir, name, ext)


class File(ABC):

    def __init__(self, path):
        self._path = path

    @staticmethod
    def hash(path):
        if not os.path.exists(path):
            return None
        return time.strftime(
            "%Y-%m-%d_%H:%M:%S", time.localtime(os.path.getmtime(path))
        )

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self, data):
        pass

    @staticmethod
    def findExtension(path, ext):
        dir = Paths.dir(path)
        for x in os.listdir(dir):
            d, n, e = Paths.split(x)
            if ext == e:
                return Paths.child(dir, x)


class TextFile(File):

    def read(self):
        with open(self._path, "r") as f:
            return f.read()

    def write(self, data):
        with open(self._path, "w") as f:
            f.write(data)


class BinaryFile(File):

    def read(self):
        if self._path is None:
            return bytes()
        with open(self._path, "rb") as f:
            return bytes(f.read())

    def write(self, data):
        if x is None:
            data = bytes()
        elif isinstance(x, bytes):
            data = x
        else:
            data = str(x).encode("utf-8")
        with open(self._path, "wb") as f:
            f.write(data)


class JsonFile(File):

    def read(self):
        with open(self._path, "r") as f:
            return json.loads(f.read())

    def write(self, data):
        with open(self._path, "w") as f:
            json.dump(data, f, indent=2)
            f.write("\n")


class YamlFile(File):

    @staticmethod
    def get(yaml, tag, default=None):
        if tag in yaml:
            return yaml[tag]
        else:
            return default

    @staticmethod
    def string(yaml, tag, default=None):
        x = YamlFile.get(yaml, tag, default)
        if x is None:
            return None
        return str(x)

    @staticmethod
    def integer(yaml, tag, default=None):
        x = YamlFile.get(yaml, tag, default)
        if x is None:
            return None
        return int(x)

    @staticmethod
    def float(yaml, tag, default=None):
        x = YamlFile.get(yaml, tag, default)
        if x is None:
            return None
        return float(x)

    @staticmethod
    def boolean(yaml, tag, default=None):
        x = YamlFile.get(yaml, tag, default)
        if x is None:
            return None
        return bool(x)

    def read(self):
        omap = False
        with open(self._path, "r") as f:
            line = f.readline()
            omap = "!!omap" == line.strip()
            f.seek(0)
            d = yaml.safe_load(f)
            return omap and self._omap(d) or d

    def write(self, data, style="|"):
        with open(self._path, "w") as f:
            yaml.dump(data, f, indent=2, default_style=style, sort_keys=False)
            f.write("\n")

    def _omap(self, y):
        if y is None:
            return None
        if isinstance(y, list):
            d = {}
            for x in y:
                d[x[0]] = x[1]
            return d
        return y
