"""
Тесты команд
"""

import unittest
import tempfile
import os
import shutil
from pathlib import Path
from src.commands import ls, cd, cat, cp, mv, rm, zip_cmd, unzip_cmd, tar_cmd, untar_cmd, grep

class TestCommands(unittest.TestCase):
    def setUp(self):
        """Временный каталог для всех тестов"""
        self.test_dir = Path(tempfile.mkdtemp())
        os.chdir(self.test_dir)

    def tearDown(self):
        """Удаляем временный каталог после каждого теста"""
        os.chdir("/")
        shutil.rmtree(self.test_dir, ignore_errors=True)

    # ls
    def test_ls_simple(self):
        (self.test_dir / "test.txt").write_text("x")
        (self.test_dir / "dir").mkdir()
        output = ls(["."], long=False)
        self.assertIn("test.txt", output)
        self.assertIn("dir", output)

    def test_ls_long(self):
        f = self.test_dir / "test.txt"
        f.write_text("x")
        output = ls(["."], long=True)
        self.assertTrue(any("test.txt" in line for line in output))
        self.assertTrue(any("-rw-r--r--" in line for line in output))

    def test_ls_nonexistent(self):
        with self.assertRaises(FileNotFoundError):
            ls(["nonexistent"], long=False)

    # cd
    def test_cd_valid(self):
        new_dir = self.test_dir / "dir"
        new_dir.mkdir()
        cd(str(new_dir))
        self.assertEqual(Path.cwd(), new_dir.resolve())

    def test_cd_nonexistent(self):
        with self.assertRaises(FileNotFoundError):
            cd("nonexistent")

    # cat
    def test_cat_single_file(self):
        f = self.test_dir / "test.txt"
        f.write_text("line1\nline2")
        output = cat([str(f)])
        self.assertEqual(output, ["line1\n", "line2"])

    def test_cat_multiple_files(self):
        f1 = self.test_dir / "a.txt"
        f2 = self.test_dir / "b.txt"
        f1.write_text("A")
        f2.write_text("B")
        output = cat([str(f1), str(f2)])
        self.assertEqual(output, ["A", "B"])

    def test_cat_on_directory(self):
        d = self.test_dir / "dir"
        d.mkdir()
        with self.assertRaises(IsADirectoryError):
            cat([str(d)])

    def test_cat_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            cat(["nonexistent.txt"])

    # cp
    def test_cp_file(self):
        src = self.test_dir / "src.txt"
        dst = self.test_dir / "dst.txt"
        src.write_text("x")
        cp([str(src)], str(dst), recursive=False)
        self.assertTrue(dst.exists())
        self.assertEqual(dst.read_text(), "x")

    def test_cp_dir_recursive(self):
        src_dir = self.test_dir / "src_dir"
        src_dir.mkdir()
        (src_dir / "test.txt").write_text("x")
        dst_dir = self.test_dir / "dst_dir"
        cp([str(src_dir)], str(dst_dir), recursive=True)
        self.assertTrue((dst_dir / "test.txt").exists())

    def test_cp_dir_without_r(self):
        src_dir = self.test_dir / "src_dir"
        src_dir.mkdir()
        with self.assertRaises(IsADirectoryError):
            cp([str(src_dir)], "dst", recursive=False)

    def test_cp_nonexistent_source(self):
        with self.assertRaises(FileNotFoundError):
            cp(["nonexistent.txt"], "dst.txt", recursive=False)

    # mv
    def test_mv_file(self):
        src = self.test_dir / "old.txt"
        dst = self.test_dir / "new.txt"
        src.write_text("moved")
        mv([str(src)], str(dst))
        self.assertFalse(src.exists())
        self.assertTrue(dst.exists())

    def test_mv_file_into_directory(self):
        src_file = self.test_dir / "test.txt"
        target_dir = self.test_dir / "dir"
        target_dir.mkdir()
        src_file.write_text("x")
        mv([str(src_file)], str(target_dir))
        self.assertFalse(src_file.exists())
        moved_file = target_dir / "test.txt"
        self.assertTrue(moved_file.exists())

    def test_mv_nonexistent_source(self):
        with self.assertRaises(FileNotFoundError):
            mv(["nonexistent.txt"], "dest.txt")

    # rm
    def test_rm_file(self):
        f = self.test_dir / "test.txt"
        f.write_text("x")
        rm([str(f)], recursive=False)
        self.assertFalse(f.exists())

    def test_rm_multiple_files(self):
        f1 = self.test_dir / "file1.txt"
        f2 = self.test_dir / "file2.log"
        f3 = self.test_dir / "file3.csv"
        f1.write_text("x")
        f2.write_text("x")
        f3.write_text("x")
        rm([str(f1), str(f2), str(f3)], recursive=False)
        self.assertFalse(f1.exists())
        self.assertFalse(f2.exists())
        self.assertFalse(f3.exists())

    def test_rm_dir_recursive(self):
        d = self.test_dir / "to_delete"
        d.mkdir()
        (d / "test.txt").write_text("x")
        # Подделаем input для подтверждения
        import builtins
        def l_input(prompt: str = ""):
            return 'y'
        original_input = builtins.input
        builtins.input = l_input
        try:
            rm([str(d)], recursive=True)
            self.assertFalse(d.exists())
        finally:
            builtins.input = original_input

    def test_rm_nonexistent(self):
        with self.assertRaises(FileNotFoundError):
            rm(["nonexistent.txt"], recursive=False)

    def test_rm_root_protection(self):
        # Проверяем защиту от удаления корня (в твоей реализации)
        root_path = "/"
        if os.name == 'nt':
            root_path = "C:\\"
        with self.assertRaises(PermissionError):
            rm([root_path], recursive=True)

    # zip/unzip
    def test_zip_unzip(self):
        # zip
        folder = self.test_dir / "folder"
        folder.mkdir()
        (folder / "f.txt").write_text("zip test")
        zip_cmd(str(folder), str(self.test_dir / "archive"))
        archive_path = self.test_dir / "archive.zip"
        self.assertTrue(archive_path.exists())
        # unzip
        shutil.rmtree(folder)
        unzip_cmd(str(archive_path))
        self.assertTrue((self.test_dir / "folder" / "f.txt").exists())

    def test_zip_nonexistent_folder(self):
        with self.assertRaises(FileNotFoundError):
            zip_cmd("nonexistent", "archive.zip")

    def test_unzip_nonexistent_archive(self):
        with self.assertRaises(FileNotFoundError):
            unzip_cmd("nonexistent.zip")

    def test_unzip_invalid_file(self):
        f = self.test_dir / "not_zip.txt"
        f.write_text("not a zip")
        with self.assertRaises(ValueError):
            unzip_cmd(str(f))

    # tar/untar
    def test_tar_and_untar(self):
        # tar
        folder = self.test_dir / "tar_folder"
        folder.mkdir()
        (folder / "t.txt").write_text("tar test")
        tar_cmd(str(folder), str(self.test_dir / "backup"))
        archive_path = self.test_dir / "backup.tar.gz"
        self.assertTrue(archive_path.exists())
        # untar
        shutil.rmtree(folder)
        untar_cmd(str(archive_path))
        self.assertTrue((self.test_dir / "tar_folder" / "t.txt").exists())

    def test_tar_nonexistent_folder(self):
        with self.assertRaises(FileNotFoundError):
            tar_cmd("nonexistent", "archive.tar.gz")

    def test_untar_nonexistent_archive(self):
        with self.assertRaises(FileNotFoundError):
            untar_cmd("nonexistent.tar.gz")

    def test_untar_invalid_file(self):
        f = self.test_dir / "not_tar.txt"
        f.write_text("not a tar")
        with self.assertRaises(ValueError):
            untar_cmd(str(f))

    # grep
    def test_grep_simple(self):
        f = self.test_dir / "test.txt"
        f.write_text("hello world\nfoo bar\nhello again")
        results = grep("hello", [str(f)], recursive=False, ignore_case=False)
        self.assertEqual(len(results), 2)

    def test_grep_ignore_case(self):
        f = self.test_dir / "test.txt"
        f.write_text("Hello\nworld")
        results = grep("hello", [str(f)], recursive=False, ignore_case=True)
        self.assertEqual(len(results), 1)

    def test_grep_recursive(self):
        subdir = self.test_dir / "sub"
        subdir.mkdir()
        (subdir / "file.txt").write_text("pattern")
        (self.test_dir / "root.txt").write_text("pattern")
        results = grep("pattern", [str(self.test_dir)], recursive=True, ignore_case=False)
        self.assertEqual(len(results), 2)

    def test_grep_directory_without_recursive(self):
        d = self.test_dir / "dir"
        d.mkdir()
        with self.assertRaises(ValueError):
            grep("test", [str(d)], recursive=False, ignore_case=False)

    def test_grep_nonexistent_path(self):
        with self.assertRaises(FileNotFoundError):
            grep("test", ["nonexistent.txt"], recursive=False, ignore_case=False)


if __name__ == "__main__":
    unittest.main()
