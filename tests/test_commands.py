import unittest
import tempfile
import os
import shutil
from pathlib import Path
from src.commands import ls, cd, cat, cp, mv, rm, zip_cmd, unzip_cmd, tar_cmd, untar_cmd

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
        self.assertTrue(any("-rw" in line for line in output))

    def test_ls_nonexistent(self):
        with self.assertRaises(FileNotFoundError):
            ls(["nonexistent"], long=False)

    # cd
    def test_cd_valid(self):
        new_dir = self.test_dir / "dir"
        new_dir.mkdir()
        cd(str(new_dir))
        self.assertEqual(Path.cwd(), new_dir.resolve())

    def test_cd_invalid(self):
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

    # cp
    def test_cp_file(self):
        src = self.test_dir / "src.txt"
        dst = self.test_dir / "dst.txt"
        src.write_text("ч")
        cp([str(src)], str(dst))
        self.assertTrue(dst.exists())
        self.assertEqual(dst.read_text(), "ч")

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
        src_file.write_text("important data")
        mv([str(src_file)], str(target_dir))
        self.assertFalse(src_file.exists())
        moved_file = target_dir / "test.txt"
        self.assertTrue(moved_file.exists())

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


if __name__ == "__main__":
    unittest.main()
