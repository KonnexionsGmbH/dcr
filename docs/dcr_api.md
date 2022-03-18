# Table of Contents

* [dcr](#dcr)
  * [get\_args](#dcr.get_args)
  * [get\_config](#dcr.get_config)
  * [get\_environment](#dcr.get_environment)
  * [initialise\_logger](#dcr.initialise_logger)
  * [main](#dcr.main)
  * [process\_convert\_image\_2\_pdf](#dcr.process_convert_image_2_pdf)
  * [process\_convert\_non\_pdf\_2\_pdf](#dcr.process_convert_non_pdf_2_pdf)
  * [process\_convert\_pdf\_2\_image](#dcr.process_convert_pdf_2_image)
  * [process\_documents](#dcr.process_documents)
  * [process\_extract\_text\_from\_pdf](#dcr.process_extract_text_from_pdf)
  * [process\_inbox\_directory](#dcr.process_inbox_directory)
  * [validate\_config](#dcr.validate_config)
  * [validate\_config\_directory\_inbox](#dcr.validate_config_directory_inbox)
  * [validate\_config\_directory\_inbox\_accepted](#dcr.validate_config_directory_inbox_accepted)
  * [validate\_config\_directory\_inbox\_rejected](#dcr.validate_config_directory_inbox_rejected)
  * [validate\_config\_ignore\_duplicates](#dcr.validate_config_ignore_duplicates)
  * [validate\_config\_pdf2image\_type](#dcr.validate_config_pdf2image_type)
  * [validate\_config\_tesseract\_timeout](#dcr.validate_config_tesseract_timeout)
  * [validate\_config\_verbose](#dcr.validate_config_verbose)
* [libs](#libs)
* [libs.cfg](#libs.cfg)
* [libs.db.cfg](#libs.db.cfg)
* [libs.db.driver](#libs.db.driver)
  * [connect\_db](#libs.db.driver.connect_db)
  * [connect\_db\_admin](#libs.db.driver.connect_db_admin)
  * [create\_database](#libs.db.driver.create_database)
  * [create\_database\_postgresql](#libs.db.driver.create_database_postgresql)
  * [disconnect\_db](#libs.db.driver.disconnect_db)
  * [drop\_database](#libs.db.driver.drop_database)
  * [drop\_database\_postgresql](#libs.db.driver.drop_database_postgresql)
  * [prepare\_connect\_db\_admin](#libs.db.driver.prepare_connect_db_admin)
  * [select\_version\_version\_unique](#libs.db.driver.select_version_version_unique)
  * [upgrade\_database](#libs.db.driver.upgrade_database)
  * [upgrade\_database\_version](#libs.db.driver.upgrade_database_version)
* [libs.db.orm](#libs.db.orm)
  * [check\_db\_up\_to\_date](#libs.db.orm.check_db_up_to_date)
  * [connect\_db](#libs.db.orm.connect_db)
  * [create\_db\_trigger\_function](#libs.db.orm.create_db_trigger_function)
  * [create\_db\_trigger\_created\_at](#libs.db.orm.create_db_trigger_created_at)
  * [create\_db\_trigger\_modified\_at](#libs.db.orm.create_db_trigger_modified_at)
  * [create\_db\_triggers](#libs.db.orm.create_db_triggers)
  * [create\_dbt\_document](#libs.db.orm.create_dbt_document)
  * [create\_dbt\_journal](#libs.db.orm.create_dbt_journal)
  * [create\_dbt\_run](#libs.db.orm.create_dbt_run)
  * [create\_dbt\_version](#libs.db.orm.create_dbt_version)
  * [create\_schema](#libs.db.orm.create_schema)
  * [disconnect\_db](#libs.db.orm.disconnect_db)
  * [insert\_dbt\_row](#libs.db.orm.insert_dbt_row)
  * [insert\_journal](#libs.db.orm.insert_journal)
  * [prepare\_connect\_db](#libs.db.orm.prepare_connect_db)
  * [select\_document\_file\_name\_sha256](#libs.db.orm.select_document_file_name_sha256)
  * [select\_run\_run\_id\_last](#libs.db.orm.select_run_run_id_last)
  * [select\_version\_version\_unique](#libs.db.orm.select_version_version_unique)
  * [update\_dbt\_id](#libs.db.orm.update_dbt_id)
  * [update\_document\_status](#libs.db.orm.update_document_status)
  * [update\_version\_version](#libs.db.orm.update_version_version)
* [libs.db](#libs.db)
* [libs.inbox](#libs.inbox)
  * [check\_and\_create\_directories](#libs.inbox.check_and_create_directories)
  * [create\_directory](#libs.inbox.create_directory)
  * [initialise\_document\_base](#libs.inbox.initialise_document_base)
  * [prepare\_document\_base](#libs.inbox.prepare_document_base)
  * [prepare\_document\_child\_accepted](#libs.inbox.prepare_document_child_accepted)
  * [prepare\_pdf](#libs.inbox.prepare_pdf)
  * [process\_inbox](#libs.inbox.process_inbox)
  * [process\_inbox\_accepted](#libs.inbox.process_inbox_accepted)
  * [process\_inbox\_file](#libs.inbox.process_inbox_file)
  * [process\_inbox\_rejected](#libs.inbox.process_inbox_rejected)
* [libs.pandocdcr](#libs.pandocdcr)
  * [convert\_non\_pdf\_2\_pdf](#libs.pandocdcr.convert_non_pdf_2_pdf)
  * [convert\_non\_pdf\_2\_pdf\_file](#libs.pandocdcr.convert_non_pdf_2_pdf_file)
* [libs.pdf2imagedcr](#libs.pdf2imagedcr)
  * [convert\_pdf\_2\_image](#libs.pdf2imagedcr.convert_pdf_2_image)
  * [convert\_pdf\_2\_image\_file](#libs.pdf2imagedcr.convert_pdf_2_image_file)
  * [prepare\_document\_4\_tesseract](#libs.pdf2imagedcr.prepare_document_4_tesseract)
* [libs.pdflibdcr](#libs.pdflibdcr)
  * [extract\_text\_from\_pdf](#libs.pdflibdcr.extract_text_from_pdf)
  * [extract\_text\_from\_pdf\_file](#libs.pdflibdcr.extract_text_from_pdf_file)
  * [prepare\_document\_4\_parser](#libs.pdflibdcr.prepare_document_4_parser)
* [libs.tesseractdcr](#libs.tesseractdcr)
  * [convert\_image\_2\_pdf](#libs.tesseractdcr.convert_image_2_pdf)
  * [convert\_image\_2\_pdf\_file](#libs.tesseractdcr.convert_image_2_pdf_file)
* [libs.utils](#libs.utils)
  * [check\_directories](#libs.utils.check_directories)
  * [compute\_sha256](#libs.utils.compute_sha256)
  * [duplicate\_file\_error](#libs.utils.duplicate_file_error)
  * [finalize\_file\_conversion](#libs.utils.finalize_file_conversion)
  * [initialise\_document\_child](#libs.utils.initialise_document_child)
  * [prepare\_document\_4\_parser\_tesseract](#libs.utils.prepare_document_4_parser_tesseract)
  * [prepare\_document\_4\_pdflib](#libs.utils.prepare_document_4_pdflib)
  * [prepare\_file\_names](#libs.utils.prepare_file_names)
  * [progress\_msg](#libs.utils.progress_msg)
  * [progress\_msg\_connected](#libs.utils.progress_msg_connected)
  * [progress\_msg\_disconnected](#libs.utils.progress_msg_disconnected)
  * [progress\_msg\_empty\_before](#libs.utils.progress_msg_empty_before)
  * [reset\_statistics](#libs.utils.reset_statistics)
  * [select\_document](#libs.utils.select_document)
  * [select\_document\_prepare](#libs.utils.select_document_prepare)
  * [show\_statistics](#libs.utils.show_statistics)
  * [start\_document\_processing](#libs.utils.start_document_processing)
  * [str\_2\_path](#libs.utils.str_2_path)
  * [terminate\_fatal](#libs.utils.terminate_fatal)

<a id="dcr"></a>

# dcr

Module dcr: Entry Point Functionality.

This is the entry point to the application DCR.

<a id="dcr.get_args"></a>

#### get\_args

```python
def get_args(argv: List[str]) -> dict[str, bool]
```

Load the command line arguments.

The command line arguments define the process steps to be executed.
The valid arguments are:

all   - Run the complete processing of all new documents.
db_c  - Create the database.
db_u  - Upgrade the database.
n_2_p - Convert non-pdf documents to pdf files.
ocr   - Convert image documents to pdf files.
p_i   - Process the inbox directory.
p_2_i - Convert pdf documents to image files.
tet   - Extract text and metadata from pdf documents.

With the option all, the following process steps are executed
in this order:

1. p_i
2. p_2_i
3. n_2_p
4. ocr
5. tet

**Arguments**:

- `argv` _List[str]_ - Command line arguments.
  

**Returns**:

  dict[str, bool]: The processing steps based on CLI arguments.

<a id="dcr.get_config"></a>

#### get\_config

```python
def get_config() -> None
```

Load the configuration parameters.

Loads the configuration parameters from the `setup.cfg` file under
the `DCR` sections.

<a id="dcr.get_environment"></a>

#### get\_environment

```python
def get_environment() -> None
```

Load environment variables.

<a id="dcr.initialise_logger"></a>

#### initialise\_logger

```python
def initialise_logger() -> None
```

Initialise the root logging functionality.

<a id="dcr.main"></a>

#### main

```python
def main(argv: List[str]) -> None
```

Entry point.

The processes to be carried out are selected via command line arguments.

**Arguments**:

- `argv` _List[str]_ - Command line arguments.

<a id="dcr.process_convert_image_2_pdf"></a>

#### process\_convert\_image\_2\_pdf

```python
def process_convert_image_2_pdf()
```

Convert image documents to pdf files.

<a id="dcr.process_convert_non_pdf_2_pdf"></a>

#### process\_convert\_non\_pdf\_2\_pdf

```python
def process_convert_non_pdf_2_pdf()
```

Convert non-pdf documents to pdf files.

<a id="dcr.process_convert_pdf_2_image"></a>

#### process\_convert\_pdf\_2\_image

```python
def process_convert_pdf_2_image()
```

Convert pdf documents to image files.

<a id="dcr.process_documents"></a>

#### process\_documents

```python
def process_documents(args: dict[str, bool]) -> None
```

Process the documents.

**Arguments**:

- `args` _dict[str, bool]_ - The processing steps based on CLI arguments.

<a id="dcr.process_extract_text_from_pdf"></a>

#### process\_extract\_text\_from\_pdf

```python
def process_extract_text_from_pdf()
```

Extract text and metadata from pdf documents.

<a id="dcr.process_inbox_directory"></a>

#### process\_inbox\_directory

```python
def process_inbox_directory() -> None
```

Process the inbox directory.

<a id="dcr.validate_config"></a>

#### validate\_config

```python
def validate_config() -> None
```

Validate the configuration parameters.

<a id="dcr.validate_config_directory_inbox"></a>

#### validate\_config\_directory\_inbox

```python
def validate_config_directory_inbox() -> None
```

Validate the configuration parameters - directory_inbox.

<a id="dcr.validate_config_directory_inbox_accepted"></a>

#### validate\_config\_directory\_inbox\_accepted

```python
def validate_config_directory_inbox_accepted() -> None
```

Validate the configuration parameters - directory_inbox_accepted.

<a id="dcr.validate_config_directory_inbox_rejected"></a>

#### validate\_config\_directory\_inbox\_rejected

```python
def validate_config_directory_inbox_rejected() -> None
```

Validate the configuration parameters - directory_inbox_rejected.

<a id="dcr.validate_config_ignore_duplicates"></a>

#### validate\_config\_ignore\_duplicates

```python
def validate_config_ignore_duplicates() -> None
```

Validate the configuration parameters - ignore_duplicates.

<a id="dcr.validate_config_pdf2image_type"></a>

#### validate\_config\_pdf2image\_type

```python
def validate_config_pdf2image_type() -> None
```

Validate the configuration parameters - pdf2image_type.

<a id="dcr.validate_config_tesseract_timeout"></a>

#### validate\_config\_tesseract\_timeout

```python
def validate_config_tesseract_timeout() -> None
```

Validate the configuration parameters - tesseract_timeout.

<a id="dcr.validate_config_verbose"></a>

#### validate\_config\_verbose

```python
def validate_config_verbose() -> None
```

Validate the configuration parameters - verbose.

<a id="libs"></a>

# libs

Package libs: DCR libraries.

<a id="libs.cfg"></a>

# libs.cfg

Module libs.cfg: DCR Configuration Data.

<a id="libs.db.cfg"></a>

# libs.db.cfg

Module libs.db.cfg: Database Configuration Data.

<a id="libs.db.driver"></a>

# libs.db.driver

Module libs.db.driver: Database Definition Management.

<a id="libs.db.driver.connect_db"></a>

#### connect\_db

```python
def connect_db() -> None
```

Connect to the database.

<a id="libs.db.driver.connect_db_admin"></a>

#### connect\_db\_admin

```python
def connect_db_admin() -> None
```

Connect to the admin database.

<a id="libs.db.driver.create_database"></a>

#### create\_database

```python
def create_database() -> None
```

Create the database.

<a id="libs.db.driver.create_database_postgresql"></a>

#### create\_database\_postgresql

```python
def create_database_postgresql() -> None
```

Create the database tables.

<a id="libs.db.driver.disconnect_db"></a>

#### disconnect\_db

```python
def disconnect_db() -> None
```

Disconnect the admin database.

<a id="libs.db.driver.drop_database"></a>

#### drop\_database

```python
def drop_database() -> None
```

Drop the database.

<a id="libs.db.driver.drop_database_postgresql"></a>

#### drop\_database\_postgresql

```python
def drop_database_postgresql() -> None
```

Drop the PostgreSQL database.

<a id="libs.db.driver.prepare_connect_db_admin"></a>

#### prepare\_connect\_db\_admin

```python
def prepare_connect_db_admin() -> None
```

Prepare the database connection for administrators.

<a id="libs.db.driver.select_version_version_unique"></a>

#### select\_version\_version\_unique

```python
def select_version_version_unique() -> str
```

Get the version number from the database table 'version'.

**Returns**:

- `str` - The version number found.

<a id="libs.db.driver.upgrade_database"></a>

#### upgrade\_database

```python
def upgrade_database() -> None
```

Upgrade the current database schema.

Check if the current database schema needs to be upgraded and
perform the necessary steps.

<a id="libs.db.driver.upgrade_database_version"></a>

#### upgrade\_database\_version

```python
def upgrade_database_version() -> None
```

Upgrade the current database schema - from one version to the next.

<a id="libs.db.orm"></a>

# libs.db.orm

Module libs.db.orm: Database Manipulation Management.

<a id="libs.db.orm.check_db_up_to_date"></a>

#### check\_db\_up\_to\_date

```python
def check_db_up_to_date() -> None
```

Check that the database version is up-to-date.

<a id="libs.db.orm.connect_db"></a>

#### connect\_db

```python
def connect_db() -> None
```

Connect to the database.

<a id="libs.db.orm.create_db_trigger_function"></a>

#### create\_db\_trigger\_function

```python
def create_db_trigger_function(column_name: str) -> None
```

Create the trigger function.

**Arguments**:

- `column_name` _str_ - Column name.

<a id="libs.db.orm.create_db_trigger_created_at"></a>

#### create\_db\_trigger\_created\_at

```python
def create_db_trigger_created_at(table_name: str) -> None
```

Create the trigger for the database column created_at.

**Arguments**:

- `table_name` _str_ - Table name.

<a id="libs.db.orm.create_db_trigger_modified_at"></a>

#### create\_db\_trigger\_modified\_at

```python
def create_db_trigger_modified_at(table_name: str) -> None
```

Create the trigger for the database column modified_at.

**Arguments**:

- `table_name` _str_ - Table name.

<a id="libs.db.orm.create_db_triggers"></a>

#### create\_db\_triggers

```python
def create_db_triggers(table_names: List[str]) -> None
```

Create the triggers for the database tables.

**Arguments**:

- `table_names` _List[str]_ - Table names.

<a id="libs.db.orm.create_dbt_document"></a>

#### create\_dbt\_document

```python
def create_dbt_document(table_name: str) -> None
```

Create the database table document.

**Arguments**:

- `table_name` _str_ - Table name.

<a id="libs.db.orm.create_dbt_journal"></a>

#### create\_dbt\_journal

```python
def create_dbt_journal(table_name: str) -> None
```

Create the database table journal.

**Arguments**:

- `table_name` _str_ - Table name.

<a id="libs.db.orm.create_dbt_run"></a>

#### create\_dbt\_run

```python
def create_dbt_run(table_name: str) -> None
```

Create the database table run.

**Arguments**:

- `table_name` _str_ - Table name.

<a id="libs.db.orm.create_dbt_version"></a>

#### create\_dbt\_version

```python
def create_dbt_version(table_name: str) -> None
```

Create and initialise the database table version.

If the database table is not yet included in the database schema, then the
database table is created and the current version number of DCR is
inserted.

**Arguments**:

- `table_name` _str_ - Table name.

<a id="libs.db.orm.create_schema"></a>

#### create\_schema

```python
def create_schema() -> None
```

Create the database tables and triggers.

<a id="libs.db.orm.disconnect_db"></a>

#### disconnect\_db

```python
def disconnect_db() -> None
```

Disconnect the database.

<a id="libs.db.orm.insert_dbt_row"></a>

#### insert\_dbt\_row

```python
def insert_dbt_row(table_name: str,
                   columns: libs.cfg.Columns) -> sqlalchemy.Integer
```

Insert a new row into a database table.

**Arguments**:

- `table_name` _str_ - Table name.
- `columns` _libs.cfg.TYPE_COLUMNS_INSERT_ - Pairs of column name and value.
  

**Returns**:

- `sqlalchemy.Integer` - The last id found.

<a id="libs.db.orm.insert_journal"></a>

#### insert\_journal

```python
def insert_journal(module_name: str, function_name: str,
                   document_id: sqlalchemy.Integer,
                   journal_action: str) -> None
```

Insert a new row into database table 'journal'.

**Arguments**:

- `module_name` _str_ - Module name.
- `function_name` _str_ - Function name.
- `document_id` _sqlalchemy.Integer_ - Document id.
- `journal_action` _str_ - Journal action.

<a id="libs.db.orm.prepare_connect_db"></a>

#### prepare\_connect\_db

```python
def prepare_connect_db() -> None
```

Prepare the database connection for normal users.

<a id="libs.db.orm.select_document_file_name_sha256"></a>

#### select\_document\_file\_name\_sha256

```python
def select_document_file_name_sha256(document_id: sqlalchemy.Integer,
                                     sha256: str) -> str | None
```

Get the filename of an accepted document based on the hash key.

**Arguments**:

- `document_id` _sqlalchemy.Integer_ - Document id.
- `sha256` _str_ - Hash key.
  

**Returns**:

- `str` - The file name found.

<a id="libs.db.orm.select_run_run_id_last"></a>

#### select\_run\_run\_id\_last

```python
def select_run_run_id_last() -> int | sqlalchemy.Integer
```

Get the last run_id from database table run.

**Returns**:

- `sqlalchemy.Integer` - The last run id found.

<a id="libs.db.orm.select_version_version_unique"></a>

#### select\_version\_version\_unique

```python
def select_version_version_unique() -> str
```

Get the version number.

Get the version number from the database table `version`.

**Returns**:

- `str` - The version number found.

<a id="libs.db.orm.update_dbt_id"></a>

#### update\_dbt\_id

```python
def update_dbt_id(table_name: str, id_where: sqlalchemy.Integer,
                  columns: Dict[str, str]) -> None
```

Update a database row based on its id column.

**Arguments**:

- `table_name` _str_ - Table name.
- `id_where` _sqlalchemy.Integer_ - Content of column id.
- `columns` _Columns_ - Pairs of column name and value.

<a id="libs.db.orm.update_document_status"></a>

#### update\_document\_status

```python
def update_document_status(
    document_columns: libs.cfg.Columns,
    call_insert_journal: Callable[[str, str, sqlalchemy.Integer, str], None]
) -> None
```

Update the document and create a new journal entry.

**Arguments**:

- `document_columns` _libs.cfg.Columns_ - Columns regarding
  database table document.
- `call_insert_journal` _Callable[[str, str, sqlalchemy.Integer, str], None]_ - New entry in
  database table journal.

<a id="libs.db.orm.update_version_version"></a>

#### update\_version\_version

```python
def update_version_version(version: str) -> None
```

Update the database version number in database table version.

**Arguments**:

- `version` _str_ - New version number.

<a id="libs.db"></a>

# libs.db

Package libs.db: DCR Database Processing.

<a id="libs.inbox"></a>

# libs.inbox

Module libs.inbox: Check, distribute and process incoming documents.

New documents are made available in the file directory inbox. These are
then checked and moved to the accepted or rejected file directories
depending on the result of the check. Depending on the file format, the
accepted documents are then converted into the pdf file format either
with the help of Pandoc and TeX Live or with the help of Tesseract OCR.

<a id="libs.inbox.check_and_create_directories"></a>

#### check\_and\_create\_directories

```python
def check_and_create_directories() -> None
```

Check the inbox file directories and create the missing ones.

The file directory inbox must exist. The two file directories
inbox_accepted and inbox_rejected are created if they do not already
exist.

<a id="libs.inbox.create_directory"></a>

#### create\_directory

```python
def create_directory(directory_type: str, directory_name: str) -> None
```

Create a new file directory if it does not already exist.

**Arguments**:

- `directory_type` _str_ - Directory type.
- `directory_name` _str_ - Directory name - may include a path.

<a id="libs.inbox.initialise_document_base"></a>

#### initialise\_document\_base

```python
def initialise_document_base(file: pathlib.Path) -> None
```

Initialise the base document in the database and in the journal.

Analyses the file name and creates an entry in each of the two database
tables document and journal.

**Arguments**:

- `file` _pathlib.Path_ - File.

<a id="libs.inbox.prepare_document_base"></a>

#### prepare\_document\_base

```python
def prepare_document_base(file: pathlib.Path) -> None
```

Prepare the base document data.

**Arguments**:

- `file` _pathlib.Path_ - File.

<a id="libs.inbox.prepare_document_child_accepted"></a>

#### prepare\_document\_child\_accepted

```python
def prepare_document_child_accepted() -> None
```

Prepare the base child document data - from inbox to inbox_accepted.

<a id="libs.inbox.prepare_pdf"></a>

#### prepare\_pdf

```python
def prepare_pdf(file: pathlib.Path) -> None
```

Prepare a new pdf document for further processing.

**Arguments**:

- `file` _pathlib.Path_ - Inbox file.

<a id="libs.inbox.process_inbox"></a>

#### process\_inbox

```python
def process_inbox() -> None
```

Process the files found in the inbox file directory.

1. Documents of type docx are converted to pdf format
   and copied to the inbox_accepted directory.
2. Documents of type pdf that do not consist only of a scanned image are
   copied unchanged to the inbox_accepted directory.
3. Documents of type pdf consisting only of a scanned image are copied
   unchanged to the inbox_ocr directory.
4. All other documents are copied to the inbox_rejected directory.

<a id="libs.inbox.process_inbox_accepted"></a>

#### process\_inbox\_accepted

```python
def process_inbox_accepted(next_step: str, journal_action: str) -> None
```

Accept a new document.

**Arguments**:

- `next_step` _str_ - Next processing step.
- `journal_action` _str_ - Journal action data.

<a id="libs.inbox.process_inbox_file"></a>

#### process\_inbox\_file

```python
def process_inbox_file(file: pathlib.Path) -> None
```

Process the next inbox file.

**Arguments**:

- `file` _pathlib.Path_ - Inbox file.

<a id="libs.inbox.process_inbox_rejected"></a>

#### process\_inbox\_rejected

```python
def process_inbox_rejected(error_code: str, journal_action: str) -> None
```

Reject a new document that is faulty.

**Arguments**:

- `error_code` _str_ - Error code.
- `journal_action` _str_ - Journal action data.

<a id="libs.pandocdcr"></a>

# libs.pandocdcr

Module libs.pandocdcr: Convert non-pdf documents to pdf files.

<a id="libs.pandocdcr.convert_non_pdf_2_pdf"></a>

#### convert\_non\_pdf\_2\_pdf

```python
def convert_non_pdf_2_pdf() -> None
```

Convert non-pdf documents to pdf files.

TBD

<a id="libs.pandocdcr.convert_non_pdf_2_pdf_file"></a>

#### convert\_non\_pdf\_2\_pdf\_file

```python
def convert_non_pdf_2_pdf_file() -> None
```

Convert a non-pdf document to a pdf file.

<a id="libs.pdf2imagedcr"></a>

# libs.pdf2imagedcr

Module libs.pdf2imagedcr: Convert scanned image pdf documents to image
files.

<a id="libs.pdf2imagedcr.convert_pdf_2_image"></a>

#### convert\_pdf\_2\_image

```python
def convert_pdf_2_image() -> None
```

Convert scanned image pdf documents to image files.

TBD

<a id="libs.pdf2imagedcr.convert_pdf_2_image_file"></a>

#### convert\_pdf\_2\_image\_file

```python
def convert_pdf_2_image_file() -> None
```

Convert a scanned image pdf document to an image file.

<a id="libs.pdf2imagedcr.prepare_document_4_tesseract"></a>

#### prepare\_document\_4\_tesseract

```python
def prepare_document_4_tesseract() -> None
```

Prepare the child document data - next step Tesseract OCR.

<a id="libs.pdflibdcr"></a>

# libs.pdflibdcr

Module libs.pdflibdcr: Extract text and metadata from pdf documents.

<a id="libs.pdflibdcr.extract_text_from_pdf"></a>

#### extract\_text\_from\_pdf

```python
def extract_text_from_pdf() -> None
```

Extract text and metadata  from pdf documents.

TBD

<a id="libs.pdflibdcr.extract_text_from_pdf_file"></a>

#### extract\_text\_from\_pdf\_file

```python
def extract_text_from_pdf_file() -> None
```

Extract text and metadata  from a pdf document.

<a id="libs.pdflibdcr.prepare_document_4_parser"></a>

#### prepare\_document\_4\_parser

```python
def prepare_document_4_parser() -> None
```

Prepare the text document data - next step Parser.

<a id="libs.tesseractdcr"></a>

# libs.tesseractdcr

Module libs.tesseractdcr: Convert image documents to pdf files.

<a id="libs.tesseractdcr.convert_image_2_pdf"></a>

#### convert\_image\_2\_pdf

```python
def convert_image_2_pdf() -> None
```

Convert image documents to pdf files.

TBD

<a id="libs.tesseractdcr.convert_image_2_pdf_file"></a>

#### convert\_image\_2\_pdf\_file

```python
def convert_image_2_pdf_file() -> None
```

Convert scanned image pdf documents to image files.

<a id="libs.utils"></a>

# libs.utils

Module libs.utils: Helper functions.

<a id="libs.utils.check_directories"></a>

#### check\_directories

```python
def check_directories() -> None
```

Check the inbox file directories.

The file directory inbox_accepted must exist.

<a id="libs.utils.compute_sha256"></a>

#### compute\_sha256

```python
def compute_sha256(file: pathlib.Path) -> str
```

Compute the SHA256 hash string of a file.

**Arguments**:

- `file` _: pathlib.Path_ - File.
  

**Returns**:

- `str` - SHA256 hash string.

<a id="libs.utils.duplicate_file_error"></a>

#### duplicate\_file\_error

```python
def duplicate_file_error(file_name: str) -> None
```

Duplicate file error.

**Arguments**:

- `file_name` __type__ - File name.

<a id="libs.utils.finalize_file_conversion"></a>

#### finalize\_file\_conversion

```python
def finalize_file_conversion(journal_action: str) -> None
```

Finalise the file conversion.

**Arguments**:

- `journal_action` _str_ - journal action.

<a id="libs.utils.initialise_document_child"></a>

#### initialise\_document\_child

```python
def initialise_document_child(journal_action: str) -> None
```

Initialise a new child document of the base document.

Prepares a new document for one of the file directories
'inbox_accepted' or 'inbox_rejected'.

**Arguments**:

- `journal_action` _str_ - Journal action data.

<a id="libs.utils.prepare_document_4_parser_tesseract"></a>

#### prepare\_document\_4\_parser\_tesseract

```python
def prepare_document_4_parser_tesseract() -> None
```

Prepare the child document data - next step parser or Tesseract OCR.

<a id="libs.utils.prepare_document_4_pdflib"></a>

#### prepare\_document\_4\_pdflib

```python
def prepare_document_4_pdflib() -> None
```

Prepare the child document data - next step PDFlib.

<a id="libs.utils.prepare_file_names"></a>

#### prepare\_file\_names

```python
def prepare_file_names(
    file_extension: str = libs.db.cfg.DOCUMENT_FILE_TYPE_PDF
) -> Tuple[str, str]
```

Prepare the source and target file names.

**Arguments**:

- `file_extension` _str_ - File extension, default value 'pdf'.
  

**Returns**:

- `Tuple(str,str)` - Source file name and target file name.

<a id="libs.utils.progress_msg"></a>

#### progress\_msg

```python
def progress_msg(msg: str) -> None
```

Create a progress message.

**Arguments**:

- `msg` _str_ - Progress message.

<a id="libs.utils.progress_msg_connected"></a>

#### progress\_msg\_connected

```python
def progress_msg_connected() -> None
```

Create a progress message: connected to database.

<a id="libs.utils.progress_msg_disconnected"></a>

#### progress\_msg\_disconnected

```python
def progress_msg_disconnected() -> None
```

Create a progress message: disconnected from database.

<a id="libs.utils.progress_msg_empty_before"></a>

#### progress\_msg\_empty\_before

```python
def progress_msg_empty_before(msg: str) -> None
```

Create a progress message.

**Arguments**:

- `msg` _str_ - Progress message.

<a id="libs.utils.reset_statistics"></a>

#### reset\_statistics

```python
def reset_statistics() -> None
```

Reset the statistic counters.

<a id="libs.utils.select_document"></a>

#### select\_document

```python
def select_document(conn: Connection, dbt: Table,
                    next_step: str) -> engine.CursorResult
```

Select the documents to be processed.

**Arguments**:

- `conn` _Connection_ - Database connection.
- `dbt` _Table_ - database table documents.
- `next_step` _str_ - Next processing step.
  

**Returns**:

- `engine.CursorResult` - The documents found.

<a id="libs.utils.select_document_prepare"></a>

#### select\_document\_prepare

```python
def select_document_prepare() -> Table
```

Prepare the selection of the documents to be processed.

**Returns**:

- `Table` - Database table document,

<a id="libs.utils.show_statistics"></a>

#### show\_statistics

```python
def show_statistics() -> None
```

Show the statistics of the run.

<a id="libs.utils.start_document_processing"></a>

#### start\_document\_processing

```python
def start_document_processing(document: Row, journal_action: str) -> None
```

Start document processing.

**Arguments**:

- `document` _Row_ - Database row document.
- `journal_action` _str_ - Journal action.

<a id="libs.utils.str_2_path"></a>

#### str\_2\_path

```python
def str_2_path(param: str) -> pathlib.Path
```

Convert a string into a file path.

**Arguments**:

- `param` _str_ - text parameter.
  

**Returns**:

- `pathlib.Path` - File path.

<a id="libs.utils.terminate_fatal"></a>

#### terminate\_fatal

```python
def terminate_fatal(error_msg: str) -> None
```

Terminate the application immediately.

**Arguments**:

- `error_msg` _str_ - Error message.

