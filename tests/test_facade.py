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


class TestPaste(unittest.TestCase):

    def setUp(self):
        self.facade = Facade()

    @patch("explorer.facade.FileExplorer.copy")
    def test_paste_single_obj(self, copy_mock):
        self.facade.current_obj = [{"src": "src/foo/bar", "func": "copy"}]
        self.facade.paste("dst/foo/bar")
        copy_mock.assert_called_with("src/foo/bar", "dst/foo/bar")

    @patch("explorer.facade.FileExplorer.copy")
    def test_paste_multiple_obj(self, copy_mock):
        self.facade.current_obj = [
            {"src": "src/foo/bar", "func": "copy"},
            {"src": "src/foo/bar", "func": "copy"}
        ]
        self.facade.paste("dst/foo/bar")
        self.assertEqual(copy_mock.call_count, 2)

    @patch("explorer.facade.FileExplorer.copy")
    def test_paste_no_current_obj(self, copy_mock):
        self.facade.paste("dst/foo/bar")
        copy_mock.assert_not_called()

    @patch("explorer.facade.FileExplorer.copy", return_value="dst/foo/bar/bar")
    def test_paste_cache_item(self, copy_mock):
        self.facade.current_obj = [{"src": "src/foo/bar", "func": "copy"}]
        self.facade.paste("dst/foo/bar")
        expected = [{
            "src": "src/foo/bar",
            "func": "copy",
            "dst": Path("dst/foo/bar"),
            "new_obj": "dst/foo/bar/bar"
        }]
        result = self.facade.cache.items[0]
        self.assertEqual(expected, result)


class TestStoreSrc(unittest.TestCase):

    def setUp(self):
        self.facade = Facade()

    @patch("explorer.facade.Path.exists", return_value=True)
    def test_copy(self, exists_mock):
        objs = {
            "parent": "foo",
            "names": ["bar.py", "foo_bar.py"],
            "func": "copy"
        }
        self.facade.store_src(objs)
        result = self.facade.current_obj
        expected = [
            {"src": Path("foo/bar.py"), "func": "copy"},
            {"src": Path("foo/foo_bar.py"), "func": "copy"}
        ]
        self.assertEqual(expected, result)

    def test_copy_raises(self):
        objs = {
            "parent": "foo",
            "names": ["bar.py", "foo_bar.py"],
            "func": "copy"
        }
        with self.assertRaises(FileNotFoundError):
            self.facade.store_src(objs)


class TestTransfer(unittest.TestCase):

    def setUp(self):
        self.facade = Facade()
        self.objs = {
            "src": "src/foo",
            "names": ["bar.py"],
            "dst": "dst/foo/bar",
        }

    @patch("explorer.facade.FileExplorer.copy")
    def test_transfer_copy(self, copy_mock):
        self.objs["func"] = "copy"
        self.facade.transfer(self.objs)
        copy_mock.assert_called_with(Path("src/foo/bar.py"), "dst/foo/bar")

    @patch("explorer.facade.FileExplorer.copy")
    def test_transfer_copy_multiple(self, copy_mock):
        self.objs["func"] = "copy"
        self.objs["names"].append("foo.py")
        self.facade.transfer(self.objs)
        self.assertEqual(copy_mock.call_count, 2)

    @patch("explorer.facade.FileExplorer.move")
    def test_transfer_move(self, move_mock):
        self.objs["func"] = "move"
        self.facade.transfer(self.objs)
        move_mock.assert_called_with(Path("src/foo/bar.py"), "dst/foo/bar")

    @patch("explorer.facade.FileExplorer.move", return_value="dst/foo/bar/bar.py")
    def test_transfer_cache_item(self, copy_mock):
        self.objs["func"] = "move"
        self.facade.transfer(self.objs)
        expected = {
            "src": Path("src/foo/bar.py"),
            "func": "move",
            "dst": Path("dst/foo/bar"),
            "new_obj": "dst/foo/bar/bar.py"
        }
        result = self.facade.cache.items[0][0]
        self.assertEqual(expected, result)


class TestRename(unittest.TestCase):

    def setUp(self):
        self.facade = Facade()
        self.src = "src/foo"
        self.name = "bar.py"

    @patch("explorer.facade.Path.exists", return_value=True)
    @patch("explorer.facade.FileExplorer.rename")
    def test_transfer_copy(self, rename_mock, exists_mock):
        src = Path(self.src) / self.name
        dst = Path(self.src) / "foo_bar"
        self.facade.rename(self.src, self.name, "foo_bar")
        rename_mock.assert_called_with(src, dst)


class TestDelete(unittest.TestCase):

    def setUp(self):
        self.facade = Facade()
        self.objs = {
            "parent": "src/foo",
            "names": ["bar.py"],
        }

    @patch("explorer.facade.Path.exists", return_value=True)
    @patch("explorer.facade.FileExplorer.rm")
    def test_delete(self, rm_mock, exists_mock):
        self.facade.delete(self.objs)
        rm_mock.assert_called_with(Path("src/foo/bar.py"))

    @patch("explorer.facade.Path.exists", return_value=True)
    @patch("explorer.facade.FileExplorer.rm")
    def test_delete_multiple(self, rm_mock, exists_mock):
        self.objs["names"].append("foo.py")
        self.facade.delete(self.objs)
        self.assertEqual(rm_mock.call_count, 2)


class TestUndo(unittest.TestCase):

    def setUp(self):
        self.facade = Facade()
        self.prev_action = {
            "src": Path("src/foo/foo_bar.py"),
            "new_obj": Path("dst/foo/bar/foo_bar.py")
        }

    @patch("explorer.facade.FileExplorer.rm")
    @patch("explorer.facade.Cache.undo")
    @patch("explorer.facade.Cache.get_current")
    def test_undo_copy(self, get_current_mock, undo_mock, rm_mock):
        self.prev_action["func"] = "copy"
        get_current_mock.return_value = [self.prev_action]
        self.facade.undo()
        get_current_mock.assert_called_once()
        rm_mock.assert_called_with(self.prev_action["new_obj"])
        undo_mock.assert_called_once()

    @patch("explorer.facade.FileExplorer.rename")
    @patch("explorer.facade.FileExplorer.move")
    @patch("explorer.facade.Cache.undo")
    @patch("explorer.facade.Cache.get_current")
    def test_undo_move_src_not_renamed(self, get_current_mock, undo_mock,
                                       move_mock, rename_mock):
        self.prev_action["func"] = "move"
        get_current_mock.return_value = [self.prev_action]
        self.facade.undo()
        get_current_mock.assert_called_once()
        move_mock.assert_called_with(
            self.prev_action["new_obj"], self.prev_action["src"].parent
        )
        undo_mock.assert_called_once()
        rename_mock.assert_not_called()

    @patch("explorer.facade.FileExplorer.rename")
    @patch("explorer.facade.FileExplorer.move")
    @patch("explorer.facade.Cache.undo")
    @patch("explorer.facade.Cache.get_current")
    def test_undo_move_src_renamed(self, get_current_mock, undo_mock,
                                   move_mock,rename_mock):
        self.prev_action["func"] = "move"
        self.prev_action["src"] = Path("src/foo/bar.py")
        get_current_mock.return_value = [self.prev_action]
        move_mock.return_value = Path("src/foo/foo_bar.py")
        self.facade.undo()
        get_current_mock.assert_called_once()
        undo_mock.assert_called_once()
        rename_mock.assert_called_with(Path("src/foo/foo_bar.py"), "bar")

    @patch("explorer.facade.FileExplorer.rename")
    @patch("explorer.facade.Cache.undo")
    @patch("explorer.facade.Cache.get_current")
    def test_undo_rename(self, get_current_mock, undo_mock, rename_mock):
        self.prev_action["func"] = "rename"
        self.prev_action["new_obj"] = Path("src/foo/bar_foo.py")
        get_current_mock.return_value = [self.prev_action]
        self.facade.undo()
        get_current_mock.assert_called_once()
        undo_mock.assert_called_once()
        rename_mock.assert_called_with(Path("src/foo/bar_foo.py"), "foo_bar")

    @patch("explorer.facade.FileExplorer.rm")
    @patch("explorer.facade.Cache.undo")
    @patch("explorer.facade.Cache.get_current")
    def test_undo_sets_last_undo(self, get_current_mock, undo_mock, rm_mock):
        self.prev_action["func"] = "copy"
        get_current_mock.return_value = [self.prev_action]
        self.facade.undo()
        self.assertEqual(self.facade.last_undo, [self.prev_action])

    @patch("explorer.facade.FileExplorer.rm")
    @patch("explorer.facade.Cache.undo")
    @patch("explorer.facade.Cache.get_current")
    def test_undo_clears_last_redo(self, get_current_mock, undo_mock, rm_mock):
        self.prev_action["func"] = "copy"
        get_current_mock.return_value = [self.prev_action]
        self.facade.last_redo = "foo_bar"
        self.facade.undo()
        self.assertIsNone(self.facade.last_redo)

    @patch("explorer.facade.FileExplorer.rm")
    @patch("explorer.facade.Cache.undo")
    @patch("explorer.facade.Cache.get_current")
    def test_cant_undo_same_action(self, get_current_mock, undo_mock, rm_mock):
        self.prev_action["func"] = "copy"
        get_current_mock.return_value = [self.prev_action]
        self.facade.last_undo = [self.prev_action]
        self.facade.undo()
        rm_mock.assert_not_called()


class TestRedo(unittest.TestCase):

    def setUp(self):
        self.facade = Facade()
        self.prev_action = {
            "src": Path("src/foo/foo_bar.py"),
            "dst": Path("dst/foo/foo_bar.py")
        }

    @patch("explorer.facade.FileExplorer.copy")
    @patch("explorer.facade.Cache.redo")
    @patch("explorer.facade.Cache.get_current")
    def test_redo_copy(self, get_current_mock, redo_mock, copy_mock):
        self.prev_action["func"] = "copy"
        get_current_mock.return_value = [self.prev_action]
        self.facade.redo()
        get_current_mock.assert_called_once()
        copy_mock.assert_called_with(
            self.prev_action["src"], self.prev_action["dst"]
        )
        redo_mock.assert_called_once()

    @patch("explorer.facade.FileExplorer.move")
    @patch("explorer.facade.Cache.redo")
    @patch("explorer.facade.Cache.get_current")
    def test_redo_move(self, get_current_mock, redo_mock, move_mock):
        self.prev_action["func"] = "move"
        get_current_mock.return_value = [self.prev_action]
        self.facade.redo()
        get_current_mock.assert_called_once()
        move_mock.assert_called_with(
            self.prev_action["src"], self.prev_action["dst"]
        )
        redo_mock.assert_called_once()

    @patch("explorer.facade.FileExplorer.rename")
    @patch("explorer.facade.Cache.redo")
    @patch("explorer.facade.Cache.get_current")
    def test_redo_rename(self, get_current_mock, redo_mock, rename_mock):
        self.prev_action["func"] = "rename"
        get_current_mock.return_value = [self.prev_action]
        self.facade.redo()
        get_current_mock.assert_called_once()
        rename_mock.assert_called_with(
            self.prev_action["src"], self.prev_action["dst"]
        )
        redo_mock.assert_called_once()

    @patch("explorer.facade.FileExplorer.rename")
    @patch("explorer.facade.Cache.redo")
    @patch("explorer.facade.Cache.get_current")
    def test_redo_sets_last_redo(self, get_curr_mock, redo_mock, rename_mock):
        self.prev_action["func"] = "rename"
        get_curr_mock.return_value = [self.prev_action]
        self.facade.redo()
        self.assertEqual(self.prev_action, self.facade.last_redo)

    @patch("explorer.facade.FileExplorer.rename")
    @patch("explorer.facade.Cache.redo")
    @patch("explorer.facade.Cache.get_current")
    def test_redo_sets_last_redo(self, get_curr_mock, redo_mock, rename_mock):
        self.prev_action["func"] = "rename"
        get_curr_mock.return_value = [self.prev_action]
        self.facade.last_undo = "foo_bar"
        self.facade.redo()
        self.assertIsNone(self.facade.last_undo)

    @patch("explorer.facade.FileExplorer.rename")
    @patch("explorer.facade.Cache.redo")
    @patch("explorer.facade.Cache.get_current")
    def test_cant_redo_same_action(self, get_curr_mock, redo_mock, rename_mock):
        self.prev_action["func"] = "rename"
        get_curr_mock.return_value = [self.prev_action]
        self.facade.last_redo = [self.prev_action]
        self.facade.redo()
        rename_mock.assert_not_called()


class TestOpen(unittest.TestCase):

    def setUp(self):
        self.facade = Facade()
        self.directory = "foo"
        self.name = "bar.py"

    @patch("explorer.facade.Path.is_file", return_value=True)
    @patch("explorer.facade.FileExplorer.open_file")
    def test_open_file(self, openf_mock, if_file_mock):
        self.facade.open(self.directory, self.name)
        openf_mock.assert_called_with(Path(self.directory) / self.name)

    @patch("explorer.facade.Path.is_dir", return_value=True)
    @patch("explorer.facade.Path.is_file", return_value=False)
    @patch("explorer.facade.FileExplorer.open_file")
    def test_open_dir(self, openf_mock, if_file_mock, is_dir_mock):
        result = self.facade.open(self.directory, self.name)
        expected = Path(self.directory) / self.name
        openf_mock.assert_not_called()
        self.assertEqual(expected, result)
