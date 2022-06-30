# DCR - Developing - Line Type Algorithms

![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)


The granularity of the document `line` tries to classify the individual lines.
The possible line types are :

| line type | Meaning                                           |
|-----------|---------------------------------------------------|
| b         | non-classifiable line, i.e. normal text body line |
| f         | footer line                                       |
| h         | header line                                       |
| h_9       | level 9 heading line                              |
| lb        | line of a bulleted list                           |
| ln        | line of a numbered list                           |
| tab       | line of a table                                   |
| toc       | line of a table of content                        |

The following three rule-based algorithms are used to determine the line type in the order given:

1. `headers & footers`
The headers and footers are determined by a similarity comparison of the first `lt_header_max_lines` and last `lt_footer_max_lines` lines respectively. 

2. `close together`
The elements of bulleted or numbered lists must be close together and are determined by regular expressions. 
Tables have already been marked accordingly by PDFlib TET.
A table of contents must be in the first `lt_toc_last_page` pages and consists of either a list or a table with ascending page numbers.

3. `headings`
Headings extend across the entire document and can have hierarchical structures. 
The headings are determined with rule-enriched regular expressions. 

## 1 Headers & Footers

The following parameter controls both the classification of the headers and the footers:

**`verbose_lt_headers_footers`**

Default value: **`false`** - the verbose mode is an option that provides additional details as to what the processing algorithm is doing.

### 1.1 Footers

#### 1.1.1 Parameters

The following parameters control the classification of the footers:

**`lt_footer_max_distance`**

Default value: **`3`** - The degree of similarity of rows is determined by means of the [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance){:target="_blank"}. 
The value zero stands for identical lines. 
The larger the Levenshtein distance, the more different the rows are. 
If the header lines do not contain a page numbers, then the parameter should be set to `0`.

**`lt_footer_max_lines`**

Default value: **`3`** - the number of lines from the bottom of the page to be analyzed as possible candidates for footers.
With the value zero the classification of footers is prevented.

**`spacy_ignore_line_type_footer`**

Default value: **`true`** -  determines whether the lines of this type are ignored (**true**) or not (**false**) during tokenisation.

#### 1.1.2 Algorithm

1. On all pages, the last line `n`, the line `n-1`, etc. are compared up to the maximum specified line. 
2. The Levenshtein distance is determined for each pair of lines in the specified range for each current page and the previous page.
3. The line is considered a footer if, except for pages `1` and `2` and pages `n-1` and `n`, the Levenshtein distance is not greater than the specified maximum value.

### 1.2 Headers

#### 1.2.1 Parameters

The following parameters control the classification of the headers:

**`lt_header_max_distance`**

Default value: **`3`** - the degree of similarity of rows is determined by means of the [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance){:target="_blank"}. 
The value zero stands for identical lines. 
The larger the Levenshtein distance, the more different the rows are. 
If the footer lines contain a page number, then depending on the number of pages in the document, the following values are useful:

| document pages | Levenshtein distance |
|----------------|----------------------|
 | < 10           | 1                    |
 | < 100          | 2                    |
 | < 1000         | 3                    |

**`lt_header_max_lines`**

Default value: **`3`** - the number of lines from the top of the page to be analyzed as possible candidates for headers.
A value of zero prevents the classification of headers.

**`spacy_ignore_line_type_header`**

Default value: **`true`** -  determines whether the lines of this type are ignored (**true**) or not (**false**) during tokenisation.

#### 1.2.2 Algorithm

1. On all pages, the first line, the second line, etc. are compared up to the maximum specified line. 
2. The Levenshtein distance is determined for each pair of lines in the specified range for each current page and the previous page.
3. The line is considered a header if, except for pages `1` and `2` and pages `n-1` and `n`, the Levenshtein distance is not greater than the specified maximum value.

## 2 TOC (Table of Content)

An attempt is made here to recognise a table of contents contained in the document. There are two main reasons for this:

1. there is the possibility to ignore the resulting tokens afterwards, and
2. on the other hand, the table of contents could be in the form of a table, which, however, is then not to be processed as a table in the sense of 4.3.  

### 2.1 Parameters

The following parameters control the classification of a table of contents included in the document:

**`lt_toc_last_page`**

Default value: **`3`** - sets the number of pages that will be searched for a table of contents from the beginning of the document.
A value of zero prevents the search for a table of contents.

**`lt_toc_min_entries`**

Default value: **`3`** - defines the minimum number of entries that a table of contents must contain.

**`spacy_ignore_line_type_toc`**

Default value: **`true`** -  determines whether the lines of this type are ignored (**true**) or not (**false**) during tokenisation.

**`verbose_lt_toc`**

Default value: **`false`** - the verbose mode is an option that provides additional details as to what the processing algorithm is doing.

### 2.2 Algorithm Table-based

A table with the following properties is searched for:

   - except for the first row, the last column of the table must contain an integer greater than zero,
   - the number found there must be ascending,
   - the number must not be greater than the last page number of the document, and
   - if such a table was found, then the algorithm ends here.

### 2.3 Algorithm Line-based

A block of lines with the following properties is searched here:

   - the last token from each line must contain an integer greater than zero,
   - the number found there must be ascending, and
   - the number must not be greater than the last page number of the document.

## 3 Tables

[PDFlib TET](https://www.pdflib.com/products/tet/){:target="_blank"} determines the tables contained in the **`pdf`** document and marks them accordingly in its **`xml`** output file. 
**DCR** now uses these marks to determine the line type **`tab`** and optionally to output the tables in a separate **`JSON`** file.

### 3.1 Parameters

The following parameters control the classification of the tables:

**`create_extra_file_table`**

Default value: **`true`** - if true, a **`JSON`** file named `<document_name>_table.json` is created in the file directory `data_accepted` with the identified tables.

**`lt_table_file_incl_empty_columns`**

Default value: **`true`** - if true, the empty columns are included in the **`JSON`** file `<document_name>_table.json`.

**`spacy_ignore_line_type_table`**

Default value: **`false`** -  determines whether the lines of this type are ignored (**true**) or not (**false**) during tokenisation.

**`verbose_lt_table`**

Default value: **`false`** - the verbose mode is an option that provides additional details as to what the processing algorithm is doing.

## 4 Bulleted Lists

TBD: bulleted and numbered lists which must be close together and are determined by regular expressions. 

## 5 Numbered Lists

TBD

## 6 Headings

### 6.1 Parameters

The following parameters control the classification of the headings:

**`create_extra_file_toc`**

Default value: **`true`** - if true, a **`JSON`** file named `<document_name>_toc.json` is created in the file directory `data_accepted` with the identified headings.

**`lt_heading_file_incl_no_ctx`**

Default value: **`1`** - the `n` lines following the heading are included as context into the **`JSON`** file.

**`lt_heading_file_incl_regexp`**

Default value: **`false`** - if true, the regular expression for the heading is included in the **`JSON`** file.

**`lt_heading_max_level`**

Default value: **`3`** - the maximum number of hierarchical heading levels.

**`lt_heading_min_pages`**

Default value: **`2`** - the minimum number of document pages for determining headings.

**`heading_rules_file`**

Default value: **`none`** - name of a file including file directory that contains the rules for determining the headings.
**`none`** means that the given default rules are applied.

**`lt_heading_tolerance_llx`**

Default value: **`5`** - percentage tolerance for the differences in indentation of a heading at the same level.

**`spacy_ignore_line_type_heading`**

Default value: **`false`** -  determines whether the lines of this type are ignored (**true**) or not (**false**) during tokenisation.

**`verbose_lt_heading`**

Default value: **`false`** - the verbose mode is an option that provides additional details as to what the processing algorithm is doing.

### 6.2 Heading Rules

A heading rule contains the following 5 elements:

| Nr. | element name        | description                                                                                              |
|-----|---------------------|----------------------------------------------------------------------------------------------------------|
| 1   | **`name`**          | for documentation purposes, a name that characterises the rule                                           |
| 2   | **`isFirstToken`**  | if true, the rule is applied to the first token of the line, <br/>otherwise to the beginning of the line |
| 3   | **`regexp`**        | the regular expression to be applied                                                                     |
| 4   | **`functionIsAsc`** | a comparison function for the values of the predecessor and the successor                                |
| 5   | **`startValues`**   | a list of allowed start values                                                                           |

The following comparison functions (**`functionIsAsc`**) can be used:

| function                | description                                                                                                         |
|-------------------------|---------------------------------------------------------------------------------------------------------------------|
| **`ignore`**            | no comparison is performed                                                                                          |
| **`lowercase_letters`** | two lowercase letters are compared,  <br/>whereby the ASCII difference must be exactly **`1`**                      |
| **`romans`**            | two Roman numerals are compared, <br/>whereby the difference must be exactly **`1`**                                |
| **`strings`**           | two strings are compared on ascending                                                                               |
| **`string_floats`**     | floating point numbers are compared, <br/>whereby the difference must be greater than **`0`** and less than **`1`** |
| **`string_integers`**   | two integer numbers are compared, <br/>whereby the difference must be exactly **`1`**                               |
| **`uppercase_letters`** | two uppercase letters are compared,  <br/>whereby the ASCII difference must be exactly **`1`**                      |

The following table shows the standard rules in the default processing order:

| name    | isFirstToken | regexp           | functionIsAsc      | startValues         |
|---------|--------------|------------------|--------------------|---------------------|
| (999)   | True         | `"\(\d+\)$"`     | string_integers    | `["(1)"]`           |
| (A)     | True         | `"\([A-Z]\)$"`   | uppercase_letters  | `["(A)"]`           |
| (ROM)   | True         | see a)           | romans             | `["(I)"]`           |
| (a)     | True         | `"\([a-z]\)$"`   | lowercase_letters  | `["(a)"]`           |
| (rom)   | True         | see b)           | romans             | `["(i)"]`           |
| 999)    | True         | `"\d+\)$"`       | string_integers    | `["1)"]`            |
| 999.    | True         | `"\d+\.$"`       | string_integers    | `["1."]`            |
| 999.999 | True         | `"\d+\.\d\d\d$"` | string_floats      | `["1.000, "1.001"]` |
| 999.99  | True         | `"\d+\.\d\d$"`   | string_floats      | `["1.00", "1.01"]`  |
| 999.9   | True         | `"\d+\.\d$"`     | string_floats      | `["1.0", 1.1]`      |
| A)      | True         | `"[A-Z]\)$"`     | uppercase_letters  | `["A)"]`            |
| A.      | True         | `"[A-Z]\.$"`     | uppercase_letters  | `["A, "A."]`        |
| ROM)    | True         | see c)           | romans             | `["I)"]`            |
| ROM.    | True         | see d)           | romans             | `["I."]`            |
| a)      | True         | `"[a-z]\)$"`     | lowercase_letters  | `["a)"]`            |
| a.      | True         | `"[a-z]\.$"`     | lowercase_letters  | `["a, "a."]`        |
| rom)    | True         | see e)           | romans             | `["i)"]`            |
| rom.    | True         | see f)           | romans             | `["i."]`            |

a) `"\(M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\)$"`

b) `"\(m{0,3}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})\)$"`

c) `"M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\)$"`

d) `"M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\.$"`

e) `"m{0,3}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})\)$"`

f) `"m{0,3}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})\.$"`

However, these default rules can also be overridden via a **`JSON`** file (see parameter **`heading_rules_file`**). 
An example file can be found in the file directory **`data`** with the file name **`heading_rules_test.json`**.

    {
      "lineTypeHeadingRules": [
        {
          "name": "(a)",
          "isFirstToken": true,
          "regexp": "\\([a-z]\\)$",
          "functionIsAsc": "lowercase_letters",
          "startValues": [
            "(a)"
          ]
        },
        {
          "name": "(A)",
          "isFirstToken": true,
          "regexp": "\\([A-Z]\\)$",
          "functionIsAsc": "uppercase_letters",
          "startValues": [
            "(A)"
          ]
        },

### 6.3 Algorithm

- the document is worked through page by page and within a page line by line
- for each current heading level there is an entry in a hierarchy table
- for each document line, this hierarchy table is searched from bottom to top for a matching entry

- an entry is considered to be matching if
    - the regular expression is satisfied, and
    - the indentation is within the specified tolerance (`lt_heading_tolerance_llx`), and
    - the comparison function is fulfilled

- if there is a match, the following processing steps are carried out and then the next document line is processed
    - an entry for the **`JSON`** file is optionally created
    - any existing lower entries in the hierarchy table are deleted

- if no match is found, then the given heading rules are searched in the specified order

- a heading rule is matching if
    - the regular expression is satisfied, and
    - one of the optional start values matches the document line, and
    - the new heading level is within the specified limit (`lt_heading_max_level`)

- if there is a match, the following processing steps are carried out and then the next document line is processed
    - the last heading level is increased by 1,
    - a new entry is added to the hierarchy table
    - an entry for the **`JSON`** file is optionally created
