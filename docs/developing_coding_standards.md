# DCR - Developing - Coding Standards

![Coveralls GitHub](https://img.shields.io/coveralls/github/KonnexionsGmbH/dcr.svg)
![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/KonnexionsGmbH/dcr/0.9.1)

----

### 1. **`Python`**

- The [PEP 8](https://www.python.org/dev/peps/pep-0008){:target="_blank"} style guide for **`Python`** code is strictly applied and enforced with static analysis tools.
- All program code must be commented with type hinting instructions.
- All functions, modules and packages must be commented with **`Docstring`**.
- The program code must be covered as far as possible with appropriate tests - the aim is always 100 % test coverage.
- The successful execution of **`make dev`** ensures that the program code meets the required standards.

### 2. Scripts

- Scripts must always be available in identical functionality for both the Unix shell **`bash`** and the Windows command interpreter **`cmd.exe`**.
- The most important dynamic parameters of a script should be requested from the user in a dialogue.
- In the event of an error, the execution of the script must be terminated immediately.
- Apart from the main scripts, all other scripts should be present in the **`scripts`** file directory.
- The main scripts are:
    - **`run_dcr_dev`** - Running the DCR functionality for development purposes.
    - **`run_dcr_prod`** - Performing the DCR functionality for productive operation.
    