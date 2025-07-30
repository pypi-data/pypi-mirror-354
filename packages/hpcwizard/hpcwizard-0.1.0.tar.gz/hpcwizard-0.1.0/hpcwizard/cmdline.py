# ruff: noqa: D100

# Standard
import argparse

# Third party
import rich_argparse

# First party
from .subcmd_gen_workflow import add_gen_workflow_subcmd

class CustomFormatter(rich_argparse.RawTextRichHelpFormatter,
                      rich_argparse.ArgumentDefaultsRichHelpFormatter):
    """Custom formatter."""

def read_args() -> argparse.Namespace:
    """Parse command line arguments."""

    # Setup parser
    parser = argparse.ArgumentParser(
            description = "HPC Workflow generator.",
            formatter_class = CustomFormatter)

    # Add sub-commands
    subparsers = parser.add_subparsers(help = "Subcommands.")
    add_gen_workflow_subcmd(subparsers.add_parser("gen-workflow",
            formatter_class = CustomFormatter,
            description = ("Generate a shell script or DAG from YAML workflow"
                           " description.")))

    # Quiet mode
    parser.add_argument("-q", dest="quiet", action="store_true",
        help="Set verbose level to 0.")

    # Verbose level
    parser.add_argument("-v", action="count", dest="verbose", default=1,
        help="Set verbose level.")

    # Version
    parser.add_argument("--version", action="store_true",
        help="Print version.")

    # Parse
    args = parser.parse_args()

    if args.quiet:
        args.verbose = 0

    return args
