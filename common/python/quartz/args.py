from quartz.log import Log
from quartz.error import Error
from quartz.util import Parse
from enum import Enum
from typing import Optional, List, Dict, Any, Iterator
from abc import ABC, abstractmethod


class Types(Enum):
    Binary  = 0x00
    Int8u   = 0x01
    Int16u  = 0x02
    Int32u  = 0x03
    Int64u  = 0x04
    Real    = 0x05
    Date    = 0x06
    Text    = 0x08
    Int8s   = 0x09
    Int16s  = 0x0A
    Int32s  = 0x0B
    Int64s  = 0x0C
    Path    = 0x0D
    Boolean = 0x0E
    Flag    = 0x0F


class Parameter:

    def __init__(
        self,
        name: str,
        short: Optional[str],
        type: Types,
        default: Optional[Any] = None,
        description: Optional[str] = None,
        hidden: bool = False,
    ):
        if not isinstance(name, str):
            Error.invalid("name", name)
        if (short is not None) and not isinstance(short, str):
            Error.invalid("short", short)
        if not isinstance(type, Types):
            Error.invalid("type", type)
        if (description is not None) and not isinstance(description, str):
            Error.invalid("description", description)
        if (hidden is not None) and not isinstance(hidden, bool):
            Error.invalid("hidden", hidden)
        self._name = name
        self._short = short
        self._type = type
        self._default = default
        self._description = description
        self._hidden = hidden

    def __hash__(self):
        return hash((self._name))

    def __eq__(self, x):
        if isinstance(x, str):
            return self._name == x
        if isinstance(x, Parameter):
            return self._name == x._name
        return False

    def __repr__(self):
        type = self._type.name
        value = Parse.string(self._default)
        desc = f" ({self._description})" if self._description else ""
        short = f", -{self.short}" if self.short else ""
        return f"--{self._name}{short}: {type}: {value}{desc}"

    def __str__(self):
        return self._name

    @property
    def name(self) -> str:
        return self._name

    @property
    def short(self) -> Optional[str]:
        return self._short

    @property
    def type(self) -> Types:
        return self._type

    @property
    def default(self) -> Optional[Any]:
        return self._default

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def hidden(self) -> bool:
        return self._hidden


class Argument(Parameter):

    def __init__(
        self,
        name: str,
        short: Optional[str],
        type: Types,
        default: Optional[Any] = None,
        description: Optional[str] = None,
        hidden: bool = False,
    ):
        super().__init__(name, short, type, default, description, hidden)
        self._value = default

    # def __repr__(self):
    #     type = self.type.name
    #     value = Parse.string(self.value)
    #     desc = f' ({self.description})' if self.description else ""
    #     short = f', -{self.short}' if self.short else ''
    #     return f'"{self.name}"{short}: {type} = {value}{desc}'

    def __str__(self):
        return Parse.string(self._value)

    def __int__(self):
        return Parse.integer(self._value)

    def __float__(self):
        return Parse.float(self._value)

    def __bool__(self):
        return Parse.boolean(self._value)

    def __str__(self):
        return Parse.string(self._value)

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value: Any):
        self._value = value

    def reset(self):
        self._value = self._default

    def string(self):
        return None if (self._value is None) else Parse.string(self._value)

    def integer(self):
        return None if (self._value is None) else Parse.integer(self._value)

    def float(self):
        return None if (self._value is None) else Parse.float(self._value)

    def boolean(self):
        return None if (self._value is None) else Parse.boolean(self._value)


class ArgumentSet(ABC):

    def __init__(self, parent=None):
        self._parent = parent

    @property
    def parent(self) -> "ArgumentSet":
        return self._parent

    @parent.setter
    def parent(self, value: "ArgumentSet"):
        self._parent = value

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    def get(self, x) -> Argument:
        a = self.find(x)
        if a is None:
            Error.invalid("argument", x)
        return a

    def find(self, x) -> Optional[Argument]:
        if isinstance(x, Parameter):
            return self.find(x._name)

    def set(self, x: Any, value: Any) -> None:
        self.get(x).value = value
        return self


class NamedArgumentSet(ArgumentSet):

    def __init__(self):
        super().__init__()
        self._names = {}
        self._shorts = {}

    def __len__(self) -> int:
        return len(self._names)

    def __contains__(self, name: str) -> bool:
        return (name in self._names) or (name in self._shorts)

    def __getitem__(self, name: str) -> Argument:
        return self.get(name)

    def __setitem__(self, name: str, value: Any) -> None:
        self.set(name, value)

    def __iter__(self) -> Iterator[Argument]:
        return iter(self._names.values())

    def clear(self):
        self._names = {}
        self._shorts = {}

    def reset(self):
        for a in self._names.values():
            a.reset()

    def add(
        self,
        name: str,
        short: str,
        type: Types,
        default: Optional[Any] = None,
        description: Optional[str] = None,
        hidden: bool = False,
    ) -> None:
        arg = Argument(name, short, type, default, description, hidden)
        self._names[name] = arg
        if short is not None:
            self._shorts[short] = arg
        return arg

    def find(self, name: str) -> Optional[Argument]:
        if isinstance(name, str):
            if name in self._names:
                return self._names[name]
            if name in self._shorts:
                return self._shorts[name]
            if self._parent is not None:
                return self._parent.find(name)
        return super().find(name)


class FixedArgumentSet(NamedArgumentSet):

    def __init__(self):
        super().__init__()
        self._args = []

    def __len__(self) -> int:
        return len(self._args)

    def __getitem__(self, x) -> Parameter:
        return self.get(x)

    def __setitem__(self, x, value: Any) -> None:
        self.set(x, value)

    def __iter__(self) -> Iterator[Parameter]:
        return iter(self._args)

    def clear(self):
        super().clear()
        self._args = []

    def add(
        self,
        name: str,
        type: Types,
        default: Optional[Any] = None,
        description: Optional[str] = None,
        hidden: bool = False,
    ) -> None:
        arg = super().add(name, None, type, default, description, hidden)
        # Remove duplicates
        self._args = [a for a in self._args if a.name != name]
        # Add new (unique) argument
        self._args.append(arg)

    def find(self, x) -> Optional[Argument]:
        if isinstance(x, int):
            if 0 <= x < len(self._args):
                return self._args[x]
        return super().find(x)


class Arguments(ArgumentSet):

    def __init__(self):
        self._parent = None
        self._fixed = FixedArgumentSet()
        self._dashed = NamedArgumentSet()

    def __len__(self) -> int:
        return len(self._fixed) + len(self._dashed)

    def __getitem__(self, x) -> Argument:
        return self.get(x)

    def __setitem__(self, x, value: Any) -> None:
        return self.set(x, value)

    @property
    def parent(self) -> ArgumentSet:
        return self._parent

    @parent.setter
    def parent(self, value: ArgumentSet):
        self._parent = value
        self._dashed.parent = value
        self._fixed.parent = value

    @property
    def fixed(self) -> "Arguments.Fixed":
        return self._fixed

    @property
    def dashed(self) -> "Arguments.Dashed":
        return self._dashed

    def clear(self):
        self.fixed.clear()
        self.dashed.clear()

    def reset(self):
        self.fixed.reset()
        self.dashed.reset()

    def find(self, x) -> Optional[Argument]:
        a = self._fixed.find(x)
        if a is None:
            a = self._dashed.find(x)
        return a

    def string(self, x: str) -> Optional[str]:
        return self.get(x).string()

    def integer(self, x: str) -> Optional[int]:
        return self.get(x).integer()

    def float(self, x: str) -> Optional[float]:
        return self.get(x).float()

    def boolean(self, x: str) -> Optional[bool]:
        return self.get(x).boolean()

    def print(self, level: int = 0) -> None:
        # Print fixed arguments first
        for arg in self._fixed:
            if not arg.hidden:
                s = Parse.string(arg.value)
                Log.list(f"{arg.name}: {s}", level, "▪︎")
        for arg in self._dashed:
            if not arg.hidden:
                s = Parse.string(arg.value)
                Log.list(f"{arg.name}: {s}", level, "∙")

    def help(self, level: int = 0) -> None:
        # Print fixed arguments first
        for arg in self._fixed:
            if not arg.hidden:
                Log.list(repr(arg), level, "▪︎")
        for arg in self._dashed:
            if not arg.hidden:
                Log.list(repr(arg), level, "∙")

    def parse(self, args: List[str], ignore=False) -> None:
        # Build a lookup map for short options
        parsed_fixed = []
        i = 0
        self.reset()

        while i < len(args):
            arg = args[i]
            # Handle long options (--option)
            if arg.startswith("--"):
                name = arg[2:]  # Remove '--'
                param = self.find(name)
                if param is None:
                    if ignore:
                        i += 1
                        continue
                    Error.fail(f"Unknown option: {name}")

                # Check if option needs a value
                if param.type == Types.Flag:
                    param.value = True
                    i += 1
                else:
                    if i + 1 >= len(args):
                        if ignore:
                            i += 1
                            continue
                        Error.fail(f"Option {name} requires a value")
                    value = args[i + 1]
                    # Convert Boolean type values to boolean
                    if param.type == Types.Boolean:
                        value = value.lower() in ["true", "1", "yes", "on"]
                    param.value = value
                    i += 2

            # Handle short options (-a)
            elif arg.startswith("-") and len(arg) == 2:
                short_name = arg[1:]  # Remove '-'
                param = self.find(short_name)
                if param is None:
                    if ignore:
                        i += 1
                        continue
                    Error.fail(f"Unknown option: -{short_name}")

                # Check if option needs a value
                if param.type == Types.Flag:
                    param.value = True
                    i += 1
                else:
                    if i + 1 >= len(args):
                        if ignore:
                            i += 1
                            continue
                        Error.fail(f"Option -{short_name} requires a value")
                    value = args[i + 1]
                    # Convert Boolean type values to boolean
                    if param.type == Types.Boolean:
                        value = value.lower() in ["true", "1", "yes", "on"]
                    param.value = value
                    i += 2

            # Handle multiple short flags (-abc)
            elif arg.startswith("-") and len(arg) > 2:
                for char in arg[1:]:
                    param = self.find(char)
                    if param is None:
                        if ignore:
                            continue
                        Error.fail(f"Unknown option: -{char}")
                    if param.type != Types.Flag:
                        if ignore:
                            continue
                        Error.fail(
                            f"Option -{char} requires a value and cannot be combined"
                        )
                    param.value = True
                i += 1

            # Handle fixed arguments
            else:
                pos_index = len(parsed_fixed)
                if pos_index >= len(self._fixed):
                    if ignore:
                        i += 1
                        continue
                    Error.fail(f"Too many fixed arguments. Expected {len(self._fixed)}")
                param = self._fixed.get(pos_index)
                param.value = arg
                parsed_fixed.append(arg)
                i += 1

        # Validate that we have all required fixed arguments
        required_fixed = sum(1 for p in self._fixed if p.default is None)
        if (len(parsed_fixed) < required_fixed) and not self.boolean("help"):
            Error.fail(
                f"Not enough fixed arguments. Expected {required_fixed}, got {len(parsed_fixed)}"
            )
