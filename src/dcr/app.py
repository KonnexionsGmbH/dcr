"""
### **Entry point functionality**.

This is the entry point to the application `dcr`.
"""

import locale
import logging
import logging.config

from inbox.document import process_inbox
from utils.constant import LOCALE
from utils.constant import LOGGER_END
from utils.constant import LOGGER_START
from utils.db import get_engine
from utils.environ import get_args
from utils.environ import get_config
from utils.environ import initialise_logger


# -----------------------------------------------------------------------------
# Entry point.
# -----------------------------------------------------------------------------


def main() -> None:
    """
    **Entry point**.

    The processes to be carried out are selected via command line arguments.
    """
    # Initialise the logging functionality.
    logger = initialise_logger()

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_START)

    print("Start app.py")

    locale.setlocale(locale.LC_ALL, LOCALE)

    # Load the command line arguments into the memory (pdf ...`)
    args = get_args(logger)

    # Load the configuration parameters into the memory (config params
    # `file.configuration.name ...`)
    config = get_config(logger)

    # Setting up the database.
    engine = get_engine(logger, config)

    if args["p_i"]:
        # Processing the inbox directory.
        process_inbox(logger, config, engine)

    print("End   app.py")

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_END)


# -----------------------------------------------------------------------------
# Program start.
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
