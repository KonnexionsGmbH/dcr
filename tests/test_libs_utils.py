"""Testing Module libs.utils."""

import libs.cfg
import libs.utils
import pytest

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Function - start_db_docker_container()().
# -----------------------------------------------------------------------------
def test_start_db_docker_container(fxtr_setup_logger_environment):
    """Test: start_db_docker_container()."""
    config_parser, setup_cfg, setup_cfg_backup = pytest.helpers.backup_setup_cfg(
        fxtr_setup_logger_environment
    )

    # -------------------------------------------------------------------------
    config_section = libs.cfg.DCR_CFG_SECTION_TEST
    config_param = libs.cfg.DCR_CFG_DB_DOCKER_CONTAINER

    value_original = pytest.helpers.store_config_param(
        config_parser, config_section, config_param, "n/a"
    )

    fxtr_setup_logger_environment()

    dcr.get_config()

    with pytest.raises(SystemExit) as expt:
        libs.utils.start_db_docker_container()

    assert expt.type == SystemExit, "DCR_CFG_DB_DOCKER_CONTAINER: invalid docker container"
    assert expt.value.code == 1, "DCR_CFG_DB_DOCKER_CONTAINER: invalid docker container"

    pytest.helpers.restore_config_param(config_parser, config_section, config_param, value_original)

    # -------------------------------------------------------------------------
    pytest.helpers.restore_setup_cfg(setup_cfg, setup_cfg_backup)
