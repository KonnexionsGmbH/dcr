"""Check and distribute incoming documents.

New documents are made available in the file directory inbox.
These are then checked and moved to the accepted or
rejected file directories depending on the result of the check.
Depending on the file format, the accepted documents are then
converted into the pdf file format either with the help of Pandoc
or with the help of Tesseract OCR.
"""
import inspect
import os
import pathlib
import shutil

import fitz
from libs import cfg
from libs import db
from libs import utils
from pdf2image import convert_from_path


# -----------------------------------------------------------------------------
# Check the inbox file directories and create the missing ones.
# -----------------------------------------------------------------------------
def check_and_create_directories() -> None:
    """Check the inbox file directories and create the missing ones.

    The file directory inbox must exist. The two file directories
    inbox_accepted and inbox_rejected are created if they do not
    already exist.
    """
    cfg.logger.debug(cfg.LOGGER_START)

    cfg.inbox = cfg.config[cfg.DCR_CFG_DIRECTORY_INBOX]
    if not os.path.isdir(cfg.inbox):
        utils.terminate_fatal(
            "The inbox directory with the name "
            + cfg.inbox
            + " does not exist - error="
            + str(OSError),
        )

    cfg.inbox_accepted = cfg.config[cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED]
    create_directory("the accepted documents", cfg.inbox_accepted)

    cfg.inbox_rejected = cfg.config[cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED]
    create_directory("the rejected documents", cfg.inbox_rejected)

    db.update_dbt_id(
        cfg.DBT_RUN,
        cfg.run_id,
        {
            cfg.DBC_INBOX_ABS_NAME: str(pathlib.Path(cfg.inbox).absolute()),
            cfg.DBC_INBOX_CONFIG: cfg.inbox,
            cfg.DBC_INBOX_ACCEPTED_ABS_NAME: str(
                pathlib.Path(cfg.inbox_accepted).absolute()
            ),
            cfg.DBC_INBOX_ACCEPTED_CONFIG: cfg.inbox_accepted,
            cfg.DBC_INBOX_REJECTED_ABS_NAME: str(
                pathlib.Path(cfg.inbox_rejected).absolute()
            ),
            cfg.DBC_INBOX_REJECTED_CONFIG: cfg.inbox_rejected,
        },
    )

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create a new file directory if it does not already exist..
# -----------------------------------------------------------------------------
def create_directory(directory_type: str, directory_name: str) -> None:
    """Create a new file directory if it does not already exist.

    Args:
        directory_type (str): Directory type.
        directory_name (str): Directory name - may include a path.
    """
    if not os.path.isdir(directory_name):
        try:
            os.mkdir(directory_name)
            utils.progress_msg(
                "The file directory for "
                + directory_type
                + " was "
                + "newly created under the name "
                + directory_name,
            )
        except OSError:
            utils.terminate_fatal(
                " : The file directory for "
                + directory_type
                + " can "
                + "not be created under the name "
                + directory_name
                + " - error code="
                + str(OSError.errno)
                + " message="
                + OSError.strerror,
            )


# -----------------------------------------------------------------------------
# Prepare a new pdf document for further processing..
# -----------------------------------------------------------------------------
def prepare_pdf() -> None:
    """Prepare a new pdf document for further processing."""
    cfg.logger.debug(cfg.LOGGER_START)

    extracted_text = "".join(
        [page.get_text() for page in fitz.open(utils.get_file_name_inbox())]
    )

    if bool(extracted_text):
        process_inbox_accepted(
            cfg.JOURNAL_ACTION_11_003,
            inspect.stack()[0][3],
            __name__,
            cfg.STATUS_PARSER_READY,
            utils.get_file_name_inbox_accepted(),
        )
    else:
        prepare_pdf_for_tesseract()

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Prepare a new pdf document for Tesseract OCR..
# -----------------------------------------------------------------------------
def prepare_pdf_for_tesseract() -> None:
    """Prepare a new pdf document for Tesseract OCR."""
    cfg.logger.debug(cfg.LOGGER_START)

    try:
        with cfg.config[cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED] as path:
            convert_from_path(utils.get_file_name_inbox(), output_folder=path)

        db.update_document_status(
            cfg.JOURNAL_ACTION_11_004,
            inspect.stack()[0][3],
            __name__,
            cfg.STATUS_TESSERACT_READY,
        )
        cfg.total_accepted += 1
    except shutil.Error as err:
        db.update_document_status(
            cfg.JOURNAL_ACTION_01_903.replace(
                "{source_file}", utils.get_file_name_inbox()
            ).replace("{error}", str(err)),
            inspect.stack()[0][3],
            __name__,
            cfg.STATUS_PDF2IMAGE_ERROR,
        )

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Accept a new document.
# -----------------------------------------------------------------------------
def process_inbox_accepted(
    action: str,
    function_name: str,
    module_name: str,
    status: str,
    target_file_name: str,
) -> None:
    """Accept a new document.

    Args:
        action (str): Current action,
        function_name (str): Name of the originating function.
        module_name (str): Name of the originating module.
        status (str): Current status,
        target_file_name (str): File name in the directory inbox_accepted.
    """
    cfg.logger.debug(cfg.LOGGER_START)

    try:
        shutil.move(utils.get_file_name_inbox(), target_file_name)
        db.update_document_status(
            action,
            function_name,
            module_name,
            status,
        )
        cfg.total_accepted += 1
    except shutil.Error as err:
        db.update_document_status(
            cfg.JOURNAL_ACTION_01_902.replace(
                "{source_file}", utils.get_file_name_inbox()
            )
            .replace("{target_file}", target_file_name)
            .replace("{error}", str(err)),
            inspect.stack()[0][3],
            __name__,
            cfg.STATUS_REJECTED_ERROR,
        )

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Initialise a new document in the database and in the journal.
# -----------------------------------------------------------------------------
def process_inbox_document_initial(file: pathlib.Path) -> None:
    """Initialise a new document in the database and in the journal.

    Analyses the file name and creates an entry in each of the two database
    tables document and journal.

    Args:
        file (pathlib.Path): File.
    """
    cfg.logger.debug(cfg.LOGGER_START)

    cfg.file_name = file.name
    cfg.stem_name = pathlib.PurePath(file).stem
    cfg.file_type = file.suffix[1:].lower()

    db.insert_dbt_document_row()

    db.insert_dbt_journal_row(
        cfg.JOURNAL_ACTION_01_001,
        inspect.stack()[0][3],
        __name__,
    )

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Process the files found in the inbox file directory..
# -----------------------------------------------------------------------------
def process_inbox_files() -> None:
    """Process the files found in the inbox file directory.

    1. Documents of type doc, docx or txt are converted to pdf format
       and copied to the inbox_accepted directory.
    2. Documents of type pdf that do not consist only of a scanned image are
       copied unchanged to the inbox_accepted directory.
    3. Documents of type pdf consisting only of a scanned image are copied
       unchanged to the inbox_ocr directory.
    4. All other documents are copied to the inbox_rejected directory.
    5. For each document a new entry is created in the database table
       document.
    """
    cfg.logger.debug(cfg.LOGGER_START)

    # Check the inbox file directories and create the missing ones.
    check_and_create_directories()

    for file in pathlib.Path(
        cfg.config[cfg.DCR_CFG_DIRECTORY_INBOX]
    ).iterdir():
        if file.is_file():
            cfg.total_new += 1

            process_inbox_document_initial(file)

            if cfg.file_type == cfg.FILE_TYPE_PDF:
                prepare_pdf()
            elif cfg.file_type in (
                cfg.FILE_TYPE_CSV,
                cfg.FILE_TYPE_DOCX,
                cfg.FILE_TYPE_EPUB,
                cfg.FILE_TYPE_HTM,
                cfg.FILE_TYPE_HTML,
                cfg.FILE_TYPE_JSON,
                cfg.FILE_TYPE_MD,
                cfg.FILE_TYPE_ODT,
                cfg.FILE_TYPE_RST,
                cfg.FILE_TYPE_RTF,
            ):
                process_inbox_pandoc()
                db.update_document_status(
                    cfg.JOURNAL_ACTION_11_001,
                    inspect.stack()[0][3],
                    __name__,
                    cfg.STATUS_PANDOC_READY,
                )
            elif cfg.file_type in (
                cfg.FILE_TYPE_BMP,
                cfg.FILE_TYPE_GIF,
                cfg.FILE_TYPE_JP2,
                cfg.FILE_TYPE_JPEG,
                cfg.FILE_TYPE_JPG,
                cfg.FILE_TYPE_PMG,
                cfg.FILE_TYPE_PMN,
                cfg.FILE_TYPE_TIFF,
                cfg.FILE_TYPE_WEBP,
            ):
                process_inbox_tesseract()
                db.update_document_status(
                    cfg.JOURNAL_ACTION_11_002,
                    inspect.stack()[0][3],
                    __name__,
                    cfg.STATUS_TESSERACT_READY,
                )
            else:
                process_inbox_rejected(
                    db.update_document_status(
                        cfg.JOURNAL_ACTION_01_901,
                        inspect.stack()[0][3],
                        __name__,
                        cfg.STATUS_REJECTED_FILE_TYPE,
                    )
                )

    utils.progress_msg("Number documents new      " + str(cfg.total_new))
    utils.progress_msg("Number documents accepted " + str(cfg.total_accepted))
    utils.progress_msg("Number documents rejected " + str(cfg.total_rejected))
    utils.progress_msg(
        "The new documents in the inbox file directory are checked and "
        + "prepared for further processing",
    )

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Convert the new document to PDF format using Pandoc.
# -----------------------------------------------------------------------------
def process_inbox_pandoc() -> None:
    """Convert the new document to PDF format using Pandoc."""
    cfg.logger.debug(cfg.LOGGER_START)

    db.update_document_status(
        cfg.JOURNAL_ACTION_11_001,
        inspect.stack()[0][3],
        __name__,
        cfg.STATUS_PANDOC_READY,
    )

    # target_file_accepted = os.path.join(
    #     cfg.config[cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED],
    #     cfg.stem_name + "_" + str(cfg.document_id) + "." + cfg.file_type,
    # )
    # target_file_rejected = os.path.join(
    #     cfg.config[cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED],
    #     cfg.stem_name + "_" + str(cfg.document_id) + "." + cfg.file_type,
    # )
    # target_file_pdf = os.path.join(
    #     cfg.config[cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED],
    #     cfg.stem_name + "_" + str(cfg.document_id) + "." + cfg.FILE_TYPE_PDF,
    # )
    #
    # try:
    #     pypandoc.convert_file(
    #         source_file=cfg.source_file,
    #         to=cfg.FILE_TYPE_PDF,
    #         outputfile=target_file_pdf,
    #         extra_args=["--latex-engine=weasyprint"],
    #     )
    # except (OSError, RuntimeError) as err:
    #     is_ok = False
    #     process_inbox_document_rejected(
    #         logger,
    #         "01.902 Issue when converting file "
    #         + cfg.source_file
    #         + " with Pandoc - error="
    #         + str(err),
    #         cfg.STATUS_PANDOC_ERROR,
    #     )
    #
    # if is_ok:
    #     try:
    #         shutil.move(cfg.source_file, target_file_accepted)
    #     except shutil.Error as err:
    #         process_inbox_document_rejected(
    #             logger,
    #             "01.903 Issue when moving file "
    #             + cfg.source_file
    #             + " to "
    #             + target_file_rejected
    #             + " - error="
    #             + str(err),
    #             cfg.STATUS_REJECTED_ERROR,
    #         )

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Reject a new document that is faulty.
# -----------------------------------------------------------------------------
def process_inbox_rejected(
    update_document_status: db.update_document_status,
) -> None:
    """Reject a new document that is faulty.

    Args:
        update_document_status (db.update_document_status): Function to update
                    the document status and create a new journal entry.
    """
    cfg.logger.debug(cfg.LOGGER_START)

    try:
        shutil.move(
            utils.get_file_name_inbox(), utils.get_file_name_inbox_rejected()
        )

        # pylint: disable=pointless-statement
        update_document_status

        cfg.total_rejected += 1
    except shutil.Error as err:
        db.update_document_status(
            cfg.JOURNAL_ACTION_01_902.replace(
                "{source_file}", utils.get_file_name_inbox()
            )
            .replace("{target_file}", utils.get_file_name_inbox_rejected())
            .replace("{error}", str(err)),
            inspect.stack()[0][3],
            __name__,
            cfg.STATUS_REJECTED_ERROR,
        )

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Process the new pdf files in the inbox file directory.
# -----------------------------------------------------------------------------
def process_inbox_tesseract() -> None:
    """Process the new pdf documents in the inbox file directory."""
    cfg.logger.debug(cfg.LOGGER_START)

    extracted_text = "".join(
        [page.getText() for page in fitz.open(utils.get_file_name_inbox())]
    )

    doc_type = "text" if extracted_text else "scan"

    print("doc_type=", doc_type)

    cfg.logger.debug(cfg.LOGGER_END)
