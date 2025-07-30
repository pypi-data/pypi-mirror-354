# ruff: noqa: D100

# Standard
import traceback
import importlib.metadata

# First party
from .cmdline import read_args
from .err import HpcWizardError
from .logger import logger, setup_logging

def main_cli() -> int:
    """Main entry point.""" # noqa: D401
    status = 0

    try:
        # Read command line arguments
        args = read_args()

        # Setup logging
        setup_logging(args.verbose)

        # Print version
        if args.version:
            ver = importlib.metadata.version("hpcwizard")
            print(ver) # noqa: T201

        else:
            args.func(args)

    except HpcWizardError as e:
        logger.debug(traceback.format_exc())
        logger.error(str(e))
        status = 1

    return status
