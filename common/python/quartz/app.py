from quartz.args import Arguments, Types
from quartz.log import Log
from quartz.error import Error
from abc import ABC, abstractmethod
import sys, os, readline, shlex


class Command(ABC):

    def __init__(self, title:str, hidden:bool=False):
        self._title = title
        self._hidden = hidden
        self._parent = None
        self._children = CommandSet(self)
        self._args = Arguments()
        self._args._tag = title
        self._needs_init = True

    @property
    def title(self) -> str:
        return self._title

    @property
    def hidden(self) -> bool:
        return self._hidden

    @property
    def parent(self) -> Command:
        return self._parent
    @parent.setter
    def parent(self, c:Command):
        if not isinstance(c, Command):
            Error.invalid("parent command", c)
        self._parent = c
        self._args.parent = c._args

    @property
    def commands(self) -> list[Command]:
        return self._children

    @property
    def args(self) -> Arguments:
        return self._args

    def setup(self):
        pass

    def clear(self):
        self.commands.clear()
        self.args.clear()

    def execute(self):
        self.print()

    def run(self, args:list[str]):
        # Prepare
        self._setup()
        # Check for sub-commands
        if len(args) > 0:
            child = self.commands.find(args[0])
            if child is not None:
                # Run sub-command
                return child.run(args[1:])
        # Parse actual arguments
        self.args.parse(args)
        # Execute
        self._execute()

    def help(self, level:int=0):
        Log.list(f"{self._title}", 0, "﹖")
        self.commands.print(level + 1)
        self.args.help(level + 1)
        exit(0)

    def print(self, level:int=0):
        Log.list(f"{self.title}", level, "‣")
        self.commands.print(level + 1)

    def _setup(self):
        if self._needs_init:
            self.clear()
            self.setup()
            self._needs_init = False

    def _execute(self):
        self.execute()


class CommandSet:

    def __init__(self, parent):
        self._parent = parent
        self._commands = {}
        self._aliases = {}

        def __len__(self):
            return len(self._commands)

        def __getitem__(self, alias:str) -> Command:
            return self.get(alias)

    def add(self, alias:str, cmd:Command):
        if not isinstance(cmd, Command):
            Error.invalid("command", cmd)
        cmd.parent = self._parent
        if isinstance(alias, str):
            self._commands[alias] = cmd
        elif isinstance(alias, (tuple, list)):
            self._commands[alias[0]] = cmd
            for a in alias[1:]:
                self._aliases[a] = cmd
        else:
            Error.invalid(f"command alias", alias)

    def get(self, alias:str) -> Command:
        c = self.find(alias)
        if c is None:
            Error.missing(f'command "{alias}"')
        return c

    def find(self, alias:str) -> Command:
        if alias in self._commands:
            return self._commands[alias]
        elif alias in self._aliases:
            return self._aliases[alias]

    def clear(self):
        self._commands = {}

    def print(self, level:int=0):
        for name, cmd in self._commands.items():
            if not cmd.hidden:
                Log.list(f"{name}", level, "✱")


class HelpCommand(Command):

    def execute(self):
        self.parent.help()


class ExitCommand(Command):

    def execute(self):
        exit(0)


class BasicCommand(Command):

    def _setup(self):
        super()._setup()
        self.commands.add(["help", "h"], HelpCommand(self.title, hidden=True))
        self.commands.add(["exit", "x"], ExitCommand("Exit", hidden=True))
        self.args.dashed.add("help", "h", Types.Flag, False, hidden=True)

    def _execute(self):
        if self.args.boolean("help"):
            self.help()
        else:
            self.execute()

    def execute(self):
        Log.list(f"\n{self._title}", 0, "◆")
        self.args.print(1)


class VersionCommand(Command):

    def __init__(self, title:str, version:str):
        super().__init__(title)
        self._version = version

    def execute(self):
        Log.list(f"{self.parent.title} v{self._version}", 1, "‣")


class MainCommand(BasicCommand):

    def __init__(self, title:str, version:str):
        super().__init__(title)
        self._version = version

    def _setup(self):
        super()._setup()
        self.commands.add(["version", "v"], VersionCommand("Version", self.version))
        self.args.dashed.add("version", "v", Types.Flag, False)

    def _execute(self):
        if self.args.boolean("help"):
            self.help()
        elif self.args.boolean("version"):
            self.commands.get("version").execute()
        else:
            self.execute()

    @property
    def version(self) -> str:
        return self._version

    def run(self, args:list[str]=None):
        super().run(sys.argv[1:] if args is None else args)


class BasicApp(MainCommand):

    def __init__(self, title, version):
        super().__init__(title, version)
        self._prompt = ">"
        self._command = self
        self._interactive = False

    @property
    def prompt(self):
        return self._prompt
    @prompt.setter
    def prompt(self, p):
        self._prompt = p.strip()

    @property
    def command(self):
        return self._command
    @command.setter
    def command(self, c):
        if not isinstance(c, Command):
            Error.invalid("command", c)
        self._command = c

    def execute(self):
        if self._interactive:
            # Already interactive
            return super().execute()
        else:
            self._interactive = True
        history_file = os.path.expanduser("~/.quartz/history")
        # Log.list(history_file, 0, '💾')
        try:
            os.makedirs(os.path.dirname(history_file), exist_ok=True)
            readline.read_history_file(history_file)
        except OSError:
            pass

        while True:
            try:
                line = input(f"{self.prompt} ").strip()
                if not line:
                    continue
                if line in ("quit", "q"):
                    break
                args = shlex.split(line)
                self.command.run(args) # FIXME: Clears the command-line arguments
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
