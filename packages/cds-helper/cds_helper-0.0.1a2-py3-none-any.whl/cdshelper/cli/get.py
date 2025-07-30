import argparse


def help_text() -> str:
    """Return subparser help text."""
    return "Retrieve data by specifying parameters for a single dataset"


def command() -> str:
    """Return subparser command name."""
    return "get"


def configure_parser(parser: argparse.ArgumentParser) -> None:
    """Configure the parser for this sub-command."""
    parser.add_argument(
        "--start",
        help="The start of the date range for the desired data.",
        # format="yyyy-mm-dd",
    )
    parser.add_argument(
        "-e",
        "--end",
        help="The date to stop retrieving data for.",
        # format="yyyy-mm-dd",
    )


def handle(args: argparse.Namespace) -> None:
    """Process a CLI request."""
    print("empty get handler")
