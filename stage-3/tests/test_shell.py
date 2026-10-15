import unittest
from src.shell import Shell
from src.vfs import VirtualFS

class StageThreeTests(unittest.TestCase):
    def test_vfs_load(self):
        fs=VirtualFS("data/deep.csv")
        self.assertEqual(fs.ls("/docs/projects/2026"), ["readme.txt"])
    def test_stub_commands(self):
        self.assertTrue(Shell("data/deep.csv").execute("ls")[0].startswith("Stub:"))
    def test_invalid_command(self):
        self.assertFalse(Shell().execute("missing")[1])
