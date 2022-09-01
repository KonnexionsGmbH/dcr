# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

# pylint: disable=unused-argument
"""Testing Module dcr.db.cls_db_core."""
import dcr_core.cls_setup
import dcr_core.core_glob
import dcr_core.core_utils
import pytest

import dcr.cfg.cls_setup
import dcr.cfg.glob
import dcr.db.cls_db_core
import dcr.db.cls_run
import dcr.launcher

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


def test(fxtr_setup_empty_db_and_inbox):
    """Test: drop_database()."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr_core.core_glob.setup = dcr.cfg.cls_setup.Setup()

    # -------------------------------------------------------------------------
    pytest.helpers.config_param_delete(dcr.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST, dcr.cfg.cls_setup.Setup._DCR_CFG_DB_DIALECT)

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_CREATE_DB])

    dcr.cfg.glob.db_core = dcr.db.cls_db_core.DBCore(is_admin=True)

    dcr.cfg.glob.db_core._drop_database()

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)
