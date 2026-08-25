# Tests for the app module.
import unittest
from unittest.mock import patch

from quartz.app import Command, MainCommand, BasicCommand, BasicApp
from quartz.args import Types


class DummyCommand(Command):

    def __init__(self, title="Dummy", hidden=False):
        super().__init__(title, hidden)
        self.executed = False
        self.help_called = False
        self.setup_called = False
        self.builtin_called = False

    def builtin(self):
        self.builtin_called = True

    def setup(self):
        self.setup_called = True

    def execute(self):
        self.executed = True

    def help(self):
        self.help_called = True


class ChildReadyCommand(DummyCommand):

    def __init__(self):
        super().__init__("Parent")
        self.child = DummyCommand("Child")

    def setup(self):
        self.commands.add("child", self.child)


class ArgsReadyCommand(DummyCommand):

    def setup(self):
        self.setup_called = True
        self.args.dashed.add("help", "h", Types.Flag, False)
        self.args.dashed.add("verbose", "v", Types.Boolean)
        self.args.fixed.add("file", Types.Text)


class TestCommandChildren(unittest.TestCase):

    def setUp(self):
        self.parent = DummyCommand("Parent")
        self.children = Command.Children(self.parent)

    def test_add_and_get_command(self):
        child = DummyCommand("Child")
        self.children.add("child", child)

        self.assertEqual(len(self.children), 1)
        self.assertIs(self.children.get("child"), child)
        self.assertTrue(self.children.has("child"))
        self.assertIs(child.parent, self.parent)
        self.assertIs(child.args.parent, self.parent.args)

    def test_add_with_aliases(self):
        child = DummyCommand("Child")
        self.children.add(["child", "c", "ch"], child)

        self.assertIs(self.children.get("child"), child)
        self.assertIs(self.children.get("c"), child)
        self.assertIs(self.children.get("ch"), child)

    def test_to_dict_returns_copy(self):
        self.children.add("one", DummyCommand("One"))
        copied = self.children.to_dict()
        copied["two"] = DummyCommand("Two")
        self.assertFalse(self.children.has("two"))


class TestCommand(unittest.TestCase):

    def test_run_executes_after_setup_and_parse(self):
        cmd = ArgsReadyCommand("Cmd")
        cmd.run(["--verbose", "true", "out.txt"])

        self.assertTrue(cmd.builtin_called)
        self.assertTrue(cmd.setup_called)
        self.assertTrue(cmd.executed)
        self.assertTrue(cmd.args.get("verbose").value)
        self.assertEqual(cmd.args.get("file").value, "out.txt")

    def test_run_dispatches_child_command(self):
        cmd = ChildReadyCommand()

        with patch.object(cmd.child, "run") as child_run:
            cmd.run(["child", "--x"])
            child_run.assert_called_once_with(["--x"])

    def test_run_calls_help_when_help_flag_true(self):
        class HelpReady(BasicCommand):
            def __init__(self):
                super().__init__("HelpReady")
                self.executed = False
                self.help_called = False

            def execute(self):
                self.executed = True

            def help(self):
                self.help_called = True

        cmd = HelpReady()
        cmd.run(["--help"])

        self.assertTrue(cmd.help_called)
        self.assertFalse(cmd.executed)

    def test_print_writes_title(self):
        cmd = DummyCommand("Printer")
        with patch("quartz.app.Log.list") as mock_list:
            cmd.print(0)
            self.assertGreaterEqual(mock_list.call_count, 1)


class TestMainCommand(unittest.TestCase):

    def setUp(self):
        self.main = MainCommand("TestApp", "1.0.0")

    @patch("sys.argv", ["prog", "--help"])
    def test_run_uses_sys_argv_when_none(self):
        with patch.object(self.main, "help") as help_call:
            self.main.run(None)
            help_call.assert_called_once()

    def test_help_delegates_to_internal_help(self):
        with patch.object(self.main, "_help") as internal_help:
            self.main.help()
            internal_help.assert_called_once_with(1)


class TestBasicCommand(unittest.TestCase):

    def test_builtin_registers_help_and_exit(self):
        cmd = BasicCommand("Base")
        cmd.builtin()

        self.assertIsNotNone(cmd.commands.get("help"))
        self.assertIsNotNone(cmd.commands.get("h"))
        self.assertIsNotNone(cmd.commands.get("exit"))
        self.assertIsNotNone(cmd.commands.get("x"))
        self.assertIsNotNone(cmd.args.find("help"))


class TestBasicApp(unittest.TestCase):

    def setUp(self):
        self.app = BasicApp("Quartz", "2.0.0")

    def test_prompt_property(self):
        self.assertEqual(self.app.prompt, "> ")
        self.app.prompt = "quartz> "
        self.assertEqual(self.app.prompt, "quartz> ")

    def test_version_flag_executes_version_command(self):
        with patch.object(
            self.app.commands, "__getitem__", wraps=self.app.commands.__getitem__
        ) as _:
            with patch("quartz.app.Log.list") as mock_list:
                self.app.run(["--version"])
                calls = [str(c) for c in mock_list.call_args_list]
                self.assertTrue(any("Version 2.0.0" in c for c in calls))


if __name__ == "__main__":
    unittest.main()
