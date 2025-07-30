"""CDS API - Multi-month Data Retrieval Demo."""

# ruff: noqa: DTZ001
import argparse
import logging
import sys
import typing as t

import cdshelper.cli.get as get_cli
import cdshelper.cli.request as request_cli
import cdshelper.cli.template as template_cli

CLI_NAME = "cdshelper"


def create_parser() -> argparse.ArgumentParser:
    """Create a parser for the arguments to this utility."""
    parser = argparse.ArgumentParser(
        CLI_NAME,
        description=(
            "cds-helper is a utility for retrieving a contiguous set of monthly "
            "data from the `Climate Data Store` API"
        ),
        # prefix_chars=["-", "--"]
    )

    subparsers = parser.add_subparsers(help="commands", dest="command")

    for tool in [request_cli, template_cli, get_cli]:
        subparser = subparsers.add_parser(
            tool.command(),
            help=tool.help_text(),
        )
        tool.configure_parser(subparser)

    return parser


def get_args() -> list[str]:
    """Retrieve CLI arguments."""
    return sys.argv[1:]


def create_handler_map() -> dict[str, t.Callable[[argparse.Namespace], None]]:
    """Map the command handler to each base command name."""
    return {
        tool.command(): tool.handle for tool in [request_cli, template_cli, get_cli]
    }


def main() -> int:
    """Execute the cds-helper CLI."""
    args_list = get_args()

    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger()

    parser = create_parser()

    if not args_list:
        parser.print_help()
        return 0

    handler_map = create_handler_map()

    try:
        parsed_args = parser.parse_args(args_list)

        handler = handler_map[parsed_args.command]
        handler(parsed_args)
    except FileNotFoundError as ex:
        print(ex.args[0])
    except SystemExit:
        log.debug("Unable to parse arguments", extra={"args_list": args_list})
        return 1

    return 0


if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
