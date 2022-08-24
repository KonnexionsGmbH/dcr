# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Testing Module dcr.cfg.cls_..."""
import os

import dcr_core.cls_setup
import dcr_core.core_glob
import pytest

import dcr.cfg.cls_setup
import dcr.cfg.glob

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# pylint: disable=unused-argument
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Check parameter complete.
# -----------------------------------------------------------------------------
def check_param_complete():
    """Check parameter complete."""
    dcr_core.core_glob.setup = dcr.cfg.cls_setup.Setup()

    assert len(dcr_core.core_glob.setup._config) == dcr_core.core_glob.setup._CONFIG_PARAM_NO, "cfg:: complete"

    dcr_core.core_glob.setup = dcr.cfg.cls_setup.Setup()

    assert len(dcr_core.core_glob.setup._config) == dcr_core.core_glob.setup._CONFIG_PARAM_NO, "dcr_core.cfg:: complete"


# -----------------------------------------------------------------------------
# Check parameter TOKENIZE_2_.
# -----------------------------------------------------------------------------
def check_param_tokenize_2_():
    """Check parameter TOKENIZE_2_."""
    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_TOKENIZE_2_DATABASE, "fALSE"),
            (dcr_core.cls_setup.Setup._DCR_CFG_TOKENIZE_2_JSONFILE, "fALSE"),
        ],
    )

    with pytest.raises(SystemExit) as expt:
        dcr_core.core_glob.setup = dcr.cfg.cls_setup.Setup()

    assert expt.type == SystemExit, "both DCR_CFG_TOKENIZE_2_DATABASE and DCR_CFG_TOKENIZE_2_JSONFILE false"
    assert expt.value.code == 1, "both DCR_CFG_TOKENIZE_2_DATABASE and DCR_CFG_TOKENIZE_2_JSONFILE false"


# -----------------------------------------------------------------------------
# Test Function - get_config() - 1.
# -----------------------------------------------------------------------------
def test_get_config_1(fxtr_setup_logger_environment):
    """Test: get_config() - 1."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_PDF2IMAGE_TYPE, dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    with pytest.raises(SystemExit) as expt:
        dcr_core.core_glob.setup = dcr.cfg.cls_setup.Setup()

    assert expt.type == SystemExit, "DCR_CFG_PDF2IMAGE_TYPE: invalid"
    assert expt.value.code == 1, "DCR_CFG_PDF2IMAGE_TYPE: invalid"

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config() - 2.
# -----------------------------------------------------------------------------
def test_get_config_2(fxtr_setup_logger_environment):
    """Test: test_get_config - 2."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    check_param_complete()

    check_param_tokenize_2_()

    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config() - coverage - false.
# -----------------------------------------------------------------------------
def test_get_config_coverage_false(fxtr_setup_logger_environment):
    """Test: test_get_config_coverage_false()."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.set_complete_cfg_spacy("false")

    dcr_core.core_glob.setup = dcr.cfg.cls_setup.Setup()

    # -------------------------------------------------------------------------
    dcr_core.core_glob.setup._determine_config_param_integer(dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE, 4711)

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config() - coverage - true.
# -----------------------------------------------------------------------------
def test_get_config_coverage_true(fxtr_setup_logger_environment):
    """Test: test_get_config_coverage_true()."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.set_complete_cfg_spacy("true")

    dcr_core.core_glob.setup = dcr.cfg.cls_setup.Setup()

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config().
# -----------------------------------------------------------------------------
def test_get_config_doc_id_in_file_name(fxtr_setup_logger_environment):
    """Test: get_config_doc_id_in_file_name()."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        dcr.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr.cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "aFTER"),
        ],
    )

    dcr_core.core_glob.setup = dcr.cfg.cls_setup.Setup()

    assert dcr_core.core_glob.setup.doc_id_in_file_name == "after", "DCR_CFG_DOC_ID_IN_FILE_NAME: after"

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        dcr.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr.cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "bEFORE"),
        ],
    )

    dcr_core.core_glob.setup = dcr.cfg.cls_setup.Setup()

    assert dcr_core.core_glob.setup.doc_id_in_file_name == "before", "DCR_CFG_DOC_ID_IN_FILE_NAME: before"

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        dcr.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr.cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    dcr_core.core_glob.setup = dcr.cfg.cls_setup.Setup()

    assert dcr_core.core_glob.setup.doc_id_in_file_name == "none", "DCR_CFG_DOC_ID_IN_FILE_NAME: none (not after or before)"

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


def test_get_config_missing_02(fxtr_setup_logger_environment):
    """Test: get_config() - missing."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.config_param_delete(dcr.cfg.cls_setup.Setup._DCR_CFG_SECTION, dcr.cfg.cls_setup.Setup._DCR_CFG_DIRECTORY_INBOX_ACCEPTED)
    pytest.helpers.config_param_delete(
        dcr.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST, dcr.cfg.cls_setup.Setup._DCR_CFG_DIRECTORY_INBOX_ACCEPTED
    )

    with pytest.raises(SystemExit) as expt:
        dcr_core.core_glob.setup = dcr.cfg.cls_setup.Setup()

    assert expt.type == SystemExit, "DCR_CFG_DIRECTORY_INBOX_ACCEPTED: missing"
    assert expt.value.code == 1, "DCR_CFG_DIRECTORY_INBOX_ACCEPTED: missing"

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


def test_get_config_missing_03(fxtr_setup_logger_environment):
    """Test: get_config() - missing."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.config_param_delete(dcr.cfg.cls_setup.Setup._DCR_CFG_SECTION, dcr.cfg.cls_setup.Setup._DCR_CFG_DIRECTORY_INBOX_REJECTED)
    pytest.helpers.config_param_delete(
        dcr.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST, dcr.cfg.cls_setup.Setup._DCR_CFG_DIRECTORY_INBOX_REJECTED
    )

    with pytest.raises(SystemExit) as expt:
        dcr_core.core_glob.setup = dcr.cfg.cls_setup.Setup()

    assert expt.type == SystemExit, "DCR_CFG_DIRECTORY_INBOX_REJECTED: missing"
    assert expt.value.code == 1, "DCR_CFG_DIRECTORY_INBOX_REJECTED: missing"

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


def test_get_config_missing_04(fxtr_setup_logger_environment):
    """Test: get_config() - missing."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.config_param_delete(
        dcr.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST, dcr.cfg.cls_setup.Setup._DCR_CFG_IGNORE_DUPLICATES
    )

    dcr_core.core_glob.setup.is_ignore_duplicates = False

    dcr_core.core_glob.setup = dcr.cfg.cls_setup.Setup()

    assert not dcr_core.core_glob.setup.is_ignore_duplicates, "DCR_CFG_IGNORE_DUPLICATES: false (missing)"

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


def test_get_config_missing_05(fxtr_setup_logger_environment):
    """Test: get_config() - missing."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.config_param_delete(dcr_core.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST, dcr_core.cls_setup.Setup._DCR_CFG_PDF2IMAGE_TYPE)

    dcr_core.core_glob.setup.pdf2image_type = dcr_core.core_glob.setup.PDF2IMAGE_TYPE_JPEG

    dcr_core.core_glob.setup = dcr.cfg.cls_setup.Setup()

    assert dcr_core.core_glob.setup.pdf2image_type == dcr_core.core_glob.setup.PDF2IMAGE_TYPE_JPEG, (
        "DCR_CFG_PDF2IMAGE_TYPE: default should not be '" + dcr_core.core_glob.setup.pdf2image_type + "'"
    )

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


def test_get_config_missing_06(fxtr_setup_logger_environment):
    """Test: get_config() - missing."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.config_param_delete(dcr_core.cls_setup.Setup._DCR_CFG_SECTION, dcr_core.cls_setup.Setup._DCR_CFG_VERBOSE)
    pytest.helpers.config_param_delete(dcr_core.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST, dcr_core.cls_setup.Setup._DCR_CFG_VERBOSE)

    dcr_core.core_glob.setup.is_verbose = True

    dcr_core.core_glob.setup = dcr.cfg.cls_setup.Setup()

    assert dcr_core.core_glob.setup.is_verbose, "DCR_CFG_VERBOSE: true (missing)"

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


def test_get_config_missing_07(fxtr_setup_logger_environment):
    """Test: get_config() - missing."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.config_param_delete(dcr_core.cls_setup.Setup._DCR_CFG_SECTION, dcr_core.cls_setup.Setup._DCR_CFG_VERBOSE_PARSER)
    pytest.helpers.config_param_delete(dcr_core.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST, dcr_core.cls_setup.Setup._DCR_CFG_VERBOSE_PARSER)

    dcr_core.core_glob.setup = dcr.cfg.cls_setup.Setup()

    assert dcr_core.core_glob.setup.verbose_parser == "none", "DCR_CFG_VERBOSE_PARSER: none (missing)"

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config().
# -----------------------------------------------------------------------------
def test_get_config_verbose_parser(fxtr_setup_logger_environment):
    """Test: get_config_verbose_parser()."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_VERBOSE_PARSER, "aLL"),
        ],
    )

    dcr_core.core_glob.setup = dcr.cfg.cls_setup.Setup()

    assert dcr_core.core_glob.setup.verbose_parser == "all", "DCR_CFG_VERBOSE_PARSER: all"

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_VERBOSE_PARSER, dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    dcr_core.core_glob.setup = dcr.cfg.cls_setup.Setup()

    assert dcr_core.core_glob.setup.verbose_parser == "none", "DCR_CFG_VERBOSE_PARSER: none (not all or text)"

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_VERBOSE_PARSER, "tEXT"),
        ],
    )

    dcr_core.core_glob.setup = dcr.cfg.cls_setup.Setup()

    assert dcr_core.core_glob.setup.verbose_parser == "text", "DCR_CFG_VERBOSE_PARSER: all"

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_environment().
# -----------------------------------------------------------------------------
def test_get_environment(fxtr_setup_logger):
    """Test: get_environment()."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr_core.core_glob.setup = dcr.cfg.cls_setup.Setup()

    os.environ[dcr_core.core_glob.setup._DCR_ENVIRONMENT_TYPE] = dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE

    with pytest.raises(SystemExit) as expt:
        dcr_core.core_glob.setup._get_environment_variant()

    os.environ[dcr_core.core_glob.setup._DCR_ENVIRONMENT_TYPE] = dcr_core.core_glob.setup.ENVIRONMENT_TYPE_TEST

    assert expt.type == SystemExit, "_DCR_ENVIRONMENT_TYPE: invalid"
    assert expt.value.code == 1, "_DCR_ENVIRONMENT_TYPE: invalid"

    # -------------------------------------------------------------------------
    os.environ.pop(dcr_core.core_glob.setup._DCR_ENVIRONMENT_TYPE)

    with pytest.raises(SystemExit) as expt:
        dcr_core.core_glob.setup._get_environment_variant()

    os.environ[dcr_core.core_glob.setup._DCR_ENVIRONMENT_TYPE] = dcr_core.core_glob.setup.ENVIRONMENT_TYPE_TEST

    assert expt.type == SystemExit, "_DCR_ENVIRONMENT_TYPE: missing"
    assert expt.value.code == 1, "_DCR_ENVIRONMENT_TYPE: missing"

    # -------------------------------------------------------------------------
    dcr_core.core_glob.setup._get_environment_variant()

    assert dcr_core.core_glob.setup.environment_variant == dcr_core.core_glob.setup.ENVIRONMENT_TYPE_TEST, "_DCR_ENVIRONMENT_TYPE: ok"

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)
