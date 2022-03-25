# DCR - Running - Installation

![Coveralls GitHub](https://img.shields.io/coveralls/github/KonnexionsGmbH/dcr.svg)
![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/KonnexionsGmbH/dcr/0.9.0)

----

1. Clone or copy the **DCR** repository from [here](https://github.com/KonnexionsGmbH/dcr){:target="_blank"}.

2. Switch to **DCR**:

    **`cd dcr`**

3. Install the necessary Python packages:

    **`make pipenv-prod`**

4. Create a PostgreSQL database container with the script **`scripts/run_setup_postgresql`** and action **`prod`**.

5. Create the **DCR** database with the script **`run_dcr_prod`** and action **`db_c`**.

6. Optionally, adjustments can be made in the following configuration files:

   - **`logging_cfg.yaml`**: for the logging functionality

   - **`setup.cfg`**: for the **DCR** application in section **DCR**

