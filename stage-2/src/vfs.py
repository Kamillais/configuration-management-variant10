"""Minimal VFS placeholder for stages 1 and 2."""
class VirtualFS:
    def __init__(self, source=None):
        self.name = source or "default"
        self.cwd = "/"
