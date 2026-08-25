from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional


class Logger(ABC):

    @abstractmethod
    def write(self, text: str) -> None:
        pass

    @abstractmethod
    def info(self, text: str) -> None:
        pass

    @abstractmethod
    def warning(self, text: str) -> None:
        pass

    @abstractmethod
    def error(self, text: str) -> None:
        pass

    @abstractmethod
    def test(self, text: str) -> None:
        pass

    @abstractmethod
    def list(self, text: str, level: int = 0, bullet: str = None) -> None:
        pass

    @abstractmethod
    def debug(self, text: str) -> None:
        pass


class PrettyLogger(Logger):

    Margin = "  "
    Bullets = ["•", "∙", "◦", "・"]

    @abstractmethod
    def write(self, text: str) -> None:
        pass

    def info(self, text: str) -> None:
        self.write(self._prefix(text, "✲"))  # ✲✱✻

    def warning(self, text: str) -> None:
        self.write(self._prefix(text, "⚠️"))

    def error(self, text: str) -> None:
        self.write(self._prefix(text, "🚫"))

    def test(self, text: str) -> None:
        self.write(self._prefix(text, "🧪"))

    def list(self, text: str, level: int = 0, bullet: str = None) -> None:
        if bullet is None:
            bullet = self.Bullets[min(level, len(self.Bullets) - 1)]
        indent = level * self.Margin
        self.write(self._prefix(text, f"{indent}{bullet}"))

    def debug(self, text: str) -> None:
        self.write(self._prefix(text, "🪲"))

    # Insert icon before text, but after any leading newlines.
    def _prefix(self, text: str, pre: str) -> str:
        stripped = text.lstrip("\n")
        leading = text[: len(text) - len(stripped)]
        return f"{leading}{pre} {stripped}"


class PrintLogger(PrettyLogger):

    def write(self, text: str) -> None:
        print(text)


class Log:

    class Level(Enum):
        Off = 0
        Error = 1
        Warning = 2
        Info = 3
        Test = 4
        Debug = 5

    _level: Level = Level.Debug
    _logger: Logger = PrintLogger()

    @staticmethod
    def level(value: "Log.Level" = None) -> "Log.Level":
        if value is not None:
            Log._level = value
        return Log._level

    @staticmethod
    def write(text: Optional[str] = None) -> None:
        if Log._logger:
            Log._logger.write(text or "")

    @staticmethod
    def info(text: Optional[str] = None) -> None:
        if Log._logger and (Log._level.value >= Log.Level.Info.value):
            Log._logger.info(text or "")

    @staticmethod
    def warning(text: Optional[str] = None) -> None:
        if Log._logger and (Log._level.value >= Log.Level.Warning.value):
            Log._logger.warning(text or "")

    @staticmethod
    def error(text: Optional[str] = None) -> None:
        if Log._logger and (Log._level.value >= Log.Level.Error.value):
            Log._logger.error(text or "")

    @staticmethod
    def test(text: Optional[str] = None) -> None:
        if Log._logger and (Log._level.value >= Log.Level.Test.value):
            Log._logger.test(text or "")

    @staticmethod
    def list(text: Optional[str] = None, level: int = 0, bullet: str = None) -> None:
        if Log._logger and (Log._level.value >= Log.Level.Debug.value):
            Log._logger.list(text or "", level, bullet)

    @staticmethod
    def dict(text: Optional[str], d: dict, level: int = 0) -> None:
        Log.list(text, level)
        Log._dict(d, level + 1)

    @staticmethod
    def _dict(d: dict, level: int = 0) -> None:
        for k, v in d.items():
            if isinstance(v, dict):
                Log.list(f"{k}:", level)
                Log._dict(v, level + 1)
            else:
                Log.list(f"{k}: {v}", level)

    @staticmethod
    def debug(text: Optional[str] = None) -> None:
        if Log._logger and (Log._level.value >= Log.Level.Debug.value):
            Log._logger.debug(text or "")
