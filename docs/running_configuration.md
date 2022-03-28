# DCR - Running - Configuration

![Coveralls GitHub](https://img.shields.io/coveralls/github/KonnexionsGmbH/dcr.svg)
![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/KonnexionsGmbH/dcr/0.9.0)

----

## 1. **`data/initial_database_dat.json`**

The customisable entries are:

## 2. **`logging_cfg.yaml`**

The customisable entries are:

## 3. **`setup.cfg`**

The customisable entries are:

      [dcr]
      db_connection_port = see environment
      db_connection_prefix = postgresql+psycopg2://
      db_database = see environment
      db_database_admin = see environment
      db_dialect = postgresql
      db_host = localhost
      db_password = postgresql
      db_password_admin = postgresql
      db_schema = dcr_schema
      db_user = dcr_user
      db_user_admin = dcr_user_admin
      dcr_version = 0.9.0
      directory_inbox = data/inbox
      directory_inbox_accepted = data/inbox_accepted
      directory_inbox_rejected = data/inbox_rejected
      ignore_duplicates = false
      initial_database_data=data/initial_database_data.json
      pdf2image_type = jpeg
      tesseract_timeout = 10
      verbose = true
      verbose_parser = false

| Parameter                | Default value                         | Description                                                                            |
|--------------------------|---------------------------------------|----------------------------------------------------------------------------------------|
| db_connection_port       | environment specific                  | port number the DBMS server is listening on                                            |
| db_connection_prefix     | **`postgresql+psycopg2://`**          | front part of the database URL                                                         |
| db_database              | environment specific                  | **DCR** database name                                                                  |
| db_database_admin        | environment specific                  | administrative database name                                                           |
| db_dialect               | **`postgresql`**                      | DBMS used, currently: only PostgreSQL allowed                                          |
| db_host                  | **`localhost`**                       | host name of the DBMS server                                                           |
| db_password              | **`postgresql`**                      | **DCR** database user password                                                         |
| db_password_admin        | **`postgresql`**                      | administrative database password                                                       |
| db_schema                | **`dcr_schema`**                      | database schema name                                                                   |
| db_user                  | **`postgresql`**                      | **DCR** database user name                                                             |
| db_user_admin            | **`postgresql`**                      | administrative database user name                                                      |
| dcr_version              | **`09.0`**                            | current version number of the **DCR** application                                      |
| directory_inbox          | **`data/inbox`**                      | directory for the new documents received                                               |
| directory_inbox_accepted | **`data/inbox_accepted`**             | directory for the accepted documents                                                   |
| directory_inbox_rejected | **`data/initial_database_data.json`** | Complete file name for the JSON file with the database initialisation data             |
| ignore_duplicates        | **`false`**                           | accept presumably duplicated documents <br/>based on a SHA256 hash key                 |
| initial_database_data    | **`false`**                           | accept presumably duplicated documents <br/>based on a SHA256 hash key                 |
| pdfimage_type            | **`jpeg`**                            | format of the image files for the scanned <br/>`pdf` document: **`jpeg`** or **`pdf`** |
| tesseract_timeout        | **`10`**                              | terminate the tesseract job after a period of time (seconds)                           |
| verbose                  | **`true`**                            | display progress messages for processing                                               |
| verbose_parser           | **`false`**                           | display progress messages for parsing xml (TETML)                                      |

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
