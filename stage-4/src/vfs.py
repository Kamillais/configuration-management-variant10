"""In-memory CSV-backed virtual file system."""
import base64
import csv
import io
import posixpath


class VFSError(ValueError):
    """Invalid virtual filesystem operation."""


class VirtualFS:
    """Manage directories and files without changing the host disk."""

    def __init__(self, source=None):
        self.nodes = {"/": {"type": "dir", "data": b""}}
        self.cwd = "/"
        self.name = "default"
        if source:
            self.load(source)

    def normalize(self, path):
        """Resolve absolute or relative virtual paths."""
        if not path:
            return self.cwd
        path = path if path.startswith("/") else posixpath.join(self.cwd, path)
        return posixpath.normpath(path)

    def load(self, source):
        """Read CSV into memory, preserving the original file."""
        try:
            with open(source, newline="", encoding="utf-8") as stream:
                reader = csv.DictReader(stream)
                if not {"path", "type", "content_base64"} <= set(reader.fieldnames or []):
                    raise VFSError("CSV must have path,type,content_base64 columns")
                rows = list(reader)
            nodes = {"/": {"type": "dir", "data": b""}}
            for row in rows:
                path = posixpath.normpath(row["path"])
                kind = row["type"]
                if not path.startswith("/") or kind not in {"dir", "file"}:
                    raise VFSError("Invalid path or type")
                try:
                    content = base64.b64decode(row["content_base64"], validate=True)
                except (ValueError, base64.binascii.Error) as error:
                    raise VFSError("Invalid base64 data") from error
                if path != "/":
                    if path in nodes:
                        raise VFSError("Duplicate path")
                    nodes[path] = {"type": kind, "data": content}
            for path in nodes:
                if path != "/":
                    parent = posixpath.dirname(path)
                    if parent not in nodes or nodes[parent]["type"] != "dir":
                        raise VFSError("Missing parent directory")
            self.nodes = nodes
            self.cwd = "/"
            self.name = source.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
        except (OSError, UnicodeError, csv.Error) as error:
            raise VFSError(f"Cannot load VFS: {error}") from error

    def get(self, path):
        """Return a node, raising for a missing path."""
        resolved = self.normalize(path)
        if resolved not in self.nodes:
            raise VFSError(f"No such file or directory: {path}")
        return self.nodes[resolved]

    def ls(self, path="."):
        """List immediate children of a directory."""
        resolved = self.normalize(path)
        node = self.get(path)
        if node["type"] == "file":
            return [posixpath.basename(resolved)]
        return sorted(
            posixpath.basename(p) for p in self.nodes
            if p != resolved and posixpath.dirname(p) == resolved
        )

    def cd(self, path="/"):
        """Change the current virtual directory."""
        resolved = self.normalize(path)
        if self.get(path)["type"] != "dir":
            raise VFSError(f"Not a directory: {path}")
        self.cwd = resolved

    def mkdir(self, path):
        """Create a directory in memory."""
        resolved = self.normalize(path)
        if resolved in self.nodes:
            raise VFSError(f"Already exists: {path}")
        parent = posixpath.dirname(resolved)
        if parent not in self.nodes or self.nodes[parent]["type"] != "dir":
            raise VFSError(f"Parent directory missing: {path}")
        self.nodes[resolved] = {"type": "dir", "data": b""}

    def rmdir(self, path):
        """Remove an empty directory from memory."""
        resolved = self.normalize(path)
        if resolved == "/":
            raise VFSError("Cannot remove root")
        if self.get(path)["type"] != "dir":
            raise VFSError(f"Not a directory: {path}")
        if any(posixpath.dirname(p) == resolved for p in self.nodes):
            raise VFSError(f"Directory not empty: {path}")
        del self.nodes[resolved]
