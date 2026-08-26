from quartz.log import Log
from quartz.util import Parse, Format
from quartz.file import YamlFile
from quartz.error import Error
from enum import Enum
import os


class Column:

    class Type(Enum):
        Unknown = 0
        Text = 1
        Integer = 2
        Real = 3
        Blob = 4
        Date = 5
        Boolean = 6

        def __str__(self):
            return self.name.lower()

    @staticmethod
    def parse(x) -> "Column.Type":
        if not isinstance(x, str):
            return Column.Type.Unknown
        lower = x.lower()
        if "text" in lower or "char" in lower or "varchar" in lower or "clob" in lower:
            return Column.Type.Text
        elif "int" in lower:
            return Column.Type.Integer
        elif (
            "real" in lower
            or "float" in lower
            or "double" in lower
            or "numeric" in lower
            or "decimal" in lower
        ):
            return Column.Type.Real
        elif "blob" in lower or "binary" in lower:
            return Column.Type.Blob
        elif (
            "date" in lower
            or "time" in lower
            or "datetime" in lower
            or "timestamp" in lower
        ):
            return Column.Type.Date
        elif "bool" in lower:
            return Column.Type.Boolean
        else:
            return Column.Type.Unknown

    def __init__(
        self,
        table: "Table",
        name: str,
        type_: str,
        notnull: bool = False,
        default=None,
        pk: bool = False,
        auto: bool = False,
    ):
        # Info
        self._table = table
        self._name = name
        self._alias = Format.abbreviate(name)
        self._type = Column.parse(type_)
        self._notnull = notnull
        self._default = default
        self._pk = pk
        self._auto = auto
        # Indexes
        self._indexed = False
        self._unique = False
        # Foreign keys
        self._into = None
        self._from = []

    def __str__(self):
        return f"{self._name}"

    def __eq__(self, other: "Column"):
        return self._name == other._name

    def __hash__(self):
        return hash(
            (
                self._name,
                self._type,
                self._notnull,
                self._default,
                self._pk,
                self._auto,
                self._indexed,
                self._unique,
                self._into,
            )
        )

    def __repr__(self):
        type_ = (
            self._type.name.lower()
            if isinstance(self._type, Column.Type)
            else str(self._type).lower()
        )
        notnull = Parse.string(Parse.boolean(self._notnull))
        default = Parse.string(self._default)
        pk = Parse.string(Parse.boolean(self._pk))
        # auto = Parse.string(Parse.boolean(self._auto))
        indexed = Parse.string(Parse.boolean(self._indexed))
        unique = Parse.string(Parse.boolean(self._unique))
        return f'"{self._name}", type:{type_}, notnull:{notnull}, default:{default}, pk:{pk}, indexed:{indexed}, unique:{unique}'

    @property
    def table(self) -> "Table":
        return self._table

    @property
    def name(self) -> str:
        return self._name

    @property
    def alias(self) -> str:
        return self._alias

    @property
    def type(self) -> str:
        return self._type

    @property
    def notnull(self) -> str:
        return self._notnull

    @property
    def pk(self) -> str:
        return self._pk

    @property
    def auto(self) -> str:
        return self._auto

    @property
    def indexed(self) -> str:
        return self._indexed

    @property
    def foreign(self) -> bool:
        return self._into is not None

    @property
    def into(self):
        return self._into

    @into.setter
    def into(self, col):
        self._into = col
        self._indexed = True
        col._from.append(self)

    def index(self, indexed: bool = True, unique: bool = False):
        self._indexed = self._indexed or indexed
        self._unique = unique
        if (self.table._lookup is None) and (Column.Type.Text == self._type):
            self.table._lookup = self

    def print(self, level: int = 0):
        bullet = "★" if self.auto else "✦" if self._pk else "∙"
        Log.list(repr(self), level, bullet)
        if self._into:
            into = Parse.string(f"{self._into.table}.{self._into}")
            Log.list(into, level + 1, "▴")
        for f in self._from:
            from_ = Parse.string(f"{f.table}.{f._name}")
            Log.list(from_, level + 1, "▾")


class Link:

    def __init__(self, source: Column, from_: Column, into: Column):
        if not isinstance(source, Column):
            Error.invalid("column", source)
        if not isinstance(from_, Column):
            Error.invalid("from", from_)
        if not isinstance(into, Column):
            Error.invalid("into", into)
        i_name = into._name.removesuffix("_id")
        self._name = f"{source.table.name}_{i_name}"
        self._alias = Format.abbreviate(self._name)
        self._source = source
        self._from = from_
        self._into = into
        self._target = into._into
        self._special = False
        self._key = from_.name.removesuffix("_id")

    def __str__(self):
        return f'"{self._name}" {self._source.table}.{self._source} → {self._target.table}.{self._target}'  # ➤

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other: "Link"):
        return (self._source == other._source) and (self._target == other._target)

    def __hash__(self):
        return hash((self._source, self._target))

    @property
    def key(self) -> str:
        return self._key
        # return f"{self._source.table.name}.{self._source.name}/{self._target.table.name}.{self._target.name}"

    @property
    def name(self) -> str:
        return self._name

    @property
    def alias(self) -> str:
        return self._alias

    @property
    def source(self) -> Column:
        return self._source

    @property
    def from_(self) -> Column:
        return self._from

    @property
    def into(self) -> Column:
        return self._into

    @property
    def target(self) -> Column:
        return self._target

    @property
    def special(self) -> bool:
        return self._special


class Table:

    class Type(Enum):
        Unknown = 0
        Generic = 1
        Subtype = 2
        Lookup = 3
        Junction = 4
        Aggregate = 5

        def __str__(self):
            return self.name.lower()

    def __init__(self, name: str, type_: "Table.Type" = None, columns: list = None):
        self._name = name
        self._alias = Format.abbreviate(name)
        self._type = type_ or Table.Type.Unknown
        self._columns = columns or []
        self._auto = None  # columns
        self._parent = None
        self._lookup = None  # column
        self._singular = False
        self._keys = []
        self._nonkeys = []
        self._nonauto = []
        self._indexed = []
        self._links = {}
        self._references = {}  # Links

    def __str__(self):
        return self._name

    def __repr__(self):
        sing = "  S" if self._singular else ""
        return f'"{self._name}"({len(self._columns)}) <{self._type.name.lower()}>{sing}'

    def __lt__(self, other):
        return self.name < other.name

    def __eq__(self, other):
        return self.name == other.name

    @property
    def name(self) -> str:
        return self._name

    @property
    def alias(self) -> str:
        return self._alias

    @property
    def type(self) -> str:
        return self._type

    @property
    def auto(self) -> Column:
        return self._auto

    @property
    def parent(self) -> Column:
        return self._parent

    @property
    def is_entity(self) -> Column:
        return self._auto or (self._parent is not None)

    @property
    def lookup(self) -> Column:
        return self._lookup

    @property
    def singular(self) -> str:
        return self._singular

    @property
    def columns(self) -> list[Column]:
        return self._columns

    @property
    def keys(self) -> list[Column]:
        return self._keys

    @property
    def nonkeys(self) -> list[Column]:
        return self._nonkeys

    @property
    def nonauto(self) -> list[Column]:
        return self._nonauto

    @property
    def links(self) -> list[Link]:
        return list(self._links.values())

    @property
    def references(self) -> list[Link]:
        return list(self._references.values())

    @property
    def indexed(self) -> list[Column]:
        return self._indexed

    def add(self, col: Column):
        self._columns.append(col)

    @property
    def entity(self) -> bool:
        return (
            (Table.Type.Generic == self.type)
            or (Table.Type.Subtype == self.type)
            or (Table.Type.Lookup == self.type)
        )

    @property
    def aggregate(self) -> bool:
        return Table.Type.Aggregate == self._type

    def find(self, x) -> Column:
        if isinstance(x, int):
            if x >= 0 or x < len(self.columns):
                return self.columns[x]
        elif isinstance(x, str):
            for c in self.columns:
                if c.name == x:
                    return c
        Error.missing(f'column "{self.name}.{x}"')

    def compile(self, config):
        # Classif columns
        for col in self.columns:
            if col.pk:
                self.keys.append(col)
            else:
                self.nonkeys.append(col)
                if col.indexed:
                    self.indexed.append(col)
            if col.auto:
                self._auto = col
            else:
                self.nonauto.append(col)
        # Determine table type
        self._classify()
        # Configuration
        if config:
            self._singular = ("singular" in config) and config["singular"]
        if Table.Type.Subtype == self.type:
            self._parent = self.keys[0].into.table


    def link(self):
        # Create links
        for col in self.columns:
            for f in col._from:
                if (Table.Type.Junction == f.table.type) or (
                    Table.Type.Aggregate == f.table.type
                ):
                    for c in f.table.columns:
                        if c != f and c.into:
                            l = Link(col, f, c)
                            if l.name not in self._links:
                                self._links[l.name] = l
                                c.table._references[l.name] = l

    def _classify(self) -> "Table.Type":
        pk_count = len(self.keys)
        # Junction table: All PK columns are foreign keys
        if (pk_count > 1) and all(col.into is not None for col in self.keys):
            self._type = Table.Type.Aggregate if self.nonkeys else Table.Type.Junction
        # Subtype table: One PK column that is a foreign key
        elif (1 == pk_count) and self.keys[0].into:
            self._type = Table.Type.Subtype

        # Lookup table: One PK column and one text column
        elif self.lookup and (1 == pk_count) and (2 == len(self.columns)):
            self._type = Table.Type.Lookup
        else:
            self._type = Table.Type.Generic

    def print(self, level: int = 0):
        Log.list(repr(self), level, "▪︎")
        for col in self.columns:
            col.print(level + 1)
        for link in self._links:
            Log.list(repr(link), level + 1, "⦿")
        for link in self.references:
            Log.list(repr(link), level + 1, "○")
        Log.list(self.lookup.name if self.lookup else "No lookup", level + 1, "◇")
        # Log.debug(f"Keys: {[col.name for col in self.keys]}")


class Schema:

    def __init__(self, name: str, schema_path: str):
        self._name = name
        self._tables = {}
        self._entities = []
        self._junctions = []
        self._aggregates = []
        self._specials = {}
        self._filters = {}
        # configuration
        config_path = "{}/meta.yaml".format(os.path.dirname(schema_path))
        self._config = (
            YamlFile(config_path).read() if os.path.isfile(config_path) else None
        )
        # Log.debug(f"CONFIG: {self._config}")
        # exit(0)

    def __str__(self):
        return self._name

    def __repr__(self):
        return f'"{self._name}"({len(self._tables)})'

    # def __getitem__(self, x) -> Table:
    #     return self.get(x)

    @property
    def tables(self) -> list[Table]:
        return self._tables

    @property
    def entities(self) -> list[Table]:
        return self._entities

    @property
    def junctions(self) -> list[Table]:
        return self._junctions

    @property
    def aggregates(self) -> list[Table]:
        return self._aggregates

    @property
    def specials(self) -> list[Table]:
        return self._specials

    @property
    def filters(self) -> list[Table]:
        return self._filters

    def add(self, t: Table):
        if ("sqlite_sequence" != t._name) and not t._name.startswith("_"):
            self._tables[t._name] = t

    def find(self, x) -> Table:
        if isinstance(x, str):
            if x in self._tables:
                return self._tables[x]
        Error.missing(f'table "{x}"')

    def compile(self):
        entities = []
        junctions = []
        aggregates = []
        # Classify tables and columns
        for t in self._tables.values():
            conf = (
                self._config and t.name in self._config and self._config[t.name] or None
            )
            t.compile(conf)
            if t.entity:
                entities.append(t)
            else:
                junctions.append(t)
            if t.aggregate:
                aggregates.append(t)
            if t.lookup:
                self._filters[t.lookup.name] = t.lookup
        # Link tables
        for t in self._tables.values():
            t.link()
            for l in t.links:
                l._special = l.key not in self._tables
                if l.special:
                    self._specials[l.name] = l
        # Sort
        self._entities = sorted(entities, key=lambda t: t.name)
        self._junctions = sorted(junctions, key=lambda t: t.name)
        self._aggregates = sorted(aggregates, key=lambda t: t.name)
        return self

    def print(self, level: int = 0):
        Log.list(repr(self), level, "★")
        for t in self._tables.values():
            t.print(level + 1)
