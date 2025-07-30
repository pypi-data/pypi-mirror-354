# ruff: noqa: D100

# Standard
import logging
import typing

# Third party
import colorlog

VERBOSE_INFO_LEVEL = 1
VERBOSE_DEBUG_LEVEL = 2
VERBOSE_TRACE_LEVEL = 3

# Get logger
logger = logging.getLogger("biophony")

def setup_logging(verbose: int, log_file: str | None = None) -> None:
    """Configure logging for both import and gen-data scripts."""
    # Define TRACE level
    logging.TRACE = 5 # type: ignore[attr-defined]
    logging.addLevelName(logging.TRACE, "TRACE")  # type: ignore[attr-defined]

    def trace(self: logging.Logger, message: object,
              *args: typing.Any, **kws: typing.Any) -> None: # noqa: ANN401
        if self.isEnabledFor(logging.TRACE):  # type: ignore[attr-defined]
            self._log(logging.TRACE,  # type: ignore[attr-defined]
                      message, args, **kws)

    logging.Logger.trace = trace  # type: ignore[attr-defined]

    # Define formatter for file logging.
    fmt = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")

    # Define formatter for colored console logging.
    color_fmt = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s %(levelname)-8s %(message)s",
        log_colors={
            "TRACE": "light_cyan",
            "DEBUG": "light_yellow",
            "INFO": "light_green",
            "WARNING": "light_purple",
            "ERROR": "light_red",
            "CRITICAL": "light_red",
        },
    )

    # Define console handler
    color_handler = colorlog.StreamHandler()
    color_handler.setFormatter(color_fmt)
    logger.addHandler(color_handler)

    # Set log file
    if log_file is not None:
        fh = logging.FileHandler(log_file)
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    # Set log level
    if verbose >= VERBOSE_TRACE_LEVEL:
        logger.setLevel(logging.TRACE)  # type: ignore[attr-defined]
    elif verbose == VERBOSE_DEBUG_LEVEL:
        logger.setLevel(logging.DEBUG)
    elif verbose == VERBOSE_INFO_LEVEL:
        logger.setLevel(logging.INFO)
