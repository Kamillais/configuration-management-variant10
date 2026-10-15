import unittest
from src.shell import Shell

class StageTests(unittest.TestCase):
    def test_ls_stub(self):
        self.assertTrue(Shell().execute("ls")[0].startswith("Stub: ls"))
    def test_unknown(self):
        self.assertFalse(Shell().execute("wrong")[1])
    def test_exit(self):
        shell = Shell()
        self.assertTrue(shell.execute("exit")[1])
        self.assertFalse(shell.running)
