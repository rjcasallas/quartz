from quartz.log import Log
from quartz.args import Types, Parameter, Argument, NamedArgumentSet, OrderedArgumentSet, Arguments
import unittest

unittest.TestLoader.sortTestMethodsUsing = None


class TestBase:

    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestA(TestBase, unittest.TestCase):

    def testParameter(self):
        Log.test("\nTest Parameter")
        r = Parameter("red", None, Types.Text)
        g = Parameter("green", "g", Types.Int8u, 42, "Olive green", False)
        b = Parameter("blue", "bl", Types.Real, description="Sky blue", hidden=True, default=1.2)
        y = Parameter("yellow", "yel", Types.Boolean, description="Sunny", default=True)
        # red
        self.assertEqual(r.name, "red")
        self.assertIsNone(r.short)
        self.assertEqual(r.type, Types.Text)
        self.assertIsNone(r.default)
        self.assertIsNone(r.description)
        self.assertEqual(r.hidden, False)
        # green
        self.assertEqual(g.name, "green")
        self.assertEqual(g.short, "g")
        self.assertEqual(g.type, Types.Int8u)
        self.assertEqual(g.default, 42)
        self.assertEqual(g.description, "Olive green")
        self.assertEqual(g.hidden, False)
        # blue
        self.assertEqual(b.name, "blue")
        self.assertEqual(b.short, "bl")
        self.assertEqual(b.type, Types.Real)
        self.assertEqual(b.default, 1.2)
        self.assertEqual(b.description, "Sky blue")
        self.assertEqual(b.hidden, True)
        # yellow
        self.assertEqual(y.name, "yellow")
        self.assertEqual(y.short, "yel")
        self.assertEqual(y.type, Types.Boolean)
        self.assertEqual(y.default, True)
        self.assertEqual(y.description, "Sunny")
        self.assertEqual(y.hidden, False)

    def testArgument(self):
        Log.test("\nTest Argument")
        r = Argument("red", None, Types.Text)
        g = Argument("green", "g", Types.Int8u, 42, "Olive green", False)
        b = Argument("blue", "bl", Types.Real, description="Sky blue", hidden=True, default=1.2)
        y = Argument("yellow", "yel", Types.Boolean, description="Sunny", default=True)
        # values
        r.value = "abc123"
        g.value = 213
        b.value = 12.34
        y.value = "false"
        # red
        self.assertEqual(r.name, "red")
        self.assertIsNone(r.short)
        self.assertEqual(r.type, Types.Text)
        self.assertIsNone(r.default)
        self.assertIsNone(r.description)
        self.assertEqual(r.hidden, False)
        self.assertEqual(r.value, "abc123")
        r.value = 12
        self.assertEqual(r.value, "12")
        r.value = 2.3
        self.assertEqual(r.value, "2.3")
        r.value = False
        self.assertEqual(r.value, "false")
        r.reset()
        self.assertIsNone(r.value)
        # green
        self.assertEqual(g.name, "green")
        self.assertEqual(g.short, "g")
        self.assertEqual(g.type, Types.Int8u)
        self.assertEqual(g.default, 42)
        self.assertEqual(g.description, "Olive green")
        self.assertEqual(g.hidden, False)
        self.assertEqual(g.value, 213)
        g.value = "34"
        self.assertEqual(g.value, 34)
        g.reset()
        self.assertEqual(g.value, 42)
        # blue
        self.assertEqual(b.name, "blue")
        self.assertEqual(b.short, "bl")
        self.assertEqual(b.type, Types.Real)
        self.assertEqual(b.default, 1.2)
        self.assertEqual(b.description, "Sky blue")
        self.assertEqual(b.hidden, True)
        self.assertEqual(b.value, 12.34)
        b.value = 123
        self.assertEqual(b.value, 123)
        b.value = "5.3"
        self.assertEqual(b.value, 5.3)
        b.reset()
        self.assertEqual(b.value, 1.2)
        # yellow
        self.assertEqual(y.name, "yellow")
        self.assertEqual(y.short, "yel")
        self.assertEqual(y.type, Types.Boolean)
        self.assertEqual(y.default, True)
        self.assertEqual(y.description, "Sunny")
        self.assertEqual(y.hidden, False)
        self.assertEqual(y.value, False)
        y.value = 1
        self.assertEqual(y.value, True)
        y.value = False
        self.assertEqual(y.value, False)
        y.reset()
        self.assertEqual(y.value, True)

    def testNamedArgumentSet(self):
        Log.test("\nTest NamedArgumentSet")
        args = NamedArgumentSet()
        args.add("red", None, Types.Real)
        args.add("green", "g", Types.Boolean, True)
        args.add("blue", "b", Types.Text, "once in a blue moon")
        args.add("cyan", "c", Types.Int16s, -4321)
        # red
        r = args.get("red")
        self.assertIsNotNone(r)
        self.assertEqual(r.name, "red")
        self.assertEqual(r.type, Types.Real)
        self.assertIsNone(r.default)
        self.assertIsNone(r.value)
        r.value = 0.12345
        self.assertIsNone(r.default)
        self.assertEqual(r.value, 0.12345)
        self.assertEqual(args.real("red"), 0.12345)
        # green
        g = args.get("g")
        self.assertIsNotNone(g)
        self.assertEqual(g.name, "green")
        self.assertEqual(g.type, Types.Boolean)
        self.assertEqual(g.default, True)
        self.assertEqual(g.value, True)
        g.value = 0
        self.assertEqual(g.default, True)
        self.assertEqual(g.value, False)
        self.assertEqual(args.boolean("g"), False)
        # blue
        b = args.get("blue")
        self.assertIsNotNone(b)
        self.assertEqual(b.name, "blue")
        self.assertEqual(b.type, Types.Text)
        self.assertEqual(b.default, "once in a blue moon")
        self.assertEqual(b.value, "once in a blue moon")
        b.value = "something else"
        self.assertEqual(b.default, "once in a blue moon")
        self.assertEqual(b.value, "something else")
        self.assertEqual(args.string("b"), "something else")
        # cyan
        c = args.get("c")
        self.assertIsNotNone(b)
        self.assertEqual(c.name, "cyan")
        self.assertEqual(c.type, Types.Int16s)
        self.assertEqual(c.default, -4321)
        self.assertEqual(c.value, -4321)
        c.value = 1025
        self.assertEqual(c.default, -4321)
        self.assertEqual(c.value, 1025)
        self.assertEqual(args.integer("cyan"), 1025)

    def testOrderedArgumentSet(self):
        Log.test("\nTest OrderedArgumentSet")
        args = OrderedArgumentSet()
        args.add("red", Types.Real)
        args.add("green", Types.Boolean, True)
        args.add("blue", Types.Text, "once in a blue moon")
        args.add("cyan", Types.Int16s, -4321)
        # red
        r = args.get(0)
        self.assertIsNotNone(r)
        self.assertEqual(r.name, "red")
        self.assertEqual(r.type, Types.Real)
        self.assertIsNone(r.default)
        self.assertIsNone(r.value)
        r.value = 0.12345
        self.assertIsNone(r.default)
        self.assertEqual(r.value, 0.12345)
        self.assertEqual(args.real("red"), 0.12345)
        # green
        g = args.get(1)
        self.assertIsNotNone(g)
        self.assertEqual(g.name, "green")
        self.assertEqual(g.type, Types.Boolean)
        self.assertEqual(g.default, True)
        self.assertEqual(g.value, True)
        g.value = 0
        self.assertEqual(g.default, True)
        self.assertEqual(g.value, False)
        self.assertEqual(args.boolean("green"), False)
        # blue
        b = args.get(2)
        self.assertIsNotNone(b)
        self.assertEqual(b.name, "blue")
        self.assertEqual(b.type, Types.Text)
        self.assertEqual(b.default, "once in a blue moon")
        self.assertEqual(b.value, "once in a blue moon")
        b.value = "something else"
        self.assertEqual(b.default, "once in a blue moon")
        self.assertEqual(b.value, "something else")
        self.assertEqual(args.string("blue"), "something else")
        # cyan
        c = args.get(3)
        self.assertIsNotNone(b)
        self.assertEqual(c.name, "cyan")
        self.assertEqual(c.type, Types.Int16s)
        self.assertEqual(c.default, -4321)
        self.assertEqual(c.value, -4321)
        c.value = 1025
        self.assertEqual(c.default, -4321)
        self.assertEqual(c.value, 1025)
        self.assertEqual(args.integer("cyan"), 1025)

    def testArguments(self):
        Log.test("\nTest Arguments")
        args = Arguments()
        args.dashed.add("cyan", "c", Types.Int16s)
        args.fixed.add("red", Types.Real)
        args.dashed.add("yellow", "y", Types.Int16u)
        args.dashed.add("margenta", "ma", Types.Binary)
        args.fixed.add("green", Types.Boolean)
        args.fixed.add("blue", Types.Text)
        # red
        r = args.get(0)
        self.assertIsNotNone(r)
        self.assertEqual(r.name, "red")
        self.assertEqual(r.type, Types.Real)
        self.assertIsNone(r.default)
        self.assertIsNone(r.value)
        r.value = 0.12345
        self.assertIsNone(r.default)
        self.assertEqual(r.value, 0.12345)
        self.assertEqual(args.real("red"), 0.12345)
        # green
        g = args.get(1)
        self.assertIsNotNone(g)
        self.assertEqual(g.name, "green")
        self.assertEqual(g.type, Types.Boolean)
        self.assertIsNone(g.default)
        self.assertIsNone(g.value)
        g.value = 0
        self.assertIsNone(g.default)
        self.assertEqual(g.value, False)
        self.assertEqual(args.boolean("green"), False)
        # blue
        b = args.get(2)
        self.assertIsNotNone(b)
        self.assertEqual(b.name, "blue")
        self.assertEqual(b.type, Types.Text)
        self.assertIsNone(b.default)
        # Log.debug(f"B: {b}; {type(b)}")
        self.assertIsNone(b.value)
        b.value = "something else"
        self.assertIsNone(b.default)
        self.assertEqual(b.value, "something else")
        self.assertEqual(args.string("blue"), "something else")
        # cyan
        c = args.get("cyan")
        self.assertIsNotNone(b)
        self.assertEqual(c.name, "cyan")
        self.assertEqual(c.type, Types.Int16s)
        self.assertIsNone(c.default)
        self.assertIsNone(c.value)
        c.value = 1025
        self.assertIsNone(c.default)
        self.assertEqual(c.value, 1025)
        self.assertEqual(args.integer("cyan"), 1025)

    def testParse(self):
        Log.test("\nTest Parse")
        args = Arguments()
        args.dashed.add("cyan", "c", Types.Int16s)
        args.fixed.add("red", Types.Real)
        args.dashed.add("yellow", "y", Types.Int16u)
        args.dashed.add("margenta", "ma", Types.Binary)
        args.fixed.add("green", Types.Boolean)
        args.dashed.add("orange", "o", Types.Flag)
        args.fixed.add("blue", Types.Text)
        args.parse([ "-ma", "abcdef123456", "123.45", "--orange", "true", "-c", "-3", "----yellow", "456", "Sky" ])
        self.assertEqual(args.real("red"), 123.45)
        self.assertEqual(args.boolean("green"), True)
        self.assertEqual(args.string("blue"), "Sky")
        self.assertEqual(args.integer("c"), -3)
        self.assertEqual(args.integer("yellow"), 456)
        self.assertEqual(args.boolean("o"), True)


if __name__ == "__main__":
    unittest.main()
