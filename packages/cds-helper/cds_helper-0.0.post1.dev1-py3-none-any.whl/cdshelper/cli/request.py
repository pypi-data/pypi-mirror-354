import argparse
import json
import pathlib
from datetime import datetime

from cdshelper.core.core import (
    CdsDataRequest,
    download_monthly_data,
)

DATE_FORMAT = "%Y-%m-%d"  # "%Y-%m-%d %H:%M:%S"


def help_text() -> str:
    """Return subparser help text."""
    return (
        "Retrieve data by specifying a path to a "
        "JSON file containing the request parameters."
    )


def command() -> str:
    """Return subparser command name."""
    return "request"


def _format_date(date_str: str) -> datetime:
    """Convert a date string to a datetime object using the default format.

    Parameters
    ----------
    date_str : str
        The date string to convert.

    Returns
    -------
    datetime
        The converted datetime.
    """
    return datetime.strptime(  # noqa: DTZ007
        date_str,
        DATE_FORMAT,
    )


def configure_parser(parser: argparse.ArgumentParser) -> None:
    """Configure the parser for this sub-command."""
    parser.add_argument("path", help="Path to a file containing request details.")
    parser.add_argument(
        "-o",
        "--output",
        help="Path to write the retrieved datasets to.",
        default="./output",
    )
    parser.add_argument("-dry-run", action="store_true")


def handle(args: argparse.Namespace) -> None:
    """Process a CLI request."""
    path = pathlib.Path(args.path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"A file does not exist at {path}.")

    output_to = pathlib.Path(args.output).resolve()
    if not output_to.exists():
        output_to.mkdir(parents=True)

    with path.open() as fp:
        request_dict = json.load(fp)

    request_dict["start_date"] = _format_date(request_dict["start_date"])
    request_dict["end_date"] = _format_date(request_dict["end_date"])

    file_map = request_dict.pop("file_map")
    request = CdsDataRequest(**request_dict, dry_run=args.dry_run)
    download_monthly_data(request, file_map, output_to)
