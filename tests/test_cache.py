import unittest

from parameterized import parameterized

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


class TestUndoRedo(unittest.TestCase):

    def setUp(self):
        self.cache = Cache()

    @parameterized.expand([
        ("undo", 1, 0),
        ("nothing_to_undo", -1, -1),
        ("only_one_action", 0, 0)
    ])
    def test_undo(self, name, current, expected):
        self.cache.current = current
        self.cache.undo()
        self.assertEqual(self.cache.current, expected)

    @parameterized.expand([
        ("redo", 0, ["foo", "bar"], 1),
        ("nothing_to_redo", 1, ["foo", "bar"], 1)
    ])
    def test_redo(self, name, current, items, expected):
        self.cache.current = current
        self.cache.items = items
        self.cache.redo()
        self.assertEqual(self.cache.current, expected)
