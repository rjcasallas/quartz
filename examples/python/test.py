import unittest
from unittest.mock import Mock, patch
from quartz.log import Log

unittest.TestLoader.sortTestMethodsUsing = None


class TestBase:

    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestA(TestBase, unittest.TestCase):

    def test1(self):
        Log.test("\nTest A")
        x = 1
        y = x
        self.assertEqual(x, y)

    def test2(self):
        Log.test("\nTest B")
        x = 1
        y = x + 1
        self.assertNotEqual(x, y)


if __name__ == "__main__":
    unittest.main()
