import unittest
from unittest.mock import patch
from pathlib import Path

from parameterized import parameterized

from explorer import Facade


class TestGetDefaultDir(unittest.TestCase):

    def setUp(self):
        self.facade = Facade()

    def test_get_default_dir(self):
        result = self.facade.get_default_dir()
        self.assertTrue(isinstance(result, Path))


class TestGetContent(unittest.TestCase):

    def setUp(self):
        self.facade = Facade()
        self.content = {
            "dirs": [Path("dir1")],
            "files": [Path("file1.py")]
        }

    @patch("explorer.facade.os.path.getmtime", return_value=1)
    @patch("explorer.facade.FileExplorer.get_content")
    def test_get_content(self, mock_explorer, mock_getmtime):
        mock_explorer.return_value = self.content
        expected = [
            ("dir1", "1970/01/01 01:00:01", "dirs"),
            ("file1.py", "1970/01/01 01:00:01", "files")
        ]
        result = self.facade.get_content("foo/bar")
        self.assertEqual(expected, result)


class TestGetParent(unittest.TestCase):

    def setUp(self):
        self.facade = Facade()

    @parameterized.expand([
        ("regular_path", r"C:\Users", Path("C:/")),
        ("root", "C:", Path("C:"))
    ])
    def test_get_parent(self, name, path, expected):
        result = self.facade.get_parent(path)
        self.assertEqual(expected, result)

    def test_get_parent_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            self.facade.get_parent("foo/bar")


class TestCopy(unittest.TestCase):

    def setUp(self):
        self.facade = Facade()

    @patch("explorer.facade.Path.exists", return_value=True)
    def test_copy(self, exists_mock):
        directory = "foo"
        name = "bar.py"
        self.facade.copy(directory, name)
        result = self.facade.current_obj
        expected = Path("foo/bar.py")
        self.assertEqual(expected, result)

    def test_copy_raises(self):
        with self.assertRaises(FileNotFoundError):
            self.facade.copy("foo", "bar.py")


class TestPaste(unittest.TestCase):

    def setUp(self):
        self.facade = Facade()

    @patch("explorer.facade.FileExplorer.copy")
    def test_paste_with_current_obj(self, copy_mock):
        self.facade.current_obj = {
            "src": "src/foo/bar",
            "func": "copy"
        }
        self.facade.paste("dst/foo/bar")
        copy_mock.assert_called_with("src/foo/bar", "dst/foo/bar")

    @patch("explorer.facade.FileExplorer.copy")
    def test_paste_no_current_obj(self, copy_mock):
        self.facade.paste("dst/foo/bar")
        copy_mock.assert_not_called()


class TesStoreSrc(unittest.TestCase):

    def setUp(self):
        self.facade = Facade()

    @patch("explorer.facade.Path.exists", return_value=True)
    def test_copy(self, exists_mock):
        directory = "foo"
        name = "bar.py"
        self.facade.store_src(directory, name, "copy")
        result = self.facade.current_obj
        expected = {
            "src": Path("foo/bar.py"),
            "func": "copy"
        }
        self.assertEqual(expected, result)

    def test_copy_raises(self):
        with self.assertRaises(FileNotFoundError):
            self.facade.store_src("foo", "bar.py", "copy")
