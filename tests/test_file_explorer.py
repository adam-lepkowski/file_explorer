import unittest
from unittest.mock import patch, Mock
from pathlib import Path

from parameterized import parameterized

from file_explorer import FileExplorer


class TestIsValidPath(unittest.TestCase):

    def setUp(self):
        self.fe = FileExplorer()
        self.src_dir = "src/path"
        self.src_file = "src/path/foo.py"
        self.dst_dir = "dst/path"

    @patch("file_explorer.pathlib.Path.is_dir", return_value=True)
    def test_src_not_file_raises_error(self, is_dir_mock):
        with self.assertRaises(FileNotFoundError):
            self.fe.is_valid_path(self.src_file, self.dst_dir, "file")

    @patch("file_explorer.pathlib.Path.is_file", return_value=True)
    def test_dst_not_dir_raises_error(self, is_file_mock):
        with self.assertRaises(FileNotFoundError):
            self.fe.is_valid_path(self.src_file, self.dst_dir, "dir")

    @parameterized.expand([
        ("file"),
        ("dir")
    ])
    @patch("file_explorer.pathlib.Path.is_dir", return_value=True)
    @patch("file_explorer.pathlib.Path.is_file", return_value=True)
    def test_is_valid_path(self, name, is_file_mock, is_dir_mock):
        expected = (Path(self.src_file), Path(self.dst_dir))
        result = self.fe.is_valid_path(self.src_file, self.dst_dir, name)
        self.assertEqual(expected, result)

    @patch("file_explorer.pathlib.Path.is_dir", return_value=True)
    @patch("file_explorer.pathlib.Path.is_file", return_value=True)
    def test_invalid_src_type_raises_error(self, is_file_mock, is_dir_mock):
        with self.assertRaises(ValueError):
            self.fe.is_valid_path(self.src_file, self.dst_dir, "foobartype")


class TestGetContent(unittest.TestCase):

    def setUp(self):
        self.fe = FileExplorer()

    @patch("file_explorer.pathlib.Path.iterdir")
    def test_get_content(self, iterdir_mock):
        mocks = [Mock() for _ in range(4)]
        for i, mock in enumerate(mocks):
            mock.is_dir.return_value = True if i % 2 == 0 else False
            mock.is_file.return_value = False if i % 2 == 0 else True
            mock.__str__ = "dir_path" if i % 2 == 0 else "file_path"
        iterdir_mock.return_value = mocks
        result = self.fe.get_content(".")
        expected = {
            "files": [mocks[1], mocks[3]],
            "dirs": [mocks[0], mocks[2]]
        }
        self.assertEqual(expected, result)

    def test_get_content_invalid_path_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            self.fe.get_content('invalid_path')

    @patch("file_explorer.pathlib.Path.iterdir", return_value=[])
    def test_get_content_empty_dir(self, iterdir_mock):
        expected = {
            "files": [],
            "dirs": []
        }
        result = self.fe.get_content(".")
        self.assertEqual(expected, result)


@patch("file_explorer.shutil.copy2")
class TestCopyFile(unittest.TestCase):

    def setUp(self):
        self.fe = FileExplorer()
        self.src_dir = "src/path"
        self.src_file = "src/path/foo.py"
        self.dst_dir = "dst/path"

    @patch("file_explorer.pathlib.Path.glob")
    @patch("file_explorer.pathlib.Path.exists", return_value=True)
    @patch("file_explorer.FileExplorer.is_valid_path")
    def test_copy_file_same_dir(self, vpath_mock, exists_mock, glob_mock,
                                copy2_mock):
        vpath_mock.return_value = (Path(self.src_file), Path(self.src_dir))
        for i in range(1, 10):
            glob_mock.return_value = list(range(i))
            expected = f"src/path/foo_copy_{i}.py"
            result = self.fe.copy_file(self.src_file, self.src_dir)
            copy2_mock.assert_called_with(Path(self.src_file), Path(expected))
            self.assertTrue(isinstance(result, Path))

    @patch("file_explorer.pathlib.Path.glob")
    @patch("file_explorer.pathlib.Path.exists")
    @patch("file_explorer.FileExplorer.is_valid_path")
    def test_copy_file_different_dir(self, vpath_mock, exists_mock, glob_mock,
                                     copy2_mock):
        vpath_mock.return_value = (Path(self.src_file), Path(self.dst_dir))
        exists_mock.side_effect = [bool(i) for i in range(10)]
        for i in range(10):
            if i > 0:
                glob_mock.return_value = list(range(i))
                expected = f"{self.dst_dir}/foo_copy_{i}.py"
            else:
                expected = f"{self.dst_dir}/foo.py"
            result = self.fe.copy_file(self.src_file, self.dst_dir)
            copy2_mock.assert_called_with(Path(self.src_file), Path(expected))
            self.assertTrue(isinstance(result, Path))


@patch("file_explorer.shutil.copytree")
class TestCopyDir(unittest.TestCase):

    def setUp(self):
        self.fe = FileExplorer()
        self.src_dir = "src/path/foo"
        self.dst_dir = "dst/path"

    @patch("file_explorer.FileExplorer.is_valid_path")
    @patch("file_explorer.pathlib.Path.exists", return_value=True)
    @patch("file_explorer.pathlib.Path.glob", return_value=[1])
    def test_copy_dir_same_dir(self, glob_mock, exists_mock, vpath_mock,
                               ctree_mock):
        vpath_mock.return_value = (Path(self.src_dir), Path("src/path"))
        expected = Path("src/path/foo_copy_1")
        result = self.fe.copy_dir(self.src_dir, "src/path")
        ctree_mock.assert_called_with(Path(self.src_dir), Path(expected))

    @patch("file_explorer.FileExplorer.is_valid_path")
    @patch("file_explorer.pathlib.Path.exists", return_value=True)
    @patch("file_explorer.pathlib.Path.glob")
    def test_copy_dir_same_dir_multiple(self, glob_mock, exists_mock,
                                        vpath_mock, ctree_mock):
        vpath_mock.return_value = (Path(self.src_dir), Path("src/path"))
        for i in range(1, 10):
            glob_mock.return_value = list(range(i))
            expected = Path(f"src/path/foo_copy_{i}")
            result = self.fe.copy_dir(self.src_dir, "src/path")
            ctree_mock.assert_called_with(Path(self.src_dir), Path(expected))

    @patch("file_explorer.FileExplorer.is_valid_path")
    @patch("file_explorer.pathlib.Path.exists")
    @patch("file_explorer.pathlib.Path.glob")
    def test_copy_dir_different_dir(self, glob_mock, exists_mock, vpath_mock,
                                    ctree_mock):
        vpath_mock.return_value = (Path(self.src_dir), Path(self.dst_dir))
        # first exists call False cause dst should not exist
        exists_mock.side_effect = [bool(i) for i in range(10)]
        for i in range(10):
            if i > 0:
                glob_mock.return_value = list(range(i))
                expected = f"{self.dst_dir}/foo_copy_{i}"
            else:
                expected = f"{self.dst_dir}/foo"
            result = self.fe.copy_dir(self.src_dir, self.dst_dir)
            ctree_mock.assert_called_with(Path(self.src_dir), Path(expected))
            self.assertTrue(isinstance(result, Path))


class TestCopy(unittest.TestCase):

    def setUp(self):
        self.fe = FileExplorer()
        self.src_file = "src/path/foo.py"
        self.src_dir = "src/path/foo"
        self.dst_dir = "dst/path"

    @patch("file_explorer.pathlib.Path.is_file", return_value=False)
    @patch("file_explorer.pathlib.Path.is_dir", return_value=False)
    def test_copy_invalid_src_raises_error(self, is_dir_mock, is_file_mock):
        with self.assertRaises(FileNotFoundError):
            self.fe.copy(self.src_file, self.dst_dir)

    @patch.object(FileExplorer, "copy_file")
    @patch("file_explorer.pathlib.Path.is_file", return_value=True)
    def test_copy_copies_file(self, is_file_mock, cfile_mock):
        cfile_mock.return_value=Path(self.dst_dir) / "foo.py"
        result = self.fe.copy(self.src_file, self.dst_dir)
        cfile_mock.assert_called_with(Path(self.src_file), Path(self.dst_dir))
        self.assertTrue(isinstance(result, Path))

    @patch.object(FileExplorer, "copy_dir")
    @patch("file_explorer.pathlib.Path.is_file", return_value=False)
    @patch("file_explorer.pathlib.Path.is_dir", return_value=True)
    def test_copy_copies_dir(self, is_dir_mock, is_file_mock, cdir_mock):
        cdir_mock.return_value=Path(self.dst_dir) / "foo"
        result = self.fe.copy(self.src_dir, self.dst_dir)
        cdir_mock.assert_called_with(Path(self.src_dir), Path(self.dst_dir))
        self.assertTrue(isinstance(result, Path))


class TestMove(unittest.TestCase):

    def setUp(self):
        self.fe = FileExplorer()
        self.src = Path("src/path/foo.py")
        self.dst = "dst/path"

    @patch.object(FileExplorer, "copy")
    @patch("file_explorer.pathlib.Path.unlink")
    @patch("file_explorer.pathlib.Path.is_file", return_value=True)
    def test_move_file(self, is_file_mock, unlink_mock, c_mock):
        c_mock.return_value = self.src
        self.fe.move(self.src, self.dst)
        unlink_mock.assert_called_once()

    @patch.object(FileExplorer, "copy")
    @patch("file_explorer.shutil.rmtree")
    @patch("file_explorer.pathlib.Path.is_file", return_value=False)
    @patch("file_explorer.pathlib.Path.is_dir", return_value=True)
    def test_move_dir(self, is_dir_mock, is_file_mock, rmtree_mock, c_mock):
        c_mock.return_value = self.src
        self.fe.move(self.src, self.dst)
        rmtree_mock.assert_called_with(self.src)


class TestRename(unittest.TestCase):

    def setUp(self):
        self.fe = FileExplorer()
        self.src_file = "path/foo/bar.py"
        self.src_dir = "path/foo/bar"

    @parameterized.expand([
        ("no_pref_suff", "path/foo/spam.py", None, None),
        ("prefix", "path/foo/prefix_spam.py", "prefix", None),
        ("suffix", "path/foo/spam_suffix.py", None, "suffix"),
        ("no_pref_suff", "path/foo/prefix_spam_suffix.py", "prefix", "suffix")
    ])
    @patch("file_explorer.pathlib.Path.rename")
    def test_rename_file(self, name, expected, prefix, suffix, rename_mock):
        expected = Path(expected)
        self.fe.rename(self.src_file, "spam", prefix, suffix)
        rename_mock.assert_called_with(expected)
