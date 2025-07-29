import argparse
from importlib.metadata import PackageNotFoundError, version

from .__init__ import labyr


def get_version():
    try:
        return version("labyr")  # pypi project name
    except PackageNotFoundError:
        return "unknown"


def callback(action):
    if action == "run":
        labyr()


def main():
    parser = argparse.ArgumentParser(description="labyr: a labyrinth game")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"labyr {get_version()}",
        help="Show labyr version",
    )

    allowed_actions = ["run"]

    parser.add_argument(
        "action",
        choices=allowed_actions,
        help=f"Action to perform. Allowed values: {', '.join(allowed_actions)}",
    )

    args = parser.parse_args()
    callback(args.action)


if __name__ == "__main__":
    main()
