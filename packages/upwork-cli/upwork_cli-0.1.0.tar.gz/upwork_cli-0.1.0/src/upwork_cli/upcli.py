"""
Automate and streamline your Upwork freelancer workflow using the Upwork API.

Author: Mahmudul Hasan Rasel
Version: 1.0.0
Created: 2025-06-09
License: MIT
Github: https://github.com/rsmahmud/python-api
Portfolio: https://rsmahmud.github.io
"""

import os
import cmd
import shlex
import argparse
from pprint import pprint

import upwork
from upwork.routers import auth

from upwork_cli.utils import banner

#from upwork.routers.jobs import search
#from upwork.routers.activities import team
#from upwork.routers.reports import time
#from urllib.parse import quote

_nyi = "not yet implemented!"


class UpworkShell(cmd.Cmd):
    """UpworkShell Class."""

    def __init__(self):
        super().__init__()
        self.prompt = "up-cli$ "
        self.api_key = os.getenv("UPWORK_API_KEY")
        self.api_secret = os.getenv("UPWORK_API_SECRET")
        self.access_token = os.getenv("UPWORK_ACCESS_TOKEN")
        self.access_token_secret = os.getenv("UPWORK_ACCESS_TOKEN_SECRET")

    def get_desktop_client(self):
        """Emulation of a desktop application.

        Your key should be created with the project type "Desktop".

        Returns: ``upwork.Client`` instance ready to work.

        """
        print("Emulating desktop app")
        consumer_key = self.api_key or input("Please enter consumer key: > ")
        consumer_secret = self.api_secret or input("Please enter key secret: > ")
        if self.api_secret and self.access_token_secret:
            config = upwork.Config(
                {
                    "consumer_key": consumer_key,
                    "consumer_secret": consumer_secret,
                    "access_token": self.access_token,
                    "access_token_secret": self.access_token_secret,
                }
            )
        else:
            config = upwork.Config(
                {
                    "consumer_key": consumer_key,
                    "consumer_secret": consumer_secret
                }
            )

        _client = upwork.Client(config)

        try:
            _ = config.access_token
            _ = config.access_token_secret
        except AttributeError:
            verifier = input(
                "Please enter the verification code you get "
                f"following this link:\n{client.get_authorization_url()}\n\n>"
            )
            print("Retrieving keys.... ")
            self.access_token, self.access_token_secret = client.get_access_token(verifier)
            os.environ["UPWORK_ACCESS_TOKEN"] = self.access_token
            os.environ["UPWORK_ACCESS_TOKEN_SECRET"] = self.access_token_secret
            print("OK")
        return client

    def do_reviews(self, arg):
        """Fetch and display Upwork reviews. Usage: reviews [--limit N] [--out file.json]."""
        parser = argparse.ArgumentParser(prog="reviews")
        parser.add_argument("--limit", type=int, default=10)
        parser.add_argument("--out", type=str)

        try:
            args = parser.parse_args(shlex.split(arg))
            print(f"Fetching {args.limit} reviews...")
            if args.out:
                print(f"Outputting to {args.out}")
        except SystemExit:
            pass  # Prevent argparse from exiting shell
        print(f"[reviews] args: {arg}")
        print(f"[reviews] {_nyi}")

    def do_exit(self, arg):
        """Exit the shell."""
        print("exiting...")
        return True

    def do_EOF(self, line):
        """Handle EOF."""
        return self.do_exit(line)

    def do_version(self, arg):
        """Show version."""
        banner()

    def do_help(self, arg):
        """Show help messages."""
        if arg:
            super().do_help(arg)
        else:
            print(
                "Available commands:\n"
                "  reviews  Fetch and display reviews\n"
                "  version  Show version\n"
                "  help     Show this help\n"
                "  exit     Exit the shell"
            )

    def default(self, line):
        """Default command handler."""
        print(f"Unknown command: {line}. Type 'help' or '?' for a list of commands.")


if __name__ == '__main__':

    client =  UpworkShell().get_desktop_client()

    try:
        print("My info")
        pprint(auth.Api(client).get_user_info())
        # pprint(search.Api(client).find(
        #     {'q': 'php'}
        # ))
        # pprint(team.Api(client).add_activity(
        #     'mycompany', 'mycompany',
        #     {'code': 'team-task-001', 'description': 'Description', 'all_in_company': '1'}
        # ))
        # _q = quote(
        #     'SELECT task, memo WHERE worked_on >= "2020-05-01" AND worked_on <= "2020-06-01"'
        # )
        # pprint(time.Gds(client).get_by_freelancer_full(
        #     'username',
        #     {'tq': _q}
        # ))
    except Exception as e:
        print("Catch or log exception details")
        raise
