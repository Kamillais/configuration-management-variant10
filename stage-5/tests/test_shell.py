"""Unit tests for virtual shell and filesystem."""
import os
import tempfile
import unittest
from pathlib import Path
from src.shell import Shell
from src.vfs import VirtualFS, VFSError


class ShellTests(unittest.TestCase):
    """Check core commands and error handling."""

    def setUp(self):
        self.shell = Shell()

    def test_default_and_navigation(self):
        self.assertEqual(self.shell.execute("ls"), ("", True))
        self.assertTrue(self.shell.execute("mkdir demo")[1])
        self.assertEqual(self.shell.execute("ls")[0], "demo")
        self.assertTrue(self.shell.execute("cd demo")[1])
        self.assertEqual(self.shell.vfs.cwd, "/demo")

    def test_remove_and_errors(self):
        self.shell.execute("mkdir folder")
        self.assertFalse(self.shell.execute("rmdir /")[1])
        self.assertTrue(self.shell.execute("rmdir folder")[1])
        self.assertFalse(self.shell.execute("cd missing")[1])
        self.assertFalse(self.shell.execute("unknown")[1])

    def test_system_commands(self):
        for command in ("uname", "uname -a", "who", "cal", "cal 1 2026"):
            self.assertTrue(self.shell.execute(command)[1], command)
        self.assertFalse(self.shell.execute("cal 13 2026")[1])
        self.assertIn("January", self.shell.execute("cal 2026")[0])

    def test_environment_expansion(self):
        os.environ["VFS_TEST_ARG"] = "sample"
        self.assertTrue(self.shell.execute("mkdir $VFS_TEST_ARG")[1])
        self.assertIn("/sample", self.shell.vfs.nodes)

    def test_csv_load(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "vfs.csv"
            path.write_text(
                "path,type,content_base64\n"
                "/docs,dir,\n"
                "/docs/a.txt,file,SGVsbG8=\n", encoding="utf-8"
            )
            fs = VirtualFS(str(path))
            self.assertEqual(fs.ls("/docs"), ["a.txt"])
            self.assertEqual(fs.get("/docs/a.txt")["data"], b"Hello")
            with self.assertRaises(VFSError):
                fs.mkdir("/docs/a.txt")


if __name__ == "__main__":
    unittest.main()
