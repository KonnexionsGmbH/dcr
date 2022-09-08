# DCR - Running - Configuration

![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)

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
          "columnValue": "fr_dep_news_trf"
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

**Default content**:

    version: 1
    
    formatters:
      simple:
        format: "%(asctime)s %(pathname)-80s ] %(levelname)-5s %(funcName)s:%(lineno)d %(message)s"
      extended:
        format: "%(asctime)s %(pathname)-80s ] %(levelname)-5s %(funcName)s:%(lineno)d \n%(message)s"
    
    handlers:
      console:
        class: logging.StreamHandler
        level: INFO
        formatter: simple
    
      file_handler:
        class: logging.FileHandler
        level: INFO
        filename: logging_dcr.log
        formatter: extended
    
    loggers:
      dcr:
        handlers: [ console ]
    root:
      handlers: [ file_handler ]

## 3. **`setup.cfg`**

This file controls the behaviour of the **DCR** application. 

The customisable entries are:

    [dcr]
    db_connection_port = 5432
    db_connection_prefix = postgresql+psycopg2://
    db_container_port = 5432
    db_database = dcr_db_prod
    db_database_admin = dcr_db_prod_admin
    db_dialect = postgresql
    db_host = localhost
    db_initial_data_file = data/db_initial_data_file.json
    db_password = postgresql
    db_password_admin = postgresql
    db_schema = dcr_schema
    db_user = dcr_user
    db_user_admin = dcr_user_admin
    directory_inbox_accepted = data/inbox_prod_accepted
    directory_inbox_rejected = data/inbox_prod_rejected
    doc_id_in_file_name = none
    ignore_duplicates = false

| Parameter                        | Default value                               | Description                                                                                                             |
|----------------------------------|---------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| db_connection_port               | environment specific                        | Port number the DBMS server is listening on.                                                                            |
| db_connection_prefix             | **`postgresql+psycopg2://`**                | Front part of the database URL.                                                                                         |
| db_database                      | environment specific                        | **DCR** database name.                                                                                                  |
| db_database_admin                | environment specific                        | Administrative database name.                                                                                           |
| db_dialect                       | **`postgresql`**                            | DBMS used, currently: only PostgreSQL allowed.                                                                          |
| db_host                          | **`localhost`**                             | Host name of the DBMS server.                                                                                           |
| db_initial_data_file             | **`data/db_initial_data_file.json`**        | File with initial database contents.                                                                                    |
| db_password                      | **`postgresql`**                            | **DCR** database user password.                                                                                         |
| db_password_admin                | **`postgresql`**                            | Administrative database password.                                                                                       |
| db_schema                        | **`dcr_schema`**                            | Database schema name.                                                                                                   |
| db_user                          | **`postgresql`**                            | **DCR** database user name.                                                                                             |
| db_user_admin                    | **`postgresql`**                            | Administrative database user name.                                                                                      |
| directory_inbox_accepted         | **`data/inbox_prod_accepted`**              | Directory for the accepted documents.                                                                                   |
| directory_inbox_rejected         | **`data/inbox_prod_rejected`**              | Complete file name for the **`JSON`** file with the <br>database initialisation data.                                   |
| doc_id_in_file_name              | **`none`**                                  | Position of the document id in the file name : <br>**`after`**, **`before`** or **`none`**.                             |
| ignore_duplicates                | **`false`**                                 | Accept presumably duplicated documents <br/>based on a SHA256 hash key.                                                 |

The configuration parameters can be set differently for the individual environments (`dev`, `prod` and `test`).

**Examples**:
      
    [dcr.env.dev]
    db_connection_port = 5433
    db_database = dcr_db_dev
    db_database_admin = dcr_db_dev_admin
    db_initial_data_file = data/db_initial_data_file_dev.json
    directory_inbox_accepted = data/inbox_dev_accepted
    directory_inbox_rejected = data/inbox_dev_rejected
    ...
