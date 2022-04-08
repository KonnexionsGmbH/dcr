# DCR - Release Notes

![Coveralls GitHub](https://img.shields.io/coveralls/github/KonnexionsGmbH/dcr.svg)
![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/KonnexionsGmbH/dcr/0.9.1)

----

## 1. Version 0.9.1

Release Date: dd.mm.2022

### 1.1 New Features

- processing step **`s_f_p`**: Store the document structure from the parser result.
- support for documents in different languages - English, French, German and Italian as standard

### 1.2 Applied Software

| Software                                                                      | Version                | Remark                              | Status  |
|:------------------------------------------------------------------------------|:-----------------------|:------------------------------------|---------|
| DBeaver                                                                       | 22.0.2                 | for virtual machine only [optional] | upgrade |
| Docker Desktop                                                                | 20.10.14               | base version [Docker Image & VM]    | upgrade | 
| Git                                                                           | 2.25.1                 | base version                        |         |
| [Pandoc](https://pandoc.org){:target="_blank"}                                | 2.18                   |                                     | upgrade |
| [PFlib TET](https://www.pdflib.com/products/tet){:target="_blank"}            | 5.3                    |                                     |         |
| [Poppler](https://poppler.freedesktop.org){:target="_blank"}                  | 0.86.1                 | base version                        |         |
| Python3                                                                       | 3.10.4                 |                                     | upgrade |
| Python3 - pip                                                                 | 22.0.4                 |                                     |         |
| [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"} | 5.10.0                 | base version                        |         |
| [TeX Live](https://www.tug.org/texlive){:target="_blank"}                     | 2019                   | base version                        |         |
| [TeX Live](https://www.tug.org/texlive){:target="_blank"} - pdfTeX            | 3.14159265-2.6-1.40.20 | base version                        |         |

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

- Issue: The unauthenticated git protocol on port 9418 is no longer supported. [see #3](https://github.com/aleray/mdx_del_ins/issues/3){:target="_blank"}

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

new:

"Info **********  Start: Pydoc-Markdown ******************************"
pipenv run pydoc-markdown --version
python -m pydoc-markdown, version 4.6.3
pipenv run pydoc-markdown -I src/dcr --render-toc > docs/developing_api_documentation.md
Traceback (most recent call last):
  File "C:\Users\walte\.virtualenvs\dcr-v5dCJOH6\lib\site-packages\docspec_python\parser.py", line 88, in parse_to_ast
    return RefactoringTool([], options).refactor_string(code + '\n', filename)
  File "C:\Software\Python\Python310\lib\lib2to3\refactor.py", line 364, in refactor_string
    self.log_error("Can't parse %s: %s: %s",
  File "C:\Software\Python\Python310\lib\lib2to3\refactor.py", line 362, in refactor_string
    tree = self.driver.parse_string(data)
  File "C:\Software\Python\Python310\lib\lib2to3\pgen2\driver.py", line 103, in parse_string
    return self.parse_tokens(tokens, debug)
  File "C:\Software\Python\Python310\lib\lib2to3\pgen2\driver.py", line 71, in parse_tokens
    if p.addtoken(type, value, (prefix, start)):
  File "C:\Software\Python\Python310\lib\lib2to3\pgen2\parse.py", line 162, in addtoken
    raise ParseError("bad input", type, value, context)
lib2to3.pgen2.parse.ParseError: bad input: type=1, value='child_tag', context=(' ', (66, 14))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Software\Python\Python310\lib\runpy.py", line 196, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "C:\Software\Python\Python310\lib\runpy.py", line 86, in _run_code
    exec(code, run_globals)
  File "C:\Users\walte\.virtualenvs\dcr-v5dCJOH6\Scripts\pydoc-markdown.EXE\__main__.py", line 7, in <module>
  File "C:\Users\walte\.virtualenvs\dcr-v5dCJOH6\lib\site-packages\click\core.py", line 1128, in __call__
    return self.main(*args, **kwargs)
  File "C:\Users\walte\.virtualenvs\dcr-v5dCJOH6\lib\site-packages\click\core.py", line 1053, in main
    rv = self.invoke(ctx)
  File "C:\Users\walte\.virtualenvs\dcr-v5dCJOH6\lib\site-packages\click\core.py", line 1395, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "C:\Users\walte\.virtualenvs\dcr-v5dCJOH6\lib\site-packages\click\core.py", line 754, in invoke
    return __callback(*args, **kwargs)
  File "C:\Users\walte\.virtualenvs\dcr-v5dCJOH6\lib\site-packages\pydoc_markdown\main.py", line 344, in cli
    session.render(pydocmd)
  File "C:\Users\walte\.virtualenvs\dcr-v5dCJOH6\lib\site-packages\pydoc_markdown\main.py", line 136, in render
    modules = config.load_modules()
  File "C:\Users\walte\.virtualenvs\dcr-v5dCJOH6\lib\site-packages\pydoc_markdown\__init__.py", line 154, in load_modules
    modules.extend(loader.load())
  File "C:\Users\walte\.virtualenvs\dcr-v5dCJOH6\lib\site-packages\docspec_python\__init__.py", line 87, in load_python_modules
    yield parse_python_module(filename, module_name=module_name, options=options, encoding=encoding)
  File "C:\Users\walte\.virtualenvs\dcr-v5dCJOH6\lib\site-packages\docspec_python\__init__.py", line 128, in parse_python_module
    return parse_python_module(fpobj, fp, module_name, options, encoding)
  File "C:\Users\walte\.virtualenvs\dcr-v5dCJOH6\lib\site-packages\docspec_python\__init__.py", line 132, in parse_python_module
    ast = parser.parse_to_ast(fp.read(), filename)
  File "C:\Users\walte\.virtualenvs\dcr-v5dCJOH6\lib\site-packages\docspec_python\parser.py", line 90, in parse_to_ast
    raise ParseError(exc.msg, exc.type, exc.value, tuple(exc.context) + (filename,))
lib2to3.pgen2.parse.ParseError: bad input: type=1, value='child_tag', context=(' ', (66, 14), 'src\\dcr\\libs\\parser.py')
make: *** [pydoc-markdown] Fehler 1

### <a name="issues_tesseract_ocr"></a> 2.4 [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"}

- Issue: Images of type 'jp2': Error in pixReadStreamJp2k: version 2.3.0: differs from minor = 2 ... [see #57](https://github.com/UB-Mannheim/tesseract/issues/57){:target="_blank"}

```
Issue (ocr): Converting the file 'D:\SoftDevelopment\Projects\dcr\data\inbox_accepted\pdf_scanned_03_ok_5.jp2' to the file 'D:\SoftDevelopment\Projects\dcr\data\inbox_accepted\pdf_scanned_03_ok_5.pdf' with Tesseract OCR failed - error status: '1' - error: 'Error in pixReadStreamJp2k: version 2.3.0: differs from minor = 2 Error in pixReadStream: jp2: no pix returned Error in pixRead: pix not read Error during processing.'.
```
