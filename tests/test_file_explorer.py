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


class TestCopyFile(unittest.TestCase):

    def setUp(self):
        self.fe = FileExplorer()
        self.src_dir = "src/path"
        self.src_file = "src/path/foo.py"
        self.dst_dir = "dst/path"

    @patch("file_explorer.shutil.copy2")
    @patch("file_explorer.pathlib.Path.glob")
    @patch("file_explorer.pathlib.Path.exists", return_value=True)
    @patch("file_explorer.pathlib.Path.is_dir", return_value=True)
    @patch("file_explorer.pathlib.Path.is_file", return_value=True)
    def test_copy_file_same_dir(self, is_file_mock, is_dir_mock, exists_mock,
                                glob_mock, copy2_mock):

        expected = "src/path/foo_copy_1.py"
        glob_mock.return_value = [1]
        copy2_mock.return_value = expected
        result = self.fe.copy_file(self.src_file, self.src_dir)
        copy2_mock.assert_called_with(Path(self.src_file), Path(expected))
        self.assertTrue(isinstance(result, Path))

    @patch("file_explorer.shutil.copy2")
    @patch("file_explorer.pathlib.Path.glob")
    @patch("file_explorer.pathlib.Path.exists", return_value=True)
    @patch("file_explorer.pathlib.Path.is_dir", return_value=True)
    @patch("file_explorer.pathlib.Path.is_file", return_value=True)
    def test_copy_file_multiple_times_same_dir(self, is_file_mock, is_dir_mock,
                                               exists_mock, glob_mock,
                                               copy2_mock):
        for i in range(1, 10):
            glob_mock.return_value = list(range(i))
            expected = f"src/path/foo_copy_{i}.py"
            self.fe.copy_file(self.src_file, self.src_dir)
            copy2_mock.assert_called_with(Path(self.src_file), Path(expected))

    @patch("file_explorer.shutil.copy2")
    @patch("file_explorer.pathlib.Path.is_dir", return_value=True)
    @patch("file_explorer.pathlib.Path.is_file", return_value=True)
    def test_copy_file_different_dir(self, is_file_mock, is_dir_mock,
                                    copy2_mock):
        expected = f"{self.dst_dir}/foo.py"
        copy2_mock.return_value = expected
        result = self.fe.copy_file(self.src_file, self.dst_dir)
        copy2_mock.assert_called_with(Path(self.src_file), Path(expected))
        self.assertTrue(isinstance(result, Path))

    @patch("file_explorer.shutil.copy2")
    @patch("file_explorer.pathlib.Path.glob")
    @patch("file_explorer.pathlib.Path.exists", return_value=False)
    @patch("file_explorer.pathlib.Path.is_dir", return_value=True)
    @patch("file_explorer.pathlib.Path.is_file", return_value=True)
    def test_copy_file_different_dir_multiple_times(self, is_file_mock,
                                                    is_dir_mock,exists_mock,
                                                    glob_mock, copy2_mock):
        for i in range(10):
            if i != 0:
                exists_mock.return_value = True
                glob_mock.return_value = list(range(i))
                expected = f"dst/path/foo_copy_{i}.py"
            else:
                exists_mock.return_value = False
                expected = f"dst/path/foo.py"
            self.fe.copy_file(self.src_file, self.dst_dir)
            copy2_mock.assert_called_with(Path(self.src_file), Path(expected))
