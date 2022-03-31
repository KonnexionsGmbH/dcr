# DCR - Running - Data Model

![Coveralls GitHub](https://img.shields.io/coveralls/github/KonnexionsGmbH/dcr.svg)
![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/KonnexionsGmbH/dcr/0.9.0)

----

## 1. Overview

Data storage is realised with the relational database management system [PostgreSQL](https://www.postgresql.org). 
**DCR** uses the official Docker image as provided by the PostgreSQL Docker Community on DockerHub - [see here](https://hub.docker.com/_/postgres). 
If required, a PostgreSQL container can be downloaded and created with the script `scripts/run_setup_postgresql`.

## 2. Database Schema

### 2.1 Database Table **`content`**

This database table contains the results from the parsing process:

![](img/schema_dbt_content.png)

### 2.2 Database Table **`document`**

This database table contains the document-related data:

![](img/schema_dbt_document.png)

### 2.3 Database Table **`journal`**

This database table contains document-related error message and performance data:

![](img/schema_dbt_journal.png)

### 2.1 Database Table **`language`**

This database table controls the language-related document properties during processing:

![](img/schema_dbt_language.png)

### 2.1 Database Table **`run`**

This database table documents the executed processing runs in detail:

![](img/schema_dbt_run.png)

### 2.1 Database Table **`version`**

This database table is used to monitor the version status of the **DCR** database schema:

![](img/schema_dbt_version.png)
