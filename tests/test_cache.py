import unittest

from cache import Cache


class TestStore(unittest.TestCase):

    def setUp(self):
        self.cache = Cache()

    def test_store(self):
        self.cache.store("foo")
        self.assertEqual(0, self.cache.current)
        self.assertEqual(["foo"], self.cache.items)
