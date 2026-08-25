# Main entry point for the application.
import sys
import os
from quartz.app import BasicApp, BasicCommand, Types
from quartz.log import Log


class RedCommand(BasicCommand):

    def setup(self) -> None:
        self.args.dashed.add("color", "c", Types.Int8u, 0)
        self.args.fixed.add("fruit", Types.Text, "tomato")
        self.args.dashed.add("boo", "b", Types.Boolean, True)
        self.args.fixed.add("size", Types.Text, "big")

    def execute(self):
        super().execute()
        Log.list(f"count: {self.args['count']}", 1, "◦")
        Log.list(f"name: {self.args['name']}", 1, "◦")
        self.args["count"] = 123
        self.args["name"] = "Apple"
        Log.list(f"name: {self.args['name']}", 1, "+")
        Log.list(f"count: {self.args['count']}", 1, "+")


class BlueCommand(BasicCommand):

    def setup(self) -> None:
        self.args.dashed.add("flag", "f", Types.Flag)
        self.args.dashed.add("object", "j", Types.Text, "sky")

    def execute(self):
        super().execute()
        Log.list(f"count: {self.args['count']}", 1, "◦")
        Log.list(f"name: {self.args['name']}", 1, "◦")
        self.args.set("count", 321).set("name", "Sky")
        Log.list(f"count: {self.args['count']}", 1, "+")
        Log.list(f"name: {self.args['name']}", 1, "+")


class ExampleApp(BasicApp):

    def __init__(self):
        super().__init__("Example", "1.0.0")

    def setup(self) -> None:
        self.commands.add(["red", "r"], RedCommand("Red"))
        self.commands.add(["blue", "b"], BlueCommand("Blue"))
        self.args.dashed.add("count", "c", Types.Int16u, 10)
        self.args.dashed.add("name", "n", Types.Text, "Foo Choo")


if __name__ == "__main__":
    app = ExampleApp()
    app.run()
