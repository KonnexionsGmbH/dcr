Module environ
==============
Auxiliary routines for the environment data..

Support of command line arguments, configuration parameters and
logging functionality.

Functions
---------

    
`get_args(logger)`
:   Load the command line arguments into memory.
    
    Args:
        logger (Logger): Default logger.
    
    Returns:
        dict: Edited command line arguments.

    
`get_config(logger)`
:   Load the configuration parameters into memory.
    
    Args:
        logger (Logger): Default logger.
    
    Returns:
        dict: Configuration parameters.

    
`initialise_logger()`
:   Initialise the logging functionality.
    
    Returns:
        Logger: Default logger.