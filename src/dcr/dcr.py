"""Entry point functionality."""

import locale
import logging
import logging.config

import db.schema
import inbox.document
import utils.environ


# ----------------------------------------------------------------------------------
# Entry point.
# ----------------------------------------------------------------------------------


def main():
    """Entry point."""
    # Initialise the logging functionality.
    logger = utils.environ.initialise_logger()

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Start")

    print("Start dcr.py")

    locale.setlocale(locale.LC_ALL, "de_CH.utf8")

    # Load the command line arguments into the memory (pdf ...`)
    args = utils.environ.get_args(logger)

    # Load the configuration parameters into the memory (config params
    # `file.configuration.name ...`)
    config = utils.environ.get_config(logger)

    # Setting up the database.
    engine = db.schema.get_engine(logger, config)

    if args["p_i"]:
        # Processing the inbox directory.
        inbox.document.process_inbox(logger, config, engine)

    print("End   dcr.py")

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("End")


# ----------------------------------------------------------------------------------
# Program start.
# ----------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
