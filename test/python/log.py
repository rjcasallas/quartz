import unittest
from unittest.mock import Mock, patch
from quartz.log import Log, Logger, PrettyLogger

unittest.TestLoader.sortTestMethodsUsing = None


class TestLog(unittest.TestCase):

    def setUp(self):
        pass

    def test_debug(self):
        Log.test("\nTest Debug")
        Log.debug("Message")

    def test_info(self):
        Log.test("\nTest Info")
        Log.info("Message")

    def test_warning(self):
        Log.test("\nTest Warning")
        Log.warning("Message")

    def test_error(self):
        Log.test("\nTest Error")
        Log.error("Message")

    def test_list(self):
        Log.test("\nTest List")
        Log.list("Level 0", 0)
        Log.list("Level 1", 1)
        Log.list("Level 2", 2)
        Log.list("Level 3", 3)
        Log.list("Level 4", 4)
        Log.list("Level 5", 5)
        Log.list("Level 6", 6)


if __name__ == "__main__":
    unittest.main()
