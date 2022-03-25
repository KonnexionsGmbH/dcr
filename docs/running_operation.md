# DCR - Running - Operation

![Coveralls GitHub](https://img.shields.io/coveralls/github/KonnexionsGmbH/dcr.svg)
![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/KonnexionsGmbH/dcr/0.9.0)

----

**DCR** should be operated via the script **`run_dcr_prod`**. 
The following actions are available:

| Action      | Process                                                                                                            |
|-------------|--------------------------------------------------------------------------------------------------------------------|
| **`all`**   | Run the complete processing of all new documents.                                                                  |
| **`db_c`**  | Create the database.                                                                                               |
| **`db_u`**  | Upgrade the database.                                                                                              |
| **`m_d`**   | Run the installation of the necessary 3rd party packages <br/>for development and run the development ecosystem.   |
| **`m_p`**   | Run the installation of the necessary 3rd party packages <br/>for production and compile all packages and modules. |
| **`n_2_p`** | Convert appropriate non-pdf documents to **`pdf`** files.                                                                |
| **`ocr`**   | Convert appropriate image documents to **`pdf`** files.                                                                  |
| **`p_2_i`** | Convert **`pdf`** documents to image files.                                                                              |
| **`p_i`**   | Process the inbox directory.                                                                                       |
| **`tet`**   | Extract text and metadata from **`pdf`** documents.                                                                      |
