"""Main entry points for the module."""

import sys
import argparse

from upwork_cli.upcli import UpworkShell
from upwork_cli.utils import banner, show_notification


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(prog="upwork-cli", add_help=False)
    parser.add_argument(
        "-v",
        "-V",
        "--version",
        action="store_true",
        help="Show version and exit",
    )
    parser.add_argument(
        "-h", "-H", "--help", action="store_true", help="Show help and exit"
    )
    parser.add_argument("cmd", nargs=argparse.REMAINDER, help="Command to run")

    args = parser.parse_args()

    if args.version:
        show_notification(title="Upwork CLI", msg="upwork-cli is running!")
        banner()
        if args.cmd:
            return
        sys.exit(0)

    if args.help:
        print(
            "Usage: upwork-api [options] <command> [args]\n\n"
            "Options:\n"
            "  -v, --version  Show version\n"
            "  -h, --help     Show help"
        )
        if args.cmd:
            return
        sys.exit(0)

    if args.cmd:
        UpworkShell().onecmd(" ".join(args.cmd))
    else:
        UpworkShell().cmdloop("Entering Upwork CLI shell. Type 'help' or '?'.")



if __name__ == '__main__':
    main()
