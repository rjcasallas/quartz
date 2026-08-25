# MainCommand module.
from quartz.args import Arguments, Types
from quartz.log import Log
from typing import Optional, Dict, List
from abc import ABC
import os
import shlex
import sys
import readline


# Abstract command class with execute method.
class Command(ABC):

    class Children:

        def __init__(self, _parent: "Command"):
            if not isinstance(_parent, Command):
                Error.invalid(f"Invalid parent", _parent)
            self._parent = _parent
            self._commands = {}
            self._aliases = {}

        def __len__(self):

            return len(self._commands)

        def __getitem__(self, name: str) -> "Command":
            return self._commands[name]

        def __str__(self) -> str:
            commands = [f"{name}" for name, cmd in self._commands.items()]
            return ", ".join(commands)

        def clear(self):
            self._commands = {}

        def add(self, x: str, cmd: "Command") -> None:
            # command
            if not isinstance(cmd, Command):
                Error.invalid(f"Invalid command", cmd)
            # name/alias
            if isinstance(x, str):
                self._commands[x] = cmd
            elif isinstance(x, (tuple, list)):
                self._commands[x[0]] = cmd
                for a in x[1:]:
                    self._aliases[a] = cmd
            else:
                Error.invalid(f"Invalid command name/alias", x)
            # parent
            cmd._parent = self._parent
            cmd.args.parent = self._parent.args

        def get(self, x: str) -> Optional["Command"]:
            if x in self._commands:
                return self._commands[x]
            elif x in self._aliases:
                return self._aliases[x]

        def has(self, name: str) -> bool:
            return name in self._commands

        def to_dict(self) -> Dict[str, "Command"]:
            return self._commands.copy()

    def __init__(self, title: str, hidden: bool = False):
        self._title = title
        self._hidden = hidden
        self._parent = None
        self._args = Arguments()
        self._children = Command.Children(self)
        self._running = True

    def __str__(self) -> str:
        return f"{self._title}({self._children})"

    @property
    def hidden(self) -> bool:
        return self._hidden

    @property
    def parent(self) -> "Command":
        return self._parent

    @property
    def commands(self) -> "Command.Children":
        return self._children

    @property
    def args(self) -> Arguments:
        return self._args

    def run(self, argv: List[str]) -> None:
        self.clear()
        self.builtin()
        self.setup()

        # Check if the first argument matches a child command name
        if len(argv) > 0:
            child = self.commands.get(argv[0])
            if child:
                # Remove the first argument and execute run in the child command
                return child.run(argv[1:])
        # Otherwise parse arguments
        self.args.parse(argv)
        # Execute
        if self.args.boolean("help"):
            self.help()
        else:
            self.execute()

    def clear(self):
        self.args.clear()
        self._children.clear()

    def builtin(self) -> None:
        pass

    def setup(self) -> None:
        pass

    def execute(self) -> None:
        self.print(0)

    def print(self, level: int = 0) -> None:
        Log.list(f"{self._title}", level, "‣")
        # Commands
        self._printCommands(level + 1)
        # Arguments
        self.args.print(level + 1)

    def help(self) -> None:
        Log.list(f"{self._title}", 0, "﹖")
        self._help(1)

    def _printCommands(self, level: int = 0) -> None:
        # Subcommands
        children = self.commands.to_dict()
        for name, cmd in children.items():
            if not cmd.hidden:
                Log.list(f"{name}", level, "✱")

    def _help(self, level: int = 0) -> None:
        # Commands
        self._printCommands(level)
        # Arguments
        self.args.help(level)

    def _exit(self) -> None:
        self._running = False


class HelpCommand(Command):

    def execute(self):
        self.parent.help()


class ExitCommand(Command):

    def execute(self):
        if self.parent:
            self.parent._exit()
        else:
            self._exit()


class BasicCommand(Command):

    def __init__(self, title: str, hidden: bool = False):
        super().__init__(title, hidden)

    def builtin(self) -> None:
        # Build-in
        self.commands.add(["help", "h"], HelpCommand(self._title, hidden=True))
        self.commands.add(["exit", "x"], ExitCommand("Exit", hidden=True))
        self.args.dashed.add(
            "help",
            "h",
            Types.Flag,
            False,
            "Show help",
            hidden=(self.parent is not None),
        )


class MainCommand(BasicCommand):

    def __init__(self, title: str, version: str):
        super().__init__(title)
        self._version = version

    def run(self, argv: List[str] = None) -> None:
        super().run(sys.argv[1:] if argv is None else argv)

    def execute(self):
        Log.list(f"\n{self._title}", 0, "◆")

    def help(self) -> None:
        self._help(1)


class VersionCommand(Command):

    def execute(self):
        Log.list(f"Version {self.parent._version}", 1, "‣")


class BasicApp(MainCommand):

    def __init__(self, title: str, version: str):
        super().__init__(title, version)
        self._command = self
        self._prompt = "> "

    @property
    def prompt(self):
        return self._prompt

    @prompt.setter
    def prompt(self, prompt):
        self._prompt = prompt

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, command):
        self._command = command

    def builtin(self) -> None:
        super().builtin()
        self.commands.add(["version", "v"], VersionCommand("Version"))
        self.args.dashed.add("version", "v", Types.Flag, False, "Show version")

    def execute(self):
        super().execute()
        if self.args["version"].boolean():
            return self.commands["version"].execute()
        history_file = os.path.expanduser("~/.quartz/history")
        # Log.list(history_file, 0, '💾')
        try:
            os.makedirs(os.path.dirname(history_file), exist_ok=True)
            readline.read_history_file(history_file)
        except OSError:
            pass
        while self._running:
            try:
                line = input(self.prompt).strip()
                if not line:
                    continue
                if line in ("quit", "q"):
                    break
                argv = shlex.split(line)
                self.command.run(argv)
            except EOFError:
                break
            except KeyboardInterrupt:
                print()
                continue
            except ValueError as e:
                Log.error(str(e))
        try:
            readline.write_history_file(history_file)
        except OSError:
            pass
