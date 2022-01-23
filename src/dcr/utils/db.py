"""
### Module: **Database Schema Management**.

Database schema-related processing routines.
"""
from typing import Union

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import MetaData
from sqlalchemy.engine import Engine

from utils.constant import DB_ENGINE
from utils.constant import DB_METADATA
from utils.constant import DCR_CFG_DATABASE_URL


# -----------------------------------------------------------------------------
# Get the database state.
# -----------------------------------------------------------------------------


def get_engine(
    config: dict[str, Union[Engine, MetaData]],
) -> Union[Engine, MetaData]:
    """
    #### Function: **Get the database state**.

    **Args**:
    - **config (dict[str, Union[Engine,MetaData]])**: Configuration parameters.

    Returns:
    - **Union[Engine, MetaData]**: Database state.
    """
    if DB_ENGINE in config:
        engine = config[DB_ENGINE]
    else:
        engine = sqlalchemy.create_engine(config[DCR_CFG_DATABASE_URL])
        config[DB_ENGINE] = engine

    return engine


# -----------------------------------------------------------------------------
# Get a metadata object.
# -----------------------------------------------------------------------------


def get_metadata(
    config: dict[str, Union[Engine, MetaData]],
) -> Union[Engine, MetaData]:
    """
    #### Function: **Get a metadata object.**.

    **Args**:
    - **config (dict[str, Union[Engine,MetaData])**: Configuration parameters.

    Returns:
    - **Union[Engine, MetaData]**: Metadata object.
    """
    if DB_METADATA in config:
        metadata = config[DB_METADATA]
    else:
        metadata = sqlalchemy.MetaData()
        config[DB_METADATA] = metadata

    return metadata
