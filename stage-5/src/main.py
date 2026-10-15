"""Tkinter GUI for the virtual shell."""
import argparse
import tkinter as tk
from tkinter import scrolledtext
from .shell import Shell
from .vfs import VFSError


class ShellWindow:
    """Interactive graphical shell with script playback."""

    def __init__(self, shell, prompt):
        self.shell = shell
        self.prompt = prompt
        self.root = tk.Tk()
        self.root.title(f"VFS Emulator — {shell.vfs.name}")
        self.root.geometry("760x480")
        self.output = scrolledtext.ScrolledText(
            self.root, state="disabled", font=("Courier", 12)
        )
        self.output.pack(fill="both", expand=True, padx=12, pady=12)
        self.entry = tk.Entry(self.root, font=("Courier", 12))
        self.entry.pack(fill="x", padx=12, pady=(0, 12))
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus_set()

    def write(self, text):
        """Append text to the console."""
        self.output.configure(state="normal")
        self.output.insert("end", text + "\n")
        self.output.see("end")
        self.output.configure(state="disabled")

    def run_command(self, line):
        """Echo and execute one command."""
        self.write(f"{self.prompt} {line}")
        result, success = self.shell.execute(line)
        if result:
            self.write(result)
        if not self.shell.running:
            self.entry.configure(state="disabled")
            self.root.after(250, self.root.destroy)
        return success

    def on_enter(self, _event):
        """Handle interactive input."""
        line = self.entry.get()
        self.entry.delete(0, "end")
        self.run_command(line)

    def play_script(self, path):
        """Run script lines, reporting and skipping errors."""
        try:
            with open(path, encoding="utf-8") as stream:
                lines = stream.readlines()
        except OSError as error:
            self.write(f"Script error: {error}")
            return
        for number, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if not self.run_command(line):
                self.write(f"Script error at line {number}; continuing")
            if not self.shell.running:
                break


def main():
    """Parse options and start the GUI."""
    parser = argparse.ArgumentParser(description="Variant 10 VFS emulator")
    parser.add_argument("--vfs", help="CSV filesystem source")
    parser.add_argument("--prompt", default="vfs$",
                        help="Custom interactive prompt")
    parser.add_argument("--script", help="Startup command script")
    options = parser.parse_args()
    print(f"Configuration: VFS={options.vfs!r}, "
          f"prompt={options.prompt!r}, script={options.script!r}")
    try:
        shell = Shell(options.vfs)
    except VFSError as error:
        parser.error(str(error))
    window = ShellWindow(shell, options.prompt)
    if options.script:
        window.root.after(100, lambda: window.play_script(options.script))
    window.root.mainloop()


if __name__ == "__main__":
    main()
