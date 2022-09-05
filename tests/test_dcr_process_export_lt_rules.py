# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

# pylint: disable=unused-argument
"""Testing Module dcr.dcr."""
import os

import dcr_core.cls_setup
import dcr_core.core_glob

import dcr.cfg.cls_setup
import dcr.cfg.glob
import dcr.db.cls_run
import dcr.launcher

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Function - process_export_lt_rules().
# -----------------------------------------------------------------------------
def test(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_PROCESS_ALL_COMPLETE - delete_auxiliary_files = true."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    try:
        os.mkdir("tmp")
    except OSError:
        pass

    # -------------------------------------------------------------------------
    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_EXPORT_LT_RULES])

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)
