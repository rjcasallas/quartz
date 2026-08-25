# Tests for the args module.
import unittest

from quartz.args import (
    Parameter,
    Argument,
    NamedArgumentSet,
    FixedArgumentSet,
    Arguments,
    Types,
)


class TestParameter(unittest.TestCase):

    def setUp(self):
        self.param = Parameter("test", "t", Types.Text, "default_value", "Test parameter")

    def test_parameter_init(self):
        self.assertEqual(self.param.name, "test")
        self.assertEqual(self.param.short, "t")
        self.assertEqual(self.param.type, Types.Text)
        self.assertEqual(self.param.default, "default_value")
        self.assertEqual(self.param.description, "Test parameter")
        self.assertFalse(self.param.hidden)

    def test_parameter_hidden(self):
        param = Parameter("hidden", None, Types.Flag, hidden=True)
        self.assertTrue(param.hidden)

    def test_parameter_repr(self):
        repr_str = repr(self.param)
        self.assertIn('test', repr_str)
        self.assertIn("Text", repr_str)
        self.assertIn("default_value", repr_str)

    def test_parameter_eq(self):
        self.assertEqual(
            Parameter("same", None, Types.Text), Parameter("same", "s", Types.Flag)
        )
        self.assertEqual(self.param, "test")
        self.assertNotEqual(self.param, "other")


class TestArgument(unittest.TestCase):

    def setUp(self):
        self.arg = Argument("verbose", "v", Types.Boolean, False)

    def test_argument_value_and_reset(self):
        self.assertFalse(self.arg.value)
        self.arg.value = True
        self.assertTrue(self.arg.value)
        self.arg.reset()
        self.assertFalse(self.arg.value)

    def test_argument_converters(self):
        text = Argument("name", "n", Types.Text, "alice")
        number = Argument("count", "c", Types.Int32u, "42")
        real = Argument("ratio", "r", Types.Real, "3.5")
        flag = Argument("enabled", "e", Types.Boolean, "yes")

        self.assertEqual(text.string(), "alice")
        self.assertEqual(number.integer(), 42)
        self.assertAlmostEqual(real.float(), 3.5)
        self.assertTrue(flag.boolean())


class TestNamedArgumentSet(unittest.TestCase):

    def setUp(self):
        self.args = NamedArgumentSet()

    def test_add_find_by_name_and_short(self):
        self.args.add("verbose", "v", Types.Flag)
        self.assertIn("verbose", self.args)
        self.assertIn("v", self.args)
        self.assertEqual(self.args.get("verbose").name, "verbose")
        self.assertEqual(self.args.get("v").name, "verbose")

    def test_set_and_reset(self):
        self.args.add("input", "i", Types.Text, "a.txt")
        self.args.set("input", "b.txt")
        self.assertEqual(self.args.get("input").value, "b.txt")
        self.args.reset()
        self.assertEqual(self.args.get("input").value, "a.txt")

    def test_parent_lookup(self):
        parent = NamedArgumentSet()
        parent.add("debug", "d", Types.Flag)
        child = NamedArgumentSet()
        child.parent = parent
        self.assertIsNotNone(child.find("debug"))
        self.assertIsNotNone(child.find("d"))


class TestFixedArgumentSet(unittest.TestCase):

    def setUp(self):
        self.args = FixedArgumentSet()

    def test_add_find_by_index_and_name(self):
        self.args.add("file", Types.Text)
        self.assertEqual(len(self.args), 1)
        self.assertEqual(self.args.get(0).name, "file")
        self.assertEqual(self.args.get("file").name, "file")

    def test_add_duplicate_name_keeps_single_entry(self):
        self.args.add("file", Types.Text)
        self.args.add("file", Types.Path)
        self.assertEqual(len(self.args), 1)
        self.assertEqual(self.args.get(0).type, Types.Path)


class TestArguments(unittest.TestCase):

    def setUp(self):
        self.args = Arguments()

    def test_arguments_len(self):
        self.assertEqual(len(self.args), 0)
        self.args.dashed.add("verbose", "v", Types.Flag)
        self.args.fixed.add("file", Types.Text)
        self.assertEqual(len(self.args), 2)

    def test_getitem_with_name_index_and_parameter(self):
        self.args.dashed.add("verbose", "v", Types.Flag)
        self.args.fixed.add("file", Types.Text)
        self.args.parse(["-v", "main.txt"])

        self.assertTrue(self.args["verbose"].value)
        self.assertEqual(self.args[0].value, "main.txt")
        self.assertTrue(self.args[Parameter("verbose", None, Types.Flag)].value)

    def test_parse_long_and_short_with_values(self):
        self.args.dashed.add("input", "i", Types.Text)
        self.args.dashed.add("verbose", "v", Types.Boolean)
        self.args.fixed.add("output", Types.Text)
        self.args.parse(["--input", "in.txt", "-v", "yes", "out.txt"])

        self.assertEqual(self.args.get("input").value, "in.txt")
        self.assertTrue(self.args.get("verbose").value)
        self.assertEqual(self.args.get("output").value, "out.txt")

    def test_parse_multiple_short_flags(self):
        self.args.dashed.add("verbose", "v", Types.Flag)
        self.args.dashed.add("debug", "d", Types.Flag)
        self.args.parse(["-vd"])
        self.assertTrue(self.args.get("verbose").value)
        self.assertTrue(self.args.get("debug").value)

    def test_parse_with_defaults(self):
        self.args.dashed.add("verbose", "v", Types.Boolean, False)
        self.args.parse([])
        self.assertFalse(self.args.get("verbose").value)

    def test_unknown_option_exits(self):
        with self.assertRaises(SystemExit):
            self.args.parse(["--unknown"])

    def test_missing_value_exits(self):
        self.args.dashed.add("input", "i", Types.Text)
        with self.assertRaises(SystemExit):
            self.args.parse(["--input"])

    def test_too_many_fixed_exits(self):
        self.args.fixed.add("file", Types.Text)
        with self.assertRaises(SystemExit):
            self.args.parse(["a.txt", "b.txt"])

    def test_not_enough_fixed_exits(self):
        self.args.dashed.add("help", "h", Types.Boolean, False)
        self.args.fixed.add("file1", Types.Text)
        self.args.fixed.add("file2", Types.Text)
        with self.assertRaises(SystemExit):
            self.args.parse(["a.txt"])

    def test_parse_ignore(self):
        self.args.dashed.add("known", "k", Types.Flag)
        self.args.parse(["--unknown", "-k", "extra"], ignore=True)
        self.assertTrue(self.args.get("known").value)

    def test_find_with_parent(self):
        parent = Arguments()
        parent.dashed.add("parent_opt", "p", Types.Text, "x")
        child = Arguments()
        child.parent = parent

        self.assertEqual(child.find("parent_opt").name, "parent_opt")
        self.assertEqual(child.find("p").name, "parent_opt")


if __name__ == "__main__":
    unittest.main()
