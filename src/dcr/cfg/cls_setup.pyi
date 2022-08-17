from __future__ import annotations

import dcr_core.cls_setup
import dcr_core.core_utils

class Setup(dcr_core.cls_setup.Setup):
    db_connection_port: int
    db_connection_prefix: str
    db_container_port: int
    db_database: str
    db_database_admin: str
    db_dialect: str
    db_host: str
    db_initial_data_file: str
    db_password: str
    db_password_admin: str
    db_schema: str
    db_user: str
    db_user_admin: str
    directory_inbox: str
    directory_inbox_accepted: str
    directory_inbox_rejected: str
    doc_id_in_file_name: str
    is_delete_auxiliary_files: bool
    is_ignore_duplicates: bool
    def __init__(self) -> None: ...
