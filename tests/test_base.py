import unittest
from src.cumulator.base import Cumulator


class TestBase(unittest.TestCase):
    def test_run(self):
        cumulator = Cumulator()

        # Test without parameters
        def foo():
            return 1

        output = cumulator.run(foo)
        self.assertEqual(1, output)

        # Tests with arguments
        def foo(x, y=1):
            return x*y

        # (only positional)
        output = cumulator.run(foo, 3)
        self.assertEqual(3, output)

        # (both)
        output = cumulator.run(foo, 3, y=2)
        self.assertEqual(6, output)


if __name__ == '__main__':
    unittest.main()
