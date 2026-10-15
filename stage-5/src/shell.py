"""Command parser and virtual UNIX-like shell."""
import calendar
import getpass
import os
import platform
import shlex
from datetime import datetime
from .vfs import VFSError, VirtualFS


class Shell:
    """Execute supported commands against an in-memory VFS."""

    def __init__(self, source=None):
        self.vfs = VirtualFS(source)
        self.running = True

    def execute(self, line):
        """Return (output, success) for a command."""
        try:
            expanded = os.path.expandvars(line)
            args = shlex.split(expanded)
            if not args:
                return "", True
            command, *params = args
            if command == "exit":
                self._arity(params, 0)
                self.running = False
                return "Session ended", True
            if command == "ls":
                self._arity(params, 0, 1)
                return "  ".join(self.vfs.ls(params[0] if params else ".")), True
            if command == "cd":
                self._arity(params, 0, 1)
                self.vfs.cd(params[0] if params else "/")
                return "", True
            if command == "mkdir":
                self._arity(params, 1)
                self.vfs.mkdir(params[0])
                return "", True
            if command == "rmdir":
                self._arity(params, 1)
                self.vfs.rmdir(params[0])
                return "", True
            if command == "uname":
                self._arity(params, 0, 1)
                if params and params[0] != "-a":
                    raise VFSError("uname supports only -a")
                return platform.platform() if params else platform.system(), True
            if command == "who":
                self._arity(params, 0)
                return f"{getpass.getuser()}  console  {datetime.now():%Y-%m-%d %H:%M} (simulated session)", True
            if command == "cal":
                self._arity(params, 0, 2)
                now = datetime.now()
                if len(params) == 0:
                    month, year = now.month, now.year
                elif len(params) == 1:
                    return calendar.calendar(int(params[0])).rstrip(), True
                else:
                    month, year = int(params[0]), int(params[1])
                if not 1 <= month <= 12 or not 1 <= year <= 9999:
                    raise VFSError("Invalid month or year")
                return calendar.month(year, month).rstrip(), True
            raise VFSError(f"Unknown command: {command}")
        except (VFSError, ValueError, OverflowError) as error:
            return f"Error: {error}", False

    @staticmethod
    def _arity(args, minimum, maximum=None):
        """Check the number of command arguments."""
        maximum = minimum if maximum is None else maximum
        if not minimum <= len(args) <= maximum:
            raise VFSError(f"Expected {minimum}..{maximum} arguments")
