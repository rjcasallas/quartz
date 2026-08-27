import pybars
import os
import keyword
from abc import ABC
from typing import List
from quartz.log import Log
from quartz.error import Error
from quartz.util import Format
from quartz.file import Paths
from quartz.db.meta import Table, Column, Link
from quartz.file import TextFile


class Helpers:

    def _name(self, x=None, shorten=False):
        if isinstance(x, str):
            return x
        if isinstance(x, dict) and ("name" in x):
            return x["name"]
        if isinstance(x, Table):
            return x.name
        if isinstance(x, Column):
            if shorten and x.name.endswith("_id"):
                return x.name[:-3]
            else:
                return x.name
            #return x.name[:-3] if x.name.endswith("_id") else x.name
        if isinstance(x, Link):
            return x.name
        Log.warning(f"Invalid name: {x}; {type(x)}")
        return "N?".format(type(x))

    def _field(self, x=None, shorten=False):
        name = "_" + self._name(x, shorten)
        return name

    def _param(self, x=None):
        name = self._name(x)
        if keyword.iskeyword(name):
            return f"{name}_"
        else:
            return name

    def _plural(self, x=None):
        if isinstance(x, Table) and x.singular:
            return x.name
        return Format.plural(x)

    def _pascal(self, x=None):
        return Format.pascal(self._name(x))

    def _len(self, x=None):
        return len(x)

    def _curly(self, x=None):
        return f"{{{x}}}"

    def _plus(self, x, y=None, z=None):
        if (y is None) and (z is None):
            return int(x) + 1
        return int(x) + (int(y) if y else 0) + (int(z) if z else 0)

    def __or(self, this, a=False, b=False):
        return a or b

    def __and(self, this, a=False, b=False):
        return a and b

    def __name(self, this, text=None):
        return self._name(text or this.context)

    def __name_(self, this, text=None):
        return self._name(text or this.context, shorten=True)

    def __field(self, this, text=None):
        return self._field(text or this.context)

    def __field_(self, this, text=None):
        return self._field(text or this.context, shorten=True)

    def __param(self, this, text=None):
        return self._param(text or this.context)

    def __plural(self, this, text=None):
        return self._plural(text or this.context)

    def __pascal(self, this, text=None):
        return self._pascal(text or this.context)

    def __ppascal(self, this, text=None):
        return self._pascal(self._plural(text or this.context))

    def __each(self, this, options, items, items2=None, items3=None):
        i1 = (
            (isinstance(items, list) and items)
            or (isinstance(items, dict) and list(items.values()))
            or []
        )
        i2 = (
            (isinstance(items2, list) and items2)
            or (isinstance(items2, dict) and list(items2.values()))
            or []
        )
        i3 = (
            (isinstance(items3, list) and items3)
            or (isinstance(items3, dict) and list(items3.values()))
            or []
        )
        all = sorted(i1 + i2 + i3)
        result = []
        for i in all:
            result.extend(options["fn"](i))
        return result

    def __list(self, this, options, items, items2=None, items3=None):
        all = (items or []) + (items2 or []) + (items3 or [])
        result = []
        count = len(all)
        for i in range(0, count):
            if i > 0:
                result.append(pybars.strlist(", "))
            k = options["fn"](all[i])
            result.extend(k)
        return result

    def __len(self, this, text=None):
        return self._len(text if (text is not None) else this.context)

    def __curly(self, this, text=None):
        return self._curly(text if (text is not None) else this.context)

    def __plus(self, this, x=None, y=None, z=None):
        return self._plus(this.context if (x is None) else x, y, z)

    def compile(self):
        return {
            "-or": self.__or,
            "-and": self.__and,
            "-name": self.__name,
            "-name-": self.__name_,
            "-field": self.__field,
            "-field-": self.__field_,
            "-param": self.__param,
            "-plural": self.__plural,
            "-pascal": self.__pascal,
            "-ppascal": self.__ppascal,
            "-each": self.__each,
            "-list": self.__list,
            "-len": self.__len,
            "-curly": self.__curly,
            "-plus": self.__plus,
        }


class Generator:

    def __init__(self, template, helpers=None):
        self._template = template
        self._helpers = helpers or {}

    def generate(self, out_path, context):
        # Template
        if not os.path.isfile(self._template):
            Error.missing(self._template)
        text = TextFile(self._template).read()
        templ = pybars.Compiler().compile(text)
        # Output
        out_dir = os.path.dirname(out_path)
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir, exist_ok=True)

        text = templ(context, helpers=self.helpers())
        Log.list(out_path, bullet="✏️")
        TextFile(out_path).write(text)

    def helpers(self):
        if isinstance(self._helpers, dict):
            return self._helpers
        if isinstance(self._helpers, Helpers):
            return self._helpers.compile()
        return {}


class Target:
    def __init__(self, template: str, output: str, context: dict = None):
        self._template = template
        self._output = output
        self._context = context


class TargetGenerator(ABC):

    def __init__(self, templates_dir, helpers=None):
        self._template_dir = templates_dir
        self._helpers = helpers

    def generate(self, targets: List[str], output_dir, context=None):
        Log.info(f"\nGenerating [{output_dir}]")
        self._templates = {}
        for target in targets:
            # Log.debug(f"Target: {target._template} --> {target._output}")
            templ_path = os.path.join(self._template_dir, target._template)
            out_path = os.path.join(output_dir, target._output)
            gen = Generator(templ_path, self._helpers)
            gen.generate(out_path, target._context or context or {})
