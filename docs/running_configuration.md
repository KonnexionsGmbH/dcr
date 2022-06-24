# DCR - Running - Configuration

![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)

## 1. **`data/initial_database_dat.json`**

This file contains the initial values relating to the database table **`language`**.
The existing entries can be modified or deleted, but new entries can also be added.

**Syntax**:

    {
      "apiVersion": "9.9.9",
      "data": {
        "tables": [
          {
            "tableName": "language",
            "rows": [
              {
                "row": [
                  {
                    "columnName": "active",
                    "columnValue": true | false
                  },
                  {
                    "columnName": "code_iso_639_3",
                    "columnValue": "deu"
                  },
                  {
                    "columnName": "code_spacy",
                    "columnValue": "..."
                  },
                  {
                    "columnName": "code_tesseract",
                    "columnValue": "..."
                  },
                  {
                    "columnName": "directory_name_inbox",
                    "columnValue": null | "..."
                  },
                  {
                    "columnName": "iso_language_name",
                    "columnValue": "..."
                  }
                ]
              },
              ...
            ]
          }
        ]
      }
    }

**Example entry for a language**:

    {
      "row": [
        {
          "columnName": "active",
          "columnValue": false
        },
        {
          "columnName": "code_iso_639_3",
          "columnValue": "fra"
        },
        {
          "columnName": "code_spacy",
          "columnValue": "fr_dep_news_trf"
        },
        {
          "columnName": "code_tesseract",
          "columnValue": "fra"
        },
        {
          "columnName": "directory_name_inbox",
          "columnValue": null
        },
        {
          "columnName": "iso_language_name",
          "columnValue": "French"
        }
      ]
    },

## 2. **`logging_cfg.yaml`**

This file controls the logging behaviour of the application. 

**Default content**:

    version: 1
    
    formatters:
      simple:
        format: "%(asctime)s [%(module)s.py  ] %(levelname)-5s %(funcName)s:%(lineno)d %(message)s"
      extended:
        format: "%(asctime)s [%(module)s.py  ] %(levelname)-5s %(funcName)s:%(lineno)d \n%(message)s"
    
    handlers:
      console:
        class: logging.StreamHandler
        level: INFO
        formatter: simple
    
      file_handler:
        class: logging.FileHandler
        level: INFO
        filename: run_dcr_debug.log
        formatter: extended
    
    loggers:
      dcr.py:
        handlers: [ console ]
    root:
      handlers: [ file_handler ]

## 3. **`setup.cfg`**

This file controls the behaviour of the **DCR** application. 

The customisable entries are:

    [dcr]
    db_connection_port = 5432
    db_connection_prefix = postgresql+psycopg2://
    db_container_port = 5432
    db_database = dcr_db_prod
    db_database_admin = dcr_db_prod_admin
    db_dialect = postgresql
    db_host = localhost
    db_password = postgresql
    db_password_admin = postgresql
    db_schema = dcr_schema
    db_user = dcr_user
    db_user_admin = dcr_user_admin
    delete_auxiliary_files = true
    directory_inbox = data/inbox_prod
    directory_inbox_accepted = data/inbox_prod_accepted
    directory_inbox_rejected = data/inbox_prod_rejected
    doc_id_in_file_name = none
    heading_max_level = 3
    heading_min_pages = 2
    heading_rule_file = none
    heading_toc_create = true
    heading_toc_incl_no_ctx = 1
    heading_toc_incl_regexp = false
    heading_tolerance_x = 5
    ignore_duplicates = false
    initial_database_data = data/initial_database_data.json
    json_indent = 4
    json_sort_keys = false
    line_footer_max_distance = 3
    line_footer_max_lines = 3
    line_header_max_distance = 3
    line_header_max_lines = 3
    pdf2image_type = jpeg
    tesseract_timeout = 30
    tetml_page = false
    tetml_word = false
    toc_last_page = 5
    toc_min_entries = 5
    tokenize_2_database = true
    tokenize_2_jsonfile = true
    verbose = true
    verbose_line_type_headers_footers = false
    verbose_line_type_heading = false
    verbose_line_type_toc = false
    verbose_parser = none

| Parameter                         | Default value                           | Description                                                                                                     |
|-----------------------------------|-----------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| db_connection_port                | environment specific                    | Port number the DBMS server is listening on.                                                                    |
| db_connection_prefix              | **`postgresql+psycopg2://`**            | Front part of the database URL.                                                                                 |
| db_database                       | environment specific                    | **DCR** database name.                                                                                          |
| db_database_admin                 | environment specific                    | Administrative database name.                                                                                   |
| db_dialect                        | **`postgresql`**                        | DBMS used, currently: only PostgreSQL allowed.                                                                  |
| db_host                           | **`localhost`**                         | Host name of the DBMS server.                                                                                   |
| db_password                       | **`postgresql`**                        | **DCR** database user password.                                                                                 |
| db_password_admin                 | **`postgresql`**                        | Administrative database password.                                                                               |
| db_schema                         | **`dcr_schema`**                        | Database schema name.                                                                                           |
| db_user                           | **`postgresql`**                        | **DCR** database user name.                                                                                     |
| db_user_admin                     | **`postgresql`**                        | Administrative database user name.                                                                              |
| delete_auxiliary_files            | **`true`**                              | Delete the auxiliary files after a successful <br>processing step.                                              |
| directory_inbox                   | **`data/inbox_prod`**                   | Directory for the new documents received.                                                                       |
| directory_inbox_accepted          | **`data/inbox_prod_accepted`**          | Directory for the accepted documents.                                                                           |
| directory_inbox_rejected          | **`data/inbox_prod_rejected`**          | Complete file name for the **`JSON`** file with the <br>database initialisation data.                           |
| doc_id_in_file_name               | **`none`**                              | Position of the document id in the file name : <br>**`after`**, **`before`** or **`none`**.                     |
| heading_max_level                 | **`3`**                                 | Maximum level of the heading structure.                                                                         |
| heading_min_pages                 | **`2`**                                 | Minimum number of pages to determine the headings.                                                              |
| heading_rule_file                 | **`data/line_type_heading_rules.json`** | File with rules to determine the headings.                                                                      |
| heading_toc_create                | **`true`**                              | Create a separate **`JSON`** file with the table of contents.                                                   |
| heading_toc_incl_no_ctx           | **`1`**                                 | The number of lines following the heading to be included as context into the **`JSON`** file.                   |
| heading_toc_incl_regexp           | **`false`**                             | If it is set to **`true`**, the regular expression for the heading is included in the **`JSON`** file.          |
| heading_tolerance_x               | **`5`**                                 | Tolerance of vertical indentation in percent.                                                                   |
| ignore_duplicates                 | **`false`**                             | Accept presumably duplicated documents <br/>based on a SHA256 hash key.                                         |
| initial_database_data             | **`data/initial_database_data.json`**   | File with initial database contents.                                                                            |
| json_indent                       | **`4`**                                 | Improves the readability of the **`JSON`** file.                                                                |
| json_sort_keys                    | **`false`**                             | If it is set to **`true`**, the keys are set in ascending order else, <br/>they appear as in the Python object. |
| line_footer_max_distance          | **`3`**                                 | Maximum Levenshtein distance for a footer line.                                                                 |
| line_footer_max_lines             | **`3`**                                 | Maximum number of footers.                                                                                      |
| line_header_max_distance          | **`3`**                                 | Maximum Levenshtein distance for a header line.                                                                 |
| line_header_max_lines             | **`3`**                                 | Maximum number of headers.                                                                                      |
| pdfimage_type                     | **`jpeg`**                              | Format of the image files for the scanned <br/>`pdf` document: **`jpeg`** or **`pdf`**.                         |
| tesseract_timeout                 | **`30`**                                | Terminate the tesseract job after a <br>period of time (seconds).                                               |
| tetml_page                        | **`false`**                             | PDFlib TET granularity 'page'.                                                                                  |
| tetml_word                        | **`false`**                             | PDFlib TET granularity 'word'.                                                                                  |
| toc_last_page                     | **`5`**                                 | Maximum number of pages for the search of the TOC (from the beginning).                                         |
| toc_min_entries                   | **`5`**                                 | Minimum number of TOC entries.                                                                                  |
| tokenize_2_database               | **`true`**                              | Store the tokens in the database table **`token`**.                                                             |
| tokenize_2_jsonfile               | **`true`**                              | Store the tokens in a **`JSON`** flat file.                                                                     |
| verbose                           | **`true`**                              | Display progress messages for processing.                                                                       |
| verbose_line_type_headers_footers | **`false`**                             | Display progress messages for headers & footers line type determination.                                        |
| verbose_line_type_heading         | **`false`**                             | Display progress messages for heading line type determination.                                                  |
| verbose_line_type_toc             | **`false`**                             | Display progress messages for table of content line type determination.                                         |
| verbose_parser                    | **`none`**                              | Display progress messages for parsing **`xml`** (TETML) : <br>**`all`**, **`none`** or **`text`**.              |

The configuration parameters can be set differently for the individual environments (`dev`, `prod` and `test`).

**Examples**:
      
    [dcr.env.dev]
    db_connection_port = 5433
    db_database = dcr_db_dev
    db_database_admin = dcr_db_dev_admin
    db_host = localhost
    db_password = postgresql
    db_password_admin = postgresql
    db_user = dcr_user
    ...
    
## 4. **`setup.cfg`** - [spaCy](https://spacy.io){:target="_blank"} Token Attributes

The tokens derived from the documents can be qualified via various attributes. 
The available options are described below.

    [dcr.spacy]
    spacy_ignore_bracket = true
    spacy_ignore_left_punct = true
    spacy_ignore_line_type_footer = true
    spacy_ignore_line_type_header = true
    spacy_ignore_line_type_heading = false
    spacy_ignore_line_type_list_bulleted = false
    spacy_ignore_line_type_list_numbered = false
    spacy_ignore_line_type_table = false
    spacy_ignore_line_type_toc = true
    spacy_ignore_punct = true
    spacy_ignore_quote = true
    spacy_ignore_right_punct = true
    spacy_ignore_space = true
    spacy_ignore_stop = true

    spacy_tkn_attr_cluster = false
    spacy_tkn_attr_dep_ = false
    spacy_tkn_attr_doc = false
    spacy_tkn_attr_ent_iob_ = true
    spacy_tkn_attr_ent_kb_id_ = false
    spacy_tkn_attr_ent_type_ = true
    spacy_tkn_attr_head = false
    spacy_tkn_attr_i = true
    spacy_tkn_attr_idx = false
    spacy_tkn_attr_is_alpha = false
    spacy_tkn_attr_is_ascii = false
    spacy_tkn_attr_is_bracket = false
    spacy_tkn_attr_is_currency = true
    spacy_tkn_attr_is_digit = true
    spacy_tkn_attr_is_left_punct = false
    spacy_tkn_attr_is_lower = false
    spacy_tkn_attr_is_oov = true
    spacy_tkn_attr_is_punct = true
    spacy_tkn_attr_is_quote = false
    spacy_tkn_attr_is_right_punct = false
    spacy_tkn_attr_is_sent_end = true
    spacy_tkn_attr_is_sent_start = true
    spacy_tkn_attr_is_space = false
    spacy_tkn_attr_is_stop = true
    spacy_tkn_attr_is_title = true
    spacy_tkn_attr_is_upper = false
    spacy_tkn_attr_lang_ = false
    spacy_tkn_attr_left_edge = false
    spacy_tkn_attr_lemma_ = true
    spacy_tkn_attr_lex = false
    spacy_tkn_attr_lex_id = false
    spacy_tkn_attr_like_email = true
    spacy_tkn_attr_like_num = true
    spacy_tkn_attr_like_url = true
    spacy_tkn_attr_lower_ = false
    spacy_tkn_attr_morph = false
    spacy_tkn_attr_norm_ = true
    spacy_tkn_attr_orth_ = false
    spacy_tkn_attr_pos_ = true
    spacy_tkn_attr_prefix_ = false
    spacy_tkn_attr_prob = false
    spacy_tkn_attr_rank = false
    spacy_tkn_attr_right_edge = false
    spacy_tkn_attr_sent = false
    spacy_tkn_attr_sentiment = false
    spacy_tkn_attr_shape_ = false
    spacy_tkn_attr_suffix_ = false
    spacy_tkn_attr_tag_ = true
    spacy_tkn_attr_tensor = false
    spacy_tkn_attr_text = true
    spacy_tkn_attr_text_with_ws = false
    spacy_tkn_attr_vocab = false
    spacy_tkn_attr_whitespace_ = true

    spacy_ignore_line_type_footer = true
    spacy_ignore_line_type_header = true
    spacy_ignore_line_type_heading = false
    spacy_ignore_line_type_list_bulleted = false
    spacy_ignore_line_type_list_numbered = false
    spacy_ignore_line_type_table = false
    spacy_ignore_line_type_toc = true
    
| Parameter                            | Default | Description                                                                                                   |
|--------------------------------------|---------|---------------------------------------------------------------------------------------------------------------|
 | spacy_ignore_bracket                 | true    | Ignore the tokens which are brackets ?                                                                        |
 | spacy_ignore_left_punct              | true    | Ignore the tokens which are left punctuation marks, e.g. "(" ?                                                |
 | spacy_ignore_line_type_footer        | true    | Ignore the tokens from line type footer ?                                                                     |
 | spacy_ignore_line_type_header        | true    | Ignore the tokens from line type header ?                                                                     |
 | spacy_ignore_line_type_heading       | false   | Ignore the tokens from line type heading ?                                                                    |
 | spacy_ignore_line_type_list_bulleted | false   | Ignore the tokens from line type bulleted list ?                                                              |
 | spacy_ignore_line_type_list_numbered | false   | Ignore the tokens from line type numbered list ?                                                              |
 | spacy_ignore_line_type_table         | false   | Ignore the tokens from line type table ?                                                                      |
 | spacy_ignore_line_type_toc           | true    | Ignore the tokens from line type TOC ?                                                                        |
 | spacy_ignore_punct                   | true    | Ignore the tokens which are punctuations ?                                                                    |
 | spacy_ignore_quote                   | true    | Ignore the tokens which are quotation marks ?                                                                 |
 | spacy_ignore_right_punct             | true    | Ignore the tokens which are right punctuation marks, e.g. ")" ?                                               |
 | spacy_ignore_space                   | true    | Ignore the tokens which consist of whitespace characters ?                                                    |
 | spacy_ignore_stop                    | true    | Ignore the tokens which are part of a “stop list” ?                                                           |
 |                                      |         |                                                                                                               |
 | spacy_tkn_attr_cluster               | false   | Brown cluster ID.                                                                                             |
 | spacy_tkn_attr_dep_                  | false   | Syntactic dependency relation.                                                                                |
 | spacy_tkn_attr_doc                   | false   | The parent document.                                                                                          |
 | spacy_tkn_attr_ent_iob_              | true    | IOB code of named entity tag.                                                                                 |
 | spacy_tkn_attr_ent_kb_id_            | false   | Knowledge base ID that refers to the named entity <br>this token is a part of, if any.                        |
 | spacy_tkn_attr_ent_type_             | true    | Named entity type.                                                                                            |
 | spacy_tkn_attr_head                  | false   | The syntactic parent, or “governor”, of this token.                                                           |
 | spacy_tkn_attr_i                     | true    | The index of the token within the parent document.                                                            |
 | spacy_tkn_attr_idx                   | false   | The character offset of the token within the parent document.                                                 |
 | spacy_tkn_attr_is_alpha              | false   | Does the token consist of alphabetic characters?                                                              |
 | spacy_tkn_attr_is_ascii              | false   | Does the token consist of ASCII characters? <br>Equivalent to all (ord(c) < 128 for c in token.text).         |
 | spacy_tkn_attr_is_bracket            | false   | Is the token a bracket?                                                                                       |
 | spacy_tkn_attr_is_currency           | true    | Is the token a currency symbol?                                                                               |
 | spacy_tkn_attr_is_digit              | true    | Does the token consist of digits?                                                                             |
 | spacy_tkn_attr_is_left_punct         | false   | Is the token a left punctuation mark, e.g. "(" ?                                                              |
 | spacy_tkn_attr_is_lower              | false   | Is the token in lowercase? Equivalent to token.text.islower().                                                |
 | spacy_tkn_attr_is_oov                | true    | Is the token out-of-vocabulary?                                                                               |
 | spacy_tkn_attr_is_punct              | true    | Is the token punctuation?                                                                                     |
 | spacy_tkn_attr_is_quote              | false   | Is the token a quotation mark?                                                                                |
 | spacy_tkn_attr_is_right_punct        | false   | Is the token a right punctuation mark, e.g. ")" ?                                                             |
 | spacy_tkn_attr_is_sent_end           | true    | Does the token end a sentence?                                                                                |
 | spacy_tkn_attr_is_sent_start         | true    | Does the token start a sentence?                                                                              |
 | spacy_tkn_attr_is_space              | false   | Does the token consist of whitespace characters? <br>Equivalent to token.text.isspace().                      |
 | spacy_tkn_attr_is_stop               | true    | Is the token part of a “stop list”?                                                                           |
 | spacy_tkn_attr_is_title              | true    | Is the token in titlecase?                                                                                    |
 | spacy_tkn_attr_is_upper              | false   | Is the token in uppercase? Equivalent to token.text.isupper().                                                |
 | spacy_tkn_attr_lang_                 | false   | Language of the parent document’s vocabulary.                                                                 |
 | spacy_tkn_attr_left_edge             | false   | The leftmost token of this token’s syntactic descendants.                                                     |
 | spacy_tkn_attr_lemma_                | true    | Base form of the token, with no inflectional suffixes.                                                        |
 | spacy_tkn_attr_lex                   | false   | The underlying lexeme.                                                                                        |
 | spacy_tkn_attr_lex_id                | false   | Sequential ID of the token’s lexical type, used to index into tables, e.g. for word vectors.                  |
 | spacy_tkn_attr_like_email            | true    | Does the token resemble an email address?                                                                     |
 | spacy_tkn_attr_like_num              | true    | Does the token represent a number?                                                                            |
 | spacy_tkn_attr_like_url              | true    | Does the token resemble a URL?                                                                                |
 | spacy_tkn_attr_lower_                | false   | Lowercase form of the token text. Equivalent to Token.text.lower().                                           |
 | spacy_tkn_attr_morph                 | false   | Morphological analysis.                                                                                       |
 | spacy_tkn_attr_norm_                 | true    | The token’s norm, i.e. a normalized form of the token text.                                                   |
 | spacy_tkn_attr_orth_                 | false   | Verbatim text content (identical to Token.text). <br>Exists mostly for consistency with the other attributes. |
 | spacy_tkn_attr_pos_                  | true    | Coarse-grained part-of-speech from the Universal POS tag set.                                                 |
 | spacy_tkn_attr_prefix_               | false   | A length-N substring from the start of the token. <br>Defaults to N=1.                                        |
 | spacy_tkn_attr_prob                  | false   | Smoothed log probability estimate of token’s word type <br>(context-independent entry in the vocabulary).     |
 | spacy_tkn_attr_rank                  | false   | Sequential ID of the token’s lexical type, used to index <br>into tables, e.g. for word vectors.              |
 | spacy_tkn_attr_right_edge            | false   | The rightmost token of this token’s syntactic descendants.                                                    |
 | spacy_tkn_attr_sent                  | false   | The sentence span that this token is a part of.                                                               |
 | spacy_tkn_attr_sentiment             | false   | A scalar value indicating the positivity or negativity of the token.                                          |
 | spacy_tkn_attr_shape_                | false   | Transform of the token’s string to show orthographic features.                                                |
 | spacy_tkn_attr_suffix_               | false   | Length-N substring from the end of the token. Defaults to N=3.                                                |
 | spacy_tkn_attr_tag_                  | true    | Fine-grained part-of-speech.                                                                                  |
 | spacy_tkn_attr_tensor                | false   | The token’s slice of the parent Doc’s tensor.                                                                 |
 | spacy_tkn_attr_text                  | true    | Verbatim text content.                                                                                        |
 | spacy_tkn_attr_text_with_ws          | false   | Text content, with trailing space character if present.                                                       |
 | spacy_tkn_attr_vocab                 | false   | The vocab object of the parent Doc.                                                                           |
 | spacy_tkn_attr_whitespace_           | true    | Trailing space character if present.                                                                          |

More information about the [spaCy](https://spacy.io){:target="_blank"} token attributes can be found [here](https://spacy.io/api/token#attributes){:target="_blank"}.
**DCR** currently supports only a subset of the possible attributes, but this can easily be extended if required.

Detailed information about the universal POS tags can be found [here](https://universaldependencies.org/u/pos/){:target="_blank"}.