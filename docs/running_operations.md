# DCR - Running - Operations

![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)

**DCR** should be operated via the script **`run_dcr_prod`**. 
The following actions are available:

| Action      | Process                                                                                                            |
|-------------|--------------------------------------------------------------------------------------------------------------------|
| **`all`**   | Run the complete processing of all new documents.                                                                  |
| **`db_c`**  | Create the database.                                                                                               |
| **`db_u`**  | Upgrade the database.                                                                                              |
| **`m_d`**   | Run the installation of the necessary 3rd party packages <br/>for development and run the development ecosystem.   |
| **`m_p`**   | Run the installation of the necessary 3rd party packages <br/>for production and compile all packages and modules. |
| **`n_2_p`** | Convert non **`pdf`** documents to **`pdf`** files.                                                                |
| **`ocr`**   | Convert image documents to **`pdf`** files.                                                                        |
| **`p_2_i`** | Convert **`pdf`** documents to image files.                                                                        |
| **`p_i`**   | Process the inbox directory.                                                                                       |
| **`s_p_j`** | Store the parser result in a JSON file.                                                                           |
| **`tet`**   | Extract text from **`pdf`** documents.                                                                             |
| **`tkn`**   | Create qualified document tokens.                                                                                  |

The action **`all - run the complete processing of all new documents`** includes the following processes in the order given:

| Action      | Process                                             |
|-------------|-----------------------------------------------------|
| **`p_i`**   | Process the inbox directory.                        |
| **`p_2_i`** | Convert **`pdf`** documents to image files.         |
| **`ocr`**   | Convert image documents to **`pdf`** files.         |
| **`n_2_p`** | Convert non **`pdf`** documents to **`pdf`** files. |
| **`tet`**   | Extract text from **`pdf`** documents.              |
| **`s_p_j`** | Store the parser result in a JSON file.            |
| **`tkn`**   | Create qualified document tokens.                   |

The action **`db_c - create the database`** is only required once when installing **`DCR`**.  

The action **`db_u - upgrade the database`** is necessary once for each version change of **`DCR`**.  

The actions **`m_d`** and **`m_p`** correspond to the commands **`make pipenv-dev`** and **`make pipenv-prod`** for installing or updating the necessary Python libraries. 