"""Utility functions for the package."""
import shutil
import platform
import subprocess
from importlib import metadata


def show_notification(title, msg):
    """Show toast notification."""
    pass
    # system = platform.system()
    # if system == "Darwin":  # macOS
    #     subprocess.run(
    #         ['osascript', '-e', f'display notification "{msg}" with title "{title}"'],
    #         check=False,
    #     )
    # elif system == "Linux":
    #     subprocess.run(['notify-send', title, msg], check=False)
    # elif system == "Windows":
    #     import ctypes
    #     ctypes.windll.user32.MessageBoxW(0, msg, title, 0x1000)


try:
    __meta__ = metadata.metadata(__package__ or __name__)
    __version__ = metadata.version(__package__ or __name__) or "0.0.0"
except metadata.PackageNotFoundError:
    __version__ = "0.0.0"
    __meta__ = {}

__project__ = "BitByteLab"
__title____ = "Upwork CLI"
__caption__ = "Your Upwork Workflow at Terminal"
__license__ = __meta__.get("License", "MIT")
__url______ = "https://github.com/rsmahmud/upwork-cli"
__copyright = "2025 BitByteLab"


def banner() -> None:  # noqa: D103
    terminal_size = shutil.get_terminal_size(fallback=(80, 24))
    w = min(terminal_size.columns, 80) - 2
    # fmt: off
    print("\n"
        f"+{'~~~~~~~~~~~~~~~~~~~~~~~~~~~~':{'~'}^{w}}+\n"
        f"│{__title____+' by '+__project__:{' '}^{w}}│\n"
        f"│{'    ' + __caption__ + '     ':{' '}^{w}}│\n"
        f"+{('~' * (len(__caption__) + 2)):{' '}^{w}}+\n"
        f"│{'  Version :  v' + __version__:{' '}^{w}}│\n"
        f"│{'  Copyright © ' + __copyright:{' '}^{w}}│\n"
        f"+{'~~~~~~~~~~~~~~~~~~~~~~~~~~~~':{'~'}^{w}}+\n",
    )
