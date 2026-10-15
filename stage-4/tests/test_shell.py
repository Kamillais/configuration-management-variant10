import unittest
from src.shell import Shell

class StageFourTests(unittest.TestCase):
    def test_navigation(self):
        shell=Shell("data/deep.csv")
        self.assertTrue(shell.execute("cd /docs")[1])
        self.assertIn("projects", shell.execute("ls")[0])
    def test_uname(self):
        self.assertTrue(Shell().execute("uname")[1])
    def test_who(self):
        self.assertTrue(Shell().execute("who")[1])
    def test_cal(self):
        self.assertTrue(Shell().execute("cal 10 2026")[1])
    def test_no_mkdir_yet(self):
        self.assertFalse(Shell().execute("mkdir new")[1])
