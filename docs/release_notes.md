# DCR - Release Notes

![Coveralls GitHub](https://img.shields.io/coveralls/github/KonnexionsGmbH/dcr.svg)
![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/KonnexionsGmbH/dcr/0.6.5)

----

## 1. Version 0.6.5

Release Date: dd.mm.2022

### 1.1 New Features

- processing step **`n_2_p`**: Convert appropriate non-pdf documents to pdf files.

### 1.2 Applied Software

| Software                                                     | Version  | Remark                              | Status |
|:-------------------------------------------------------------|:---------|:------------------------------------|--------|
| DBeaver                                                      | 21.3.5   | for virtual machine only [optional] |        |
| Docker Desktop                                               | 20.10.12 | base version [Docker Image & VM]    |        | 
| Git                                                          | 2.25.1   | base version                        |        |
| [Pandoc](https://pandoc.org){:target="_blank"}               | 2.17.1.1 |                                     | new    |
| [Poppler](https://poppler.freedesktop.org){:target="_blank"} | 0.86.1   | base version                        |        |
| Python3                                                      | 3.10.2   |                                     |        |
| Python3 - pip                                                | 22.0.3   |                                     |        |

#### 1.2.1 Unix-specific Software

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


#### 1.2.2 Windows-specific Software

| Software                                                                                | Version | Remark                   | Status |
|:----------------------------------------------------------------------------------------|:--------|:-------------------------|--------|
| [Grep for Windows](http://gnuwin32.sourceforge.net/packages/grep.htm){:target="_blank"} | 2.5.4   | base version             |        |
| [Make for Windows](http://gnuwin32.sourceforge.net/packages/make.htm){:target="_blank"} | 3.81    | base version             |        |
| [sed for Windows](http://gnuwin32.sourceforge.net/packages/sed.htm){:target="_blank"}   | 4.2.1   | base version             |        |

----

### 1.3 Open issues

1. Microsoft Windows Server 2019: (see [here](#issues_windows_2019){:target="_blank"}) 

2. Pydoc-Markdown: (see [here](#issues_pydoc_markdown){:target="_blank"})

----

## 2. Detailed Open Issues

### <a name="issues_windows_2019"></a> 2.1 Microsoft Windows Server 2019

- Issue: File "C:\hostedtoolcache\windows\Python\3.10.2\x64\lib\codecs.py", line 319, in decode
    def decode(self, input, final=False)

```
    Using C:/hostedtoolcache/windows/Python/3.10.2/x64/python.exe (3.10.2) to create virtualenv...
    
    created virtual environment CPython3.10.2.final.0-64 in 6336ms
      creator CPython3Windows(dest=C:\Users\runneradmin\.virtualenvs\dcr-IVfv-Mtw, clear=False, no_vcs_ignore=False, global=False)
      seeder FromAppData(download=False, pip=bundle, setuptools=bundle, wheel=bundle, via=copy, app_data_dir=C:\Users\runneradmin\AppData\Local\pypa\virtualenv)
        added seed packages: pip==22.0.3, setuptools==60.9.3, wheel==0.37.1
      activators BashActivator,BatchActivator,FishActivator,NushellActivator,PowerShellActivator,PythonActivator
    
    
    Successfully created virtual environment!
    Virtualenv location: C:\Users\runneradmin\.virtualenvs\dcr-IVfv-Mtw
    Installing dependencies from Pipfile.lock (df9ac6)...
    To activate this project's virtualenv, run pipenv shell.
    Alternatively, run a command inside the virtualenv with pipenv run.
    python -m pipenv update --dev
    Running $ pipenv lock then $ pipenv sync.
    
    Locking [dev-packages] dependencies...
    
    
    Building requirements...
    
    Resolving dependencies...
    
    Traceback (most recent call last):
      File "C:\hostedtoolcache\windows\Python\3.10.2\x64\lib\site-packages\pipenv\utils.py", line 1129, in create_spinner
        yield sp
      File "C:\hostedtoolcache\windows\Python\3.10.2\x64\lib\site-packages\pipenv\utils.py", line 1320, in venv_resolve_deps
        c = resolve(cmd, sp, project=project)
      File "C:\hostedtoolcache\windows\Python\3.10.2\x64\lib\site-packages\pipenv\utils.py", line 1139, in resolve
        for line in iter(c.stderr.readline, ""):
      File "C:\hostedtoolcache\windows\Python\3.10.2\x64\lib\codecs.py", line 319, in decode
        def decode(self, input, final=False):
    KeyboardInterrupt
    
    
    Aborted!
```

### <a name="issues_pydoc_markdown"></a> 2.2 Pydoc-Markdown

- Issue: Please help me with combined Pydoc-Markdown and MKDocs (see [here](https://github.com/NiklasRosenstein/pydoc-markdown/discussions/243){:target="_blank"}).

```
    Traceback (most recent call last):
      File "C:\hostedtoolcache\windows\Python\3.10.2\x64\lib\site-packages\pipenv\utils.py", line 1129, in create_spinner
        yield sp
      File "C:\hostedtoolcache\windows\Python\3.10.2\x64\lib\site-packages\pipenv\utils.py", line 1320, in venv_resolve_deps
        c = resolve(cmd, sp, project=project)
      File "C:\hostedtoolcache\windows\Python\3.10.2\x64\lib\site-packages\pipenv\utils.py", line 1139, in resolve
        for line in iter(c.stderr.readline, ""):
      File "C:\hostedtoolcache\windows\Python\3.10.2\x64\lib\codecs.py", line 319, in decode
        def decode(self, input, final=False):
    KeyboardInterrupt
```
