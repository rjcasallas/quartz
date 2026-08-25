# Main entry point for the application.
from quartz.app import MainCommand
import db.commands as _db


class GeneratorApp(MainCommand):

    def __init__(self):
        super().__init__("Generator", "1.0.0")

    def setup(self) -> None:
        self.commands.add(["sql", "s"], _db.QueriesCommand())


if __name__ == "__main__":
    app = GeneratorApp()
    app.run()
