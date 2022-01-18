Module schema
=============

Functions
---------

    
`check_schema_existence(logger, config, engine)`
:   Checks the existence of the database schema.
    
    Args:
        logger (Logger): Default logger.
        config (dict):   Configuration parameters.
        engine (Engine): Database state.

    
`check_schema_upgrade(logger, _config, _engine)`
:   Checks if the current database schema needs to be upgraded.
    
    Args:
        logger (Logger): Default logger.
        _config (dict):   Configuration parameters.
        _engine (Engine): Database state.

    
`create_schema(logger, config, engine)`
:   Create the database schema.
    
    Args:
        logger (Logger): Default logger.
        config (dict):   Configuration parameters.
        engine (Engine): Database state.

    
`create_table_document(metadata, table)`
:   Initialises the database table document.
    
    If the database table is not yet included in the database schema, then the
    database table is created.
    
    Args:
        metadata (MetaData): Database schema.
        table    (str):      Database table name.

    
`create_table_version(metadata, table)`
:   Initialises the database table version.
    
    If the database table is not yet included in the database schema, then the
    database table is created and the current version number of dcr is inserted.
    
    Args:
        metadata (MetaData): Database schema.
        table    (str):      Database table name.
    
    Return:
        sqlalchemy.Table: Schema of database table version.

    
`get_engine(logger, config)`
:   Initialises the database.
    
    Args:
        logger (Logger): Default logger.
        config (dict):   Configuration parameters.
    
    Returns:
        Engine: Database state.

    
`insert_version_number(logger, config, engine, version)`
:   Initialises the database table version.
    
    If the database table is not yet included in the database schema, then the
    database table is created and the current version number of dcr is inserted.
    
    Args:
        logger  (Logger):           Default logger.
        config  (dict):             Configuration parameters.
        engine  (Engine):           Database state.
        version (sqlalchemy.Table): Schema of database table version.