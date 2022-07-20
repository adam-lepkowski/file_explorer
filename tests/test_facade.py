import unittest
from pathlib import Path

from explorer import Facade


class TestGetDefaultDir(unittest.TestCase):

    def setUp(self):
        self.facade = Facade()

    def test_get_default_dir(self):
        result = self.facade.get_default_dir()
        self.assertTrue(isinstance(result, Path))
