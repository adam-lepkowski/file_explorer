import unittest

from cache import Cache


class TestStore(unittest.TestCase):

    def setUp(self):
        self.cache = Cache()

    def test_store(self):
        self.cache.store("foo")
        self.assertEqual(0, self.cache.current)
        self.assertEqual(["foo"], self.cache.items)

    def test_store_clear_actions_ahead(self):
        self.cache.items = ["foo", "bar", "foobar"]
        self.cache.store("barfoo")
        self.assertEqual(0, self.cache.current)
        self.assertEqual(["barfoo"], self.cache.items)
