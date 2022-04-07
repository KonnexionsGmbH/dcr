# DCR - Running - Data Model

![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)

----

## 1. Overview

Data storage is realised with the relational database management system [PostgreSQL](https://www.postgresql.org). 
**DCR** uses the official Docker image as provided by the PostgreSQL Docker Community on DockerHub - [see here](https://hub.docker.com/_/postgres). 
If required, a PostgreSQL container can be downloaded and created with the script `scripts/run_setup_postgresql`.

## 2. Database Schema

### 2.1 Entity-relationship (ER) Diagram

![](img/developing_data_model_dbt_overview_er.png)

#### 2.2 Database Tables **`content`**

#### 2.2.1 Database Table **`content`**

This database table contains the results from the parsing process.

**Example rows**:

![](img/developing_data_model_dbt_content_rows.png)

**Example columns**:

![](img/developing_data_model_dbt_content_columns.png)

**Example column `sentence`**:

![](img/developing_data_model_dbt_content_json.png)

**ER diagram**:

![](img/developing_data_model_dbt_content_er.png)

#### 2.2.2 Database Table **`document`**

This database table contains the document-related data.

**Example rows**:

![](img/developing_data_model_dbt_document_rows.png)

**Example columns**:

![](img/developing_data_model_dbt_document_columns.png)

**Example column `fonts`**:

![](img/developing_data_model_dbt_document_json.png)

**ER diagram**:

![](img/developing_data_model_dbt_document_er.png)

#### 2.2.3 Database Table **`journal`**

This database table contains document-related error message and performance data.

**Example rows**:

![](img/developing_data_model_dbt_journal_rows.png)

**ER diagram**:

![](img/developing_data_model_dbt_journal_er.png)

#### 2.2.4 Database Table **`language`**

This database table controls the language-related document properties during processing.

**Example rows**:

![](img/developing_data_model_dbt_language_rows.png)

**ER diagram**:

![](img/developing_data_model_dbt_language_er.png)

#### 2.2.5 Database Table **`run`**

This database table documents the executed processing runs in detail.

**Example rows**:

![](img/developing_data_model_dbt_run_rows.png)

**ER diagram**:

![](img/developing_data_model_dbt_run_er.png)

#### 2.2.6 Database Table **`version`**

This database table is used to monitor the version status of the **DCR** database schema.

**Example rows**:

![](img/developing_data_model_dbt_version_rows.png)

**ER diagram**:

![](img/developing_data_model_dbt_version_er.png)
