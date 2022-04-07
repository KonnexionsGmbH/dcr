# DCR - Running - Data Model

![Coveralls GitHub](https://img.shields.io/coveralls/github/KonnexionsGmbH/dcr.svg)
![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/KonnexionsGmbH/dcr/0.9.1)

----

## 1. Overview

Data storage is realised with the relational database management system [PostgreSQL](https://www.postgresql.org). 
**DCR** uses the official Docker image as provided by the PostgreSQL Docker Community on DockerHub - [see here](https://hub.docker.com/_/postgres). 
If required, a PostgreSQL container can be downloaded and created with the script `scripts/run_setup_postgresql`.

## 2. Database Schema

### 2.1 Entity-relationship (ER) Diagram

![](img/developing_data_model_dbt_overview_er.png)

#### 2.1.1 Database Table **`content`**

This database table contains the results from the parsing process.

##### a) Example Rows

![](img/developing_data_model_dbt_content_rows.png)

##### b) Example Columns

![](img/developing_data_model_dbt_content_columns.png)

##### c) Example Column **`sentence`**

![](img/developing_data_model_dbt_content_json.png)

##### d) ER Diagram

![](img/developing_data_model_dbt_content_er.png)

#### 2.1.2 Database Table **`document`**

This database table contains the document-related data.

##### a) Example Rows

![](img/developing_data_model_dbt_document_rows.png)

##### b) Example Columns

![](img/developing_data_model_dbt_document_columns.png)

##### c) Example Column **`fonts`**

![](img/developing_data_model_dbt_document_json.png)

##### d) ER Diagram

![](img/developing_data_model_dbt_document_er.png)

#### 2.1.3 Database Table **`journal`**

This database table contains document-related error message and performance data.

##### a) Example Rows

![](img/developing_data_model_dbt_journal_rows.png)

##### b) ER Diagram

![](img/developing_data_model_dbt_journal_er.png)

#### 2.1.4 Database Table **`language`**

This database table controls the language-related document properties during processing.

##### a) Example Rows

![](img/developing_data_model_dbt_language_rows.png)

##### b) ER Diagram

![](img/developing_data_model_dbt_language_er.png)

#### 2.1.5 Database Table **`run`**

This database table documents the executed processing runs in detail.

##### a) Example Rows

![](img/developing_data_model_dbt_run_rows.png)

##### b) ER Diagram

![](img/developing_data_model_dbt_run_er.png)

#### 2.1.6 Database Table **`version`**

This database table is used to monitor the version status of the **DCR** database schema.

##### a) Example Rows

![](img/developing_data_model_dbt_version_rows.png)

##### b) ER Diagram

![](img/developing_data_model_dbt_version_er.png)
