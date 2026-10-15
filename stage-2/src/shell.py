"""Stage 1–3: command stubs for GUI REPL."""
import os
import shlex
from .vfs import VirtualFS

class Shell:
    """Parse commands and simulate ls/cd."""
    def __init__(self, source=None):
        self.vfs = VirtualFS(source)
        self.running = True

    def execute(self, line):
        """Return output and execution status."""
        try:
            parts = shlex.split(os.path.expandvars(line))
        except ValueError as error:
            return f"Error: {error}", False
        if not parts:
            return "", True
        command, *args = parts
        if command == "exit":
            if args:
                return "Error: exit takes no arguments", False
            self.running = False
            return "Session ended", True
        if command in ("ls", "cd"):
            if len(args) > 1:
                return "Error: too many arguments", False
            return f"Stub: {command}; args={args}", True
        return f"Error: Unknown command: {command}", False
