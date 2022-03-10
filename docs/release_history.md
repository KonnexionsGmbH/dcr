# DCR - Release History

![Coveralls GitHub](https://img.shields.io/coveralls/github/KonnexionsGmbH/dcr.svg)
![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/KonnexionsGmbH/dcr/0.6.5)

----

## Version 0.6.0

Release Date: 04.03.2022

### 1. New Features

- Processing step **`db_u`**: Upgrade the database.
- Processing step **`p_2_i`**: Convert pdf documents into image files.

### 2. Applied Software

| Software                                                     | Version  | Remark                              | Status |
|:-------------------------------------------------------------|:---------|:------------------------------------|--------|
| DBeaver                                                      | 21.3.5   | for virtual machine only [optional] |        |
| Docker Desktop                                               | 20.10.12 | base version [Docker Image & VM]    | new    | 
| Git                                                          | 2.25.1   | base version                        |        |
| [Poppler](https://poppler.freedesktop.org){:target="_blank"} | 0.86.1   | base version                        | new    |
| Python3                                                      | 3.10.2   |                                     |        |
| Python3 - pip                                                | 22.0.3   |                                     |        |

#### 2.1 Unix-specific Software

| Software                                                        | Version        | Remark                  | Status |
|:----------------------------------------------------------------|:---------------|:------------------------|--------|
| asdf                                                            | v0.9.0-e0d27e6 | base version (optional) |        |
| cURL                                                            | 7.6.80         | base version            |        |
| dos2unix                                                        | 7.4.0          | base version            |        |
| GCC & G++                                                       | 9.3.0          | base version            |        |
| GNU Autoconf                                                    | 2.69           | base version            |        |
| GNU Automake                                                    | 1.16.1         | base version            |        |
| GNU make                                                        | 4.2.1          | base version            |        |
| [htop](https://htop.dev){:target="_blank"}                      | 3.1.2          | optional                |        |
| [OpenSSL](https://www.openssl.org){:target="_blank"}            | 1.1.1f         | base version            |        |
| [procps](https://github.com/warmchang/procps){:target="_blank"} | 3.3.16         | base version (optional)             |        |
| [tmux](https://github.com/tmux/tmux/wiki){:target="_blank"}     | 3.2a           | optional                |        |
| Ubuntu                                                          | 20.04.3 LTS    | base version            |        |
| Vim                                                             | 8.1.3741       | base version (optional) |        |
| Wget                                                            | 1.20.3         |                         |        |

#### 2.2 Windows-specific Software

| Software                                                                                | Version | Remark                   | Status |
|:----------------------------------------------------------------------------------------|:--------|:-------------------------|--------|
| [Grep for Windows](http://gnuwin32.sourceforge.net/packages/grep.htm){:target="_blank"} | 2.5.4   | base version             | new    |
| [Make for Windows](http://gnuwin32.sourceforge.net/packages/make.htm){:target="_blank"} | 3.81    | base version             | new    |
| [sed for Windows](http://gnuwin32.sourceforge.net/packages/sed.htm){:target="_blank"}   | 4.2.1   | base version             | new    |

----

## Version 0.5.0

Release Date: 14.02.2022

### 1. New Features

- Setup of the entire development infrastructure
- Creation of the first version of the user documentation
- Processing of new document arrivals in the file directory **`ìnbox`**

### 2. Applied Software

| Software         | Version        | Remark                   |
|:-----------------|:---------------|:-------------------------|
| asdf             | v0.9.0-e0d27e6 | base version             |
| cURL             | 7.6.80         | base version             |
| DBeaver          | 21.3.4         | for virtual machine only |
| dos2unix         | 7.4.0          | base version             |
| GCC & G++        | 9.3.0          | base version             |
| Git              | 2.25.1         | base version             |
| GNU Autoconf     | 2.69           | base version             |
| GNU Automake     | 1.16.1         | base version             |
| GNU make         | 4.2.1          | base version             |
| htop             | 3.1.2          |                          |
| OpenSSL          | 1.1.1f         | base version             |
| procps-ng        | 3.3.16         | base version             |
| Python3          | 3.10.2         |                          |
| Python3 - pip    | 22.0.3         |                          |
| tmux             | 3.2a           |                          |
| Ubuntu           | 20.04.3 LTS    | base version             |
| Vim              | 8.1.3741       | base version             |
| Wget             | 1.20.3         |                          |