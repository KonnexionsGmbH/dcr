"""Module db.utils: Helper functions."""
import os
from typing import Dict
from typing import TypeAlias

import sqlalchemy.engine

# -----------------------------------------------------------------------------
# Type declaration.
# -----------------------------------------------------------------------------
Columns: TypeAlias = Dict[
    str, bool | sqlalchemy.Boolean | int | sqlalchemy.Integer | str | os.PathLike[str] | sqlalchemy.String | None
]
