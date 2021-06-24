import unittest
import Inkscape as sut


@unittest.skip("Don't forget to test!")
class InkscapeTests(unittest.TestCase):

    def test_example_fail(self):
        result = sut.Inkscape_example()
        self.assertEqual("Happy Hacking", result)
