# DCR - Running - Installation

![Coveralls GitHub](https://img.shields.io/coveralls/github/KonnexionsGmbH/dcr.svg)
![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/KonnexionsGmbH/dcr/0.9.0)

----

1. Clone or copy the **DCR** repository from [here](https://github.com/KonnexionsGmbH/dcr){:target="_blank"}.

2. Switch to the file directory **DCR**:

    **`cd dcr`**

3. Install the necessary Python packages by running the script  **`run_dcr_prod`** with action **`m_p`**.

4. Optionally, adjustments can be made in the following configuration files - details may be found [here](https://konnexionsgmbh.github.io/dcr/running_configuration/){:target="_blank"}:

    - **`data/initial_database_data.json`**: to configure the document languages to be used
    - **`logging_cfg.yaml`**: for the logging functionality
    - **`setup.cfg`**: for the **DCR** application in section **DCR**
 
5. Create a PostgreSQL database container by running the script **`scripts/run_setup_postgresql`** with action **`prod`**.

6. Create the **DCR** database by running the script **`run_dcr_prod`** with action **`db_c`**.
