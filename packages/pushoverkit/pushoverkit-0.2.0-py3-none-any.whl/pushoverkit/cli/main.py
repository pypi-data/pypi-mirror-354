import argparse
from .message_cli import setup_message_cli
from .groups_cli import setup_groups_cli
from .teams_cli import setup_teams_cli

def main():
    parser = argparse.ArgumentParser(prog="pushoverkit")
    subparsers = parser.add_subparsers(dest="command", required=True)

    setup_message_cli(subparsers)
    setup_groups_cli(subparsers)
    setup_teams_cli(subparsers)

    args = parser.parse_args()
    args.func(args)