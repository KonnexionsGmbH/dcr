# DCR - Developing - Data Model

![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)

## 1. Overview

Data storage is realised with the relational database management system [PostgreSQL](https://www.postgresql.org){:target="_blank"}. 
**DCR** uses the official Docker image as provided by the PostgreSQL Docker Community on DockerHub - [see here](https://hub.docker.com/_/postgres){:target="_blank"}. 
If required, a PostgreSQL Docker image can be downloaded and a PostgreSQL Docker container can be created both with the script `scripts/run_setup_postgresql`.

## 2. Database Schema

### 2.1 Entity-relationship (ER) Diagram

![](img/developing_data_model_dbt_overview_erd.png)

### 2.2 Database Table **`action`**

The database table documents all actions that have been performed on the documents.

**Example rows**:

![](img/developing_data_model_dbt_action_rows.png)

**Example columns**:

![](img/developing_data_model_dbt_action_columns.png)

**ER Diagram**:

![](img/developing_data_model_dbt_action_erd.png)

### 2.3 Database Table **`document`**

The database table documents the current status of the document.

**Example rows**:

![](img/developing_data_model_dbt_document_rows.png)

**Example columns**:

![](img/developing_data_model_dbt_document_columns.png)

**ER Diagram**:

![](img/developing_data_model_dbt_document_erd.png)

### 2.4 Database Table **`language`**

This database table controls the language-related document properties during processing.

**Example rows**:

![](img/developing_data_model_dbt_language_rows.png)

**Example columns**:

![](img/developing_data_model_dbt_language_columns.png)

**ER Diagram**:

![](img/developing_data_model_dbt_language_erd.png)

### 2.5 Database Table **`run`**

This database table documents the executed processing runs in detail.

**Example rows**:

![](img/developing_data_model_dbt_run_rows.png)

**Example columns**:

![](img/developing_data_model_dbt_run_columns.png)

**ER Diagram**:

![](img/developing_data_model_dbt_run_erd.png)

### 2.6 Database Table **`token`**

This database table contains the tokens determined by [spaCy](https://spacy.io){:target="_blank"} together with selected attributes.

**Example rows**:

![](img/developing_data_model_dbt_token_rows.png)

**Example columns**:

![](img/developing_data_model_dbt_token_columns.png)

**ER Diagram**:

![](img/developing_data_model_dbt_token_erd.png)

### 2.7 Database Table **`version`**

This database table is used to monitor the version status of the **DCR** database schema.

**Example row**:

![](img/developing_data_model_dbt_version_rows.png)

**Example column**:

![](img/developing_data_model_dbt_version_columns.png)

**ER Diagram**:

![](img/developing_data_model_dbt_version_erd.png)
