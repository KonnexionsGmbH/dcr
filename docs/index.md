# DCR - Document Content Recognition

![Coveralls github](https://img.shields.io/coveralls/github/KonnexionsGmbH/dcr.svg)
![GitHub release](https://img.shields.io/github/release/KonnexionsGmbH/dcr.svg)
![GitHub Release Date](https://img.shields.io/github/release-date/KonnexionsGmbH/dcr.svg)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/KonnexionsGmbH/dcr/0.5.0.svg)

----

## 1. Introduction

Based on the paper "Unfolding the Structure of a Document using Deep Learning" ([Rahman and Finin, 2019](research.md#Rahman){:target="_blank"}), this software project attempts to automatically recognize the structure in arbitrary PDF documents and thus make them more searchable in a more qualified manner.
Documents not in PDF format are converted to PDF format using [Pandoc](https://pandoc.org){:target="_blank"}. 
Documents based on scanning which, therefore, do not contain text elements, are scanned and converted to PDF format using the [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"} software. 
This process applies to all image format files e.g. jpeg, tiff etc., as well as scanned images in PDF format.  

### 1.1 Rahman & Finin Paper

---

![](img/Screen-Shot-2020-06-03-at-1.45.33-PM.png)

---

### 1.2 DCR Architecture

---

![](img/dcr_Overview.png)

---

## 2. Requirements

### 2.1 Operating System

Continuous delivery / integration (CD/CI) runs on **`Ubunto 18.04`**, **`Ubuntu 20.04`**, **`Windows Server 2019`** and **`Windows Server 2022`**.
This means that **`DCR`** also runs under **`Windows 10`** and **`Windows 11`**. 
In this case, only the functionality of the **`grep`** and **`make`** tools must be made available, e.g. via [Grep for Windows](http://gnuwin32.sourceforge.net/packages/grep.htm) or [Make for Windows](http://gnuwin32.sourceforge.net/packages/make.htm).

### 2.2 Python

Because of the use of the new typing features, **`Python`** version [3.10](https://docs.python.org/3/whatsnew/3.10.html){:target="_blank"} or higher is required.

## 3. Installation

1. Clone or copy the **`DCR`** repository from [here](https://github.com/KonnexionsGmbH/dcr){:target="_blank"}.

2. Switch to **`DCR`**:

    **`cd dcr`**

3. Install the necessary Python packages:

    **`make inst_prod`**

4. Create or update the **`DCR`** database with the script **`run_dcr`** and action **`d_c_u`**.

5. Optionally, adjustments can be made in the following configuration files:

   - **`logging_cfg.yaml`**: for the logging functionality

   - **`setup.cfg`**: for the **`DCR`** application in section **`dcr`**

### 3.1 **`setup.cfg`**

The customisable entries are:

    [dcr] 
    database_file = data/dcr.db
    directory_inbox = data/inbox
    directory_inbox_accepted = data/inbox_accepted
    directory_inbox_rejected = data/inbox_rejected

| Parameter                | Default value             | Description                             |
|--------------------------|---------------------------|-----------------------------------------|
| database_file            | **`data/dcr.db`**         | directory and name of the database file |
| directory_inbox          | **`data/inbox`**          | directory for the unprocessed documents |
| directory_inbox_accepted | **`data/inbox_accepted`** | directory for the accepted documents    |
| directory_inbox_rejected | **`data/inbox_rejected`** | directory for the rejected documents    |

## 4. Operation

DCR should be operated via the script **`run_dcr`**. 
The following actions are available:

| Action      | Process                                                                                                           |
|-------------|-------------------------------------------------------------------------------------------------------------------|
| **`all`**   | Run the complete processing of all new documents                                                                  |
| **`d_c_u`** | Create or upgrade the database                                                                                    |
| **`m_d_e`** | Run the development ecosystem                                                                                     |
| **`m_d_i`** | Run the installation of the necessary 3rd party packages for development                                          |
| **`m_p`**   | Run the installation of the necessary 3rd party packages for production <br/>and compile all packages and modules |
| **`p_i`**   | Process input folder                                                                                              |
