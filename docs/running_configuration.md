# DCR - Running - Configuration

![Coveralls GitHub](https://img.shields.io/coveralls/github/KonnexionsGmbH/dcr.svg)
![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/KonnexionsGmbH/dcr/0.9.0)

----

## 1. **`data/initial_database_dat.json`**

This file contains the initial values relating to the database table **`language`**.
The existing entries can be modified or deleted, but new entries can also be added.

**Syntax**:

    {
      "apiVersion": "9.9.9",
      "data": {
        "tables": [
          {
            "tableName": "language",
            "rows": [
              {
                "row": [
                  {
                    "columnName": "active",
                    "columnValue": true | false
                  },
                  {
                    "columnName": "code_iso_639_3",
                    "columnValue": "deu"
                  },
                  {
                    "columnName": "code_spacy",
                    "columnValue": "..."
                  },
                  {
                    "columnName": "code_tesseract",
                    "columnValue": "..."
                  },
                  {
                    "columnName": "directory_name_inbox",
                    "columnValue": null | "..."
                  },
                  {
                    "columnName": "iso_language_name",
                    "columnValue": "..."
                  }
                ]
              },
              ...
            ]
          }
        ]
      }
    }

**Example entry for a language**:

    {
      "row": [
        {
          "columnName": "active",
          "columnValue": false
        },
        {
          "columnName": "code_iso_639_3",
          "columnValue": "fra"
        },
        {
          "columnName": "code_spacy",
          "columnValue": "fr"
        },
        {
          "columnName": "code_tesseract",
          "columnValue": "fra"
        },
        {
          "columnName": "directory_name_inbox",
          "columnValue": null
        },
        {
          "columnName": "iso_language_name",
          "columnValue": "French"
        }
      ]
    },

## 2. **`logging_cfg.yaml`**

This file controls the logging behaviour of the application. 

**Deault content**:

    version: 1
    
    formatters:
      simple:
        format: "%(asctime)s [%(module)s.py  ] %(levelname)-5s %(funcName)s:%(lineno)d %(message)s"
      extended:
        format: "%(asctime)s [%(module)s.py  ] %(levelname)-5s %(funcName)s:%(lineno)d \n%(message)s"
    
    handlers:
      console:
        class: logging.StreamHandler
        level: INFO
        formatter: simple
    
      file_handler:
        class: logging.FileHandler
        level: INFO
        filename: run_dcr_debug.log
        formatter: extended
    
    loggers:
      dcr.py:
        handlers: [ console ]
    root:
      handlers: [ file_handler ]

## 3. **`setup.cfg`**

This file controls the behaviour of the **DCR** application. 

The customisable entries are:

    [dcr]
    db_connection_prefix = postgresql+psycopg2://
    db_container_port = 5432
    db_dialect = postgresql
    db_host = localhost
    db_password = postgresql
    db_password_admin = postgresql
    db_schema = dcr_schema
    db_user = dcr_user
    db_user_admin = dcr_user_admin
    dcr_version = 0.9.0
    delete_auxiliary_files = false
    directory_inbox = data/inbox
    directory_inbox_accepted = data/inbox_accepted
    directory_inbox_rejected = data/inbox_rejected
    ignore_duplicates = false
    initial_database_data = data/initial_database_data.json
    pdf2image_type = jpeg
    simulate_parser = false
    tesseract_timeout = 10
    verbose = true
    verbose_parser = none

| Parameter                | Default value                         | Description                                                                                 |
|--------------------------|---------------------------------------|---------------------------------------------------------------------------------------------|
| db_connection_port       | environment specific                  | port number the DBMS server is listening on                                                 |
| db_connection_prefix     | **`postgresql+psycopg2://`**          | front part of the database URL                                                              |
| db_database              | environment specific                  | **DCR** database name                                                                       |
| db_database_admin        | environment specific                  | administrative database name                                                                |
| db_dialect               | **`postgresql`**                      | DBMS used, currently: only PostgreSQL allowed                                               |
| db_host                  | **`localhost`**                       | host name of the DBMS server                                                                |
| db_password              | **`postgresql`**                      | **DCR** database user password                                                              |
| db_password_admin        | **`postgresql`**                      | administrative database password                                                            |
| db_schema                | **`dcr_schema`**                      | database schema name                                                                        |
| db_user                  | **`postgresql`**                      | **DCR** database user name                                                                  |
| db_user_admin            | **`postgresql`**                      | administrative database user name                                                           |
| dcr_version              | **`09.0`**                            | current version number of the **DCR** application                                           |
| delete_auxiliary_files   | **`true`**                            | delete the auxiliary files after a successful <br>processing step                           |
| directory_inbox          | **`data/inbox`**                      | directory for the new documents received                                                    |
| directory_inbox_accepted | **`data/inbox_accepted`**             | directory for the accepted documents                                                        |
| directory_inbox_rejected | **`data/inbox_rejected`**             | Complete file name for the JSON file with the <br>database initialisation data              |
| ignore_duplicates        | **`false`**                           | accept presumably duplicated documents <br/>based on a SHA256 hash key                      |
| initial_database_data    | **`data/initial_database_data.json`** | file with initial database contents                                                         |
| pdfimage_type            | **`jpeg`**                            | format of the image files for the scanned <br/>`pdf` document: **`jpeg`** or **`pdf`**      |
| simulate_parser          | **`false`**                           | simulate the parsing process for testing purposes                                                                 |
| tesseract_timeout        | **`10`**                              | terminate the tesseract job after a <br>period of time (seconds)                            |
| verbose                  | **`true`**                            | display progress messages for processing                                                    |
| verbose_parser           | **`none`**                            | display progress messages for parsing xml (TETML) : <br>**`all`**, **`none`** or **`text`** |

The configuration parameters can be set differently for the individual environments (`dev`, `prod` and `test`).

**Examples**:
      
      [dcr_dev]
      db_connection_port = 5432
      db_database = dcr_db_dev
      db_database_admin = dcr_db_dev_admin
      
      [dcr_prod]
      db_connection_port = 5433
      db_database = dcr_db_prod
      db_database_admin = dcr_db_prod_admin
      
      [dcr_test]
      db_connection_port = 5434
      db_database = dcr_db_test
      db_database_admin = dcr_db_test_admin
