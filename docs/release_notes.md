# DCR - Release Notes

![Coveralls GitHub](https://img.shields.io/coveralls/github/KonnexionsGmbH/dcr.svg)
![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/KonnexionsGmbH/dcr/0.8.0)

----

## 1. Version 0.8.0

Release Date: 18.03.2022

### 1.1 New Features

- processing step **`tet`**: Extract text and metadata from pdf files.

### 1.2 Applied Software

| Software                                                                      | Version                | Remark                              | Status    |
|:------------------------------------------------------------------------------|:-----------------------|:------------------------------------|-----------|
| DBeaver                                                                       | 22.0.0                 | for virtual machine only [optional] |           |
| Docker Desktop                                                                | 20.10.13               | base version [Docker Image & VM]    |           | 
| Git                                                                           | 2.25.1                 | base version                        |           |
| [Pandoc](https://pandoc.org){:target="_blank"}                                | 2.17.1.1               |                                     |           |
| [PFlib TET](https://www.pdflib.com/products/tet){:target="_blank"}            | 5.3                    |                                     | new       |
| [Poppler](https://poppler.freedesktop.org){:target="_blank"}                  | 0.86.1                 | base version                        |           |
| Python3                                                                       | 3.10.3                 |                                     | upgrade   |
| Python3 - pip                                                                 | 22.0.4                 |                                     |           |
| [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"} | 5.10.0                 | base version                        |           |
| [TeX Live](https://www.tug.org/texlive){:target="_blank"}                     | 2019                   | base version                        |           |
| TeX Live - pdfTeX                                                             | 3.14159265-2.6-1.40.20 | base version                        |           |

#### 1.2.1 Unix-specific Software

| Software                                                        | Version        | Remark                    | Status |
|:----------------------------------------------------------------|:---------------|:--------------------------|--------|
| asdf                                                            | v0.9.0-e0d27e6 | base version (optional)   |        |
| cURL                                                            | 7.6.80         | base version              |        |
| dos2unix                                                        | 7.4.0          | base version              |        |
| GCC & G++                                                       | 9.4.0          | base version              |        |
| GNU Autoconf                                                    | 2.69           | base version              |        |
| GNU Automake                                                    | 1.16.1         | base version              |        |
| GNU make                                                        | 4.2.1          | base version              |        |
| [htop](https://htop.dev){:target="_blank"}                      | 3.1.2          | optional                  |        |
| [OpenSSL](https://www.openssl.org){:target="_blank"}            | 1.1.1f         | base version              |        |
| [procps](https://github.com/warmchang/procps){:target="_blank"} | 3.3.16         | base version (optional)   |        |
| [tmux](https://github.com/tmux/tmux/wiki){:target="_blank"}     | 3.2a           | optional                  |        |
| Ubuntu                                                          | 20.04.4 LTS    | base version              |        |
| Vim                                                             | 8.1.2269       | base version (optional)   |        |
| Wget                                                            | 1.20.3         |                           |        |


#### 1.2.2 Windows-specific Software

| Software                                                                                | Version | Remark                   | Status |
|:----------------------------------------------------------------------------------------|:--------|:-------------------------|--------|
| [Grep for Windows](http://gnuwin32.sourceforge.net/packages/grep.htm){:target="_blank"} | 2.5.4   | base version             |        |
| [Make for Windows](http://gnuwin32.sourceforge.net/packages/make.htm){:target="_blank"} | 3.81    | base version             |        |
| [sed for Windows](http://gnuwin32.sourceforge.net/packages/sed.htm){:target="_blank"}   | 4.2.1   | base version             |        |

----

### 1.3 Open issues

1. Del/Ins Extension for Python-Markdown: (see [here](#issues_mdx_del_ins){:target="_blank"})

2. Microsoft Windows Server 2019: (see [here](#issues_windows_2019){:target="_blank"}) 

3. Pydoc-Markdown: (see [here](#issues_pydoc_markdown){:target="_blank"})

4. Tesseract OCR: (see [here](#issues_tesseract_ocr){:target="_blank"})

----

## 2. Detailed Open Issues

### <a name="issues_mdx_del_ins"></a> 2.1 Del/Ins Extension for Python-Markdown

- Issue: The unauthenticated git protocol on port 9418 is no longer supported. [see #3](https://github.com/aleray/mdx_del_ins/issues/3)

```
    ...>pip install git+git://github.com/aleray/mdx_del_ins.git
    Collecting git+git://github.com/aleray/mdx_del_ins.git
      Cloning git://github.com/aleray/mdx_del_ins.git to c:\users\walte\appdata\local\temp\pip-req-build-z_lh5zkh
      Running command git clone --filter=blob:none --quiet git://github.com/aleray/mdx_del_ins.git 'C:\Users\walte\AppData\Local\Temp\pip-req-build-z_lh5zkh'
      fatal: remote error:
        The unauthenticated git protocol on port 9418 is no longer supported.
      Please see https://github.blog/2021-09-01-improving-git-protocol-security-github/ for more information.
      error: subprocess-exited-with-error
    
      × git clone --filter=blob:none --quiet git://github.com/aleray/mdx_del_ins.git 'C:\Users\walte\AppData\Local\Temp\pip-req-build-z_lh5zkh' did not run successfully.
      │ exit code: 128
      ╰─> See above for output.
    
      note: This error originates from a subprocess, and is likely not a problem with pip.
    error: subprocess-exited-with-error
    
    × git clone --filter=blob:none --quiet git://github.com/aleray/mdx_del_ins.git 'C:\Users\walte\AppData\Local\Temp\pip-req-build-z_lh5zkh' did not run successfully.
    │ exit code: 128
    ╰─> See above for output.
    
    note: This error originates from a subprocess, and is likely not a problem with pip.
```


### <a name="issues_windows_2019"></a> 2.2 Microsoft Windows Server 2019

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

### <a name="issues_pydoc_markdown"></a> 2.3 Pydoc-Markdown

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

### <a name="issues_tesseract_ocr"></a> 2.4 Tesseract OCR

- Issue: Images of type 'jp2': Error in pixReadStreamJp2k: version 2.3.0: differs from minor = 2 ... (**Windows 10 only**) [see #57](https://github.com/UB-Mannheim/tesseract/issues/57)

```
Issue (ocr): Converting the file 'D:\SoftDevelopment\Projects\dcr\data\inbox_accepted\pdf_scanned_03_ok_5.jp2' to the file 'D:\SoftDevelopment\Projects\dcr\data\inbox_accepted\pdf_scanned_03_ok_5.pdf' with Tesseract OCR failed - error status: '1' - error: 'Error in pixReadStreamJp2k: version 2.3.0: differs from minor = 2 Error in pixReadStream: jp2: no pix returned Error in pixRead: pix not read Error during processing.'.
```
