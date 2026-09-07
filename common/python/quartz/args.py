from quartz.log import Log
from quartz.util import Parse
from quartz.error import Error
from enum import Enum
from typing import Any, Iterator
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
    Invalid = 0xFF


class Parameter:

    def __init__(self, name:str, short:str|None, type_:Types, default:str|int|float|bool|None=Types.Invalid, description:str=None, hidden:bool=False):
        if not isinstance(name, str):
            Error.invalid("name", name)
        if not ((short is None) or isinstance(short, str)):
            Error.invalid("short", short)
        if not isinstance(type_, Types):
            Error.invalid("type", type)
        if not ((default is None) or isinstance(default, str) or isinstance(default, int) or isinstance(default, float) or isinstance(default, bool) or (Types.Invalid == default)):
            Error.invalid("default", default)
        if not ((description is None) or isinstance(description, str)):
            Error.invalid("description", description)
        if not ((hidden is None) or isinstance(hidden, bool)):
            Error.invalid("hidden", hidden)
        self._name = name
        self._short = short
        self._type = type_
        self._default = default
        self._desc = description
        self._hidden = hidden

    def __str__(self):
        return self._name

    def __repr__(self):
        type = self._type.name
        value = Parse.string(self._default)
        desc = f" ({self._desc})" if self._desc else ""
        short = f", -{self.short}" if self.short else ""
        return f"--{self._name}{short}: {type}: {value}{desc}"

    @property
    def name(self) -> str:
        return self._name

    @property
    def short(self) -> str|None:
        return self._short

    @property
    def type(self) -> Types:
        return self._type

    @property
    def default(self) -> str|int|float|bool:
        return None if isinstance(self._default, Types) else self._default

    @property
    def description(self) -> str:
        return self._desc

    @property
    def hidden(self) -> bool:
        return self._hidden


class Argument(Parameter):

    def __init__(self, name:str, short:str|None, type_:Types, default:str|int|float|bool|None, description:str, hidden:bool):
        super().__init__(name, short, type_, default, description, hidden)
        self.value = default

    def __str__(self):
        return Parse.string(self.value)

    def __int__(self):
        return Parse.integer(self.value)

    def __float__(self):
        return Parse.real(self.value)

    def __bool__(self):
        return Parse.boolean(self.value)

    def __repr__(self):
        type = self._type.name
        value = Parse.string(self.value)
        desc = f" ({self._desc})" if self._desc else ""
        short = f", -{self.short}" if self.short else ""
        return f"--{self._name}{short}: {type}: {value}{desc}"

    @property
    def value(self) -> str|int|float|bool:
        return None if isinstance(self._value, Types) else self._value
    @value.setter
    def value(self, x:str|int|float|bool|None):
        if (x is None) or (Types.Invalid == x):
            self._value = False if (Types.Flag == self.type) else x
            return
        v = None
        match self.type:
            case Types.Text:
                if isinstance(x, str):
                    v = x
                elif isinstance(x, bool):
                    v = x and "true" or "false"
                elif x is not None:
                    v = str(x)
            case Types.Binary | Types.Text | Types.Path:
                if isinstance(x, str):
                    v = x
            case Types.Int8u | Types.Int8s | Types.Int16u | Types.Int16s | Types.Int32u | Types.Int32s | Types.Int64u | Types.Int64s:
                if isinstance(x, int):
                    v = x
                elif isinstance(x, str):
                    v = Parse.integer(x)
            case Types.Real:
                if isinstance(x, float):
                    v = x
                elif isinstance(x, int):
                    v = float(x)
                elif isinstance(x, str):
                    v = Parse.real(x)
            case Types.Date:
                if isinstance(x, str):
                    v = x
            case Types.Boolean | Types.Flag:
                if isinstance(x, bool):
                    v = x
                elif isinstance(x, int):
                    v = bool(x)
                elif isinstance(x, str):
                    v = Parse.boolean(x)
        if v is not None:
            self._value = v
        else:
            t = self.type.name.lower()
            Error.fail(f'Invalid value {x} {type(x)} for "{self.name}" ({t})')

    def valid(self):
        return not isinstance(self._value, Types)

    def reset(self):
        self.value = self.default

    def string(self):
        return None if (self.value is None) else Parse.string(self.value)

    def integer(self):
        return None if (self.value is None) else Parse.integer(self.value)

    def real(self):
        return None if (self.value is None) else Parse.real(self.value)

    def boolean(self):
        return None if (self.value is None) else Parse.boolean(self.value)


class FixedArgument(Argument):

    def __init__(self, name:str, type:Types, default:None|str|int|float|bool, description:str, hidden:bool):
        super().__init__(name, None, type, default, description, hidden)

    def __repr__(self):
        type = self._type.name
        value = Parse.string(self.value)
        desc = f" ({self._desc})" if self._desc else ""
        return f"{self._name}: {type}: {value}{desc}"


class ArgumentSet(ABC):

    def __init__(self, parent=None):
        self._parent = parent
        self._tag = "*"

    @property
    def parent(self) -> ArgumentSet:
        return self._parent
    @parent.setter
    def parent(self, p:ArgumentSet):
        if not isinstance(p, ArgumentSet):
            Error.invalid("arguments' parent", p)
        self._parent = p

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def clear(self):
        pass

    def find(self, x:Any) -> Argument|None:
        if self.parent is not None:
            return self.parent.find(x)

    def get(self, x):
        a = self.find(x)
        if a is None:
            Error.invalid("argument", x)
        return a

    def set(self, x, value):
        self.get(x).value = value
        return self

    def string(self, x:Any) -> str:
        return self.get(x).string()

    def integer(self, x:Any) -> int:
        return self.get(x).integer()

    def real(self, x:Any) -> float:
        return self.get(x).real()

    def boolean(self, x:Any) -> bool:
        return self.get(x).boolean()


class NamedArgumentSet(ArgumentSet):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._names = {}
        self._shorts = {}

    def __setitem__(self, name:str, value:Any) -> None:
        self.set(name, value)

    def __getitem__(self, name:str) -> Argument:
        return self.get(name)

    def __contains__(self, name:str) -> bool:
        return (name in self._names) or (name in self._shorts)

    def __len__(self) -> int:
        return len(self._names)

    def __iter__(self) -> Iterator[Argument]:
        return iter(self._names.values())

    def reset(self):
        for a in self._names.values():
            a.reset()

    def clear(self):
        self._names = {}
        self._shorts = {}

    def find(self, x:Any) -> Argument|None:
        if isinstance(x, str):
            s = ', '.join([ f"'{k}':'{a.name}'" for k, a in self._shorts.items() ])
            if x in self._names:
                return self._names[x]
            if x in self._shorts:
                a = self._shorts[x]
                return a
        return super().find(x)

    def _add(self, a:Argument):
        self._names[a.name] = a
        if a.short is not None:
            self._shorts[a.short] = a
        return a


class FixedArgumentSet(NamedArgumentSet):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._ordered = []

    def __getitem__(self, x) -> Argument:
        return self.get(x)

    def __setitem__(self, x, value: Any) -> None:
        self.set(x, value)

    def __len__(self) -> int:
        return len(self._ordered)

    def __iter__(self) -> Iterator[Argument]:
        return iter(self._ordered)

    def clear(self):
        super().clear()
        self._ordered = []

    def add(self, name:str, type:Types, default:str|int|float|bool|None=Types.Invalid, description:str=None, hidden:bool=False):
        a = self._add(FixedArgument(name, type, default, description, hidden))
        # Remove duplicates
        self._ordered = [a for a in self._ordered if a.name != name]
        # Add new (unique) argument
        self._ordered.append(a)

    def find(self, x:Any) -> Argument|None:
        if isinstance(x, int):
            return self._ordered[x] if (0 <= x < len(self._ordered)) else None
        return super().find(x)


class DashedArgumentSet(NamedArgumentSet):

    def add(self, name:str, short:str|None, type:Types, default:str|int|float|bool|None=Types.Invalid, description:str=None, hidden:bool=False):
        return self._add(Argument(name, short, type, default, description, hidden))


class Arguments(ArgumentSet):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._fixed = FixedArgumentSet()
        self._dashed = DashedArgumentSet()

    def __getitem__(self, x) -> Argument:
        return self.get(x)

    def __setitem__(self, x, value: Any) -> None:
        return self.set(x, value)

    def __len__(self) -> int:
        return len(self._fixed) + len(self._dashed)

    @property
    def fixed(self) -> FixedArgumentSet:
        return self._fixed

    @property
    def dashed(self) -> NamedArgumentSet:
        return self._dashed

    def reset(self):
        self.fixed.reset()
        self.dashed.reset()

    def clear(self):
        self.fixed.clear()
        self.dashed.clear()

    def find(self, x:Any) -> Argument|None:
        a = self._fixed.find(x)
        if a is None:
            a = self._dashed.find(x)
            if a is None:
                a = super().find(x)
        return a

    def print(self, level:int=0):
        # Fixed
        for a in self._fixed:
            if not a.hidden:
                s = Parse.string(a)
                Log.list(f"{a.name}: {s}", level, "▪︎")
        # Dashed
        for a in self._dashed:
            if not a.hidden:
                s = Parse.string(a)
                Log.list(f"{a.name}: {s}", level, "∙")

    def help(self, level:int=0):
        # Fixed
        for a in self._fixed:
            if not a.hidden:
                s = Parse.string(a)
                Log.list(repr(a), level, "▪︎")
        # Dashed
        for a in self._dashed:
            if not a.hidden:
                s = Parse.string(a)
                Log.list(repr(a), level, "∙")

    def parse(self, args:list[str], strict=True):
        dashed = None
        fixed_count = 0
        fixed_total = len(self._fixed)
        for a in args:
            d = "*" if dashed is None else dashed.name
            n = '-3'.isnumeric()
            # Dashed name
            if a.startswith("-") and not self._is_number(a):
                # Dashed argument
                if dashed is None:
                    name = a.lstrip("-")
                    if 0 == len(name):
                        # Ignore
                        continue
                    dashed = self.find(name)
                    if dashed is not None:
                        if Types.Flag == dashed.type:
                            dashed.value = not dashed.default
                            dashed = None
                    else:
                        self._parseError(f'Missing argument "{name}"', strict)
                else:
                    self._parseError(f'Missing value for "{dashed.name}"', strict)
            # Dashed value
            elif dashed is not None:
                dashed.value = a
                dashed = None
            # Fixed argument
            elif fixed_count < fixed_total:
                fixed = self._fixed[fixed_count]
                fixed.value = a
                fixed_count += 1
            elif fixed_total > 0:
                self._parseError(f'Too many fixed arguments ({fixed_count}/{fixed_total}): "{a}" {type(a)}', strict)
            else:
                self._parseError(f'Invalid argument: "{a}" {type(a)}', strict)
        # Check for dangling dashed
        if dashed is not None:
            self._parseError(f'Missing value for "{dashed.name}"', strict)
        # Check for null values
        for a in self._fixed:
            if not a.valid():
                self._parseError(f'Missing value for "{a.name}"', strict) 
        for a in self._dashed:
            if not a.valid():
                self._parseError(f'Missing value for "{a.name}"', strict) 


    def _parseError(self, msg:str, strict:bool):
        if strict:
            Error.fail(msg)
        else:
            Log.warning(msg)
        return strict

    def _is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False