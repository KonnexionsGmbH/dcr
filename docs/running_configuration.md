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

**Deault content**:

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
    db_connection_prefix = postgresql+psycopg2://
    db_container_port = 5432
    db_dialect = postgresql
    db_host = localhost
    db_password = postgresql
    db_password_admin = postgresql
    db_schema = dcr_schema
    db_user = dcr_user
    db_user_admin = dcr_user_admin
    dcr_version = 0.9.2
    delete_auxiliary_files = false
    directory_inbox = data/inbox
    directory_inbox_accepted = data/inbox_accepted
    directory_inbox_rejected = data/inbox_rejected
    ignore_duplicates = false
    initial_database_data = data/initial_database_data.json
    line_footer_max_distance = 3
    line_footer_max_lines = 3
    line_footer_preference = true
    line_header_max_distance = 3
    line_header_max_lines = 3
    pdf2image_type = jpeg
    simulate_parser = false
    spacy_tkn_attr_...
    tesseract_timeout = 30
    tetml_line = true
    tetml_page = false
    tetml_word = false
    verbose = true
    verbose_line_type = false
    verbose_parser = none
    
| Parameter                | Default value                         | Description                                                                                        |
|--------------------------|---------------------------------------|----------------------------------------------------------------------------------------------------|
| db_connection_port       | environment specific                  | Port number the DBMS server is listening on.                                                       |
| db_connection_prefix     | **`postgresql+psycopg2://`**          | Front part of the database URL.                                                                    |
| db_database              | environment specific                  | **DCR** database name.                                                                             |
| db_database_admin        | environment specific                  | Administrative database name.                                                                      |
| db_dialect               | **`postgresql`**                      | DBMS used, currently: only PostgreSQL allowed.                                                     |
| db_host                  | **`localhost`**                       | Host name of the DBMS server.                                                                      |
| db_password              | **`postgresql`**                      | **DCR** database user password.                                                                    |
| db_password_admin        | **`postgresql`**                      | Administrative database password.                                                                  |
| db_schema                | **`dcr_schema`**                      | Database schema name.                                                                              |
| db_user                  | **`postgresql`**                      | **DCR** database user name.                                                                        |
| db_user_admin            | **`postgresql`**                      | Administrative database user name.                                                                 |
| dcr_version              | **`0.9.2`**                           | Current version number of the **DCR** application.                                                 |
| delete_auxiliary_files   | **`true`**                            | Delete the auxiliary files after a successful <br>processing step.                                 |
| directory_inbox          | **`data/inbox`**                      | Directory for the new documents received.                                                          |
| directory_inbox_accepted | **`data/inbox_accepted`**             | Directory for the accepted documents.                                                              |
| directory_inbox_rejected | **`data/inbox_rejected`**             | Complete file name for the JSON file with the <br>database initialisation data.                    |
| ignore_duplicates        | **`false`**                           | Accept presumably duplicated documents <br/>based on a SHA256 hash key.                            |
| initial_database_data    | **`data/initial_database_data.json`** | File with initial database contents.                                                               |
| line_footer_max_distance | **`3`**                               | Maximum Levenshtein distance for a footer line.                                                    |
| line_footer_max_lines    | **`3`**                               | Maximum number of footers.                                                                         |
| line_footer_preference   | **`true`**                            | Prefer the footer lines when determining the line type.                                            |
| line_header_max_distance | **`3`**                               | Maximum Levenshtein distance for a header line.                                                    |
| line_header_max_lines    | **`3`**                               | Maximum number of headers.                                                                         |
| pdfimage_type            | **`jpeg`**                            | Format of the image files for the scanned <br/>`pdf` document: **`jpeg`** or **`pdf`**.            |
| simulate_parser          | **`false`**                           | Simulate the parsing process for testing purposes.                                                 |
| tesseract_timeout        | **`30`**                              | Terminate the tesseract job after a <br>period of time (seconds).                                  |
| tetml_line               | **`true`**                            | PDFlib TET granularity 'line'.                                                                     |
| tetml_page               | **`false`**                           | PDFlib TET granularity 'page'.                                                                     |
| tetml_word               | **`false`**                           | PDFlib TET granularity 'word'.                                                                     |
| verbose                  | **`true`**                            | Display progress messages for processing.                                                          |
| verbose_line_type        | **`false`**                           | Display progress messages for line type determination.                                             |
| verbose_parser           | **`none`**                            | Display progress messages for parsing **`xml`** (TETML) : <br>**`all`**, **`none`** or **`text`**. |

The configuration parameters can be set differently for the individual environments (`dev`, `prod` and `test`).

**Examples**:
      
    [dcr.env.dev]
    db_connection_port = 5432
    db_database = dcr_db_dev
    db_database_admin = dcr_db_dev_admin
    directory_inbox = data/inbox_dev
    directory_inbox_accepted = data/inbox_dev_accepted
    directory_inbox_rejected = data/inbox_dev_rejected
    
    [dcr.env.prod]
    db_connection_port = 5433
    db_database = dcr_db_prod
    db_database_admin = dcr_db_prod_admin
    delete_auxiliary_files = true
    verbose = false
    
    [dcr.env.test]
    db_connection_port = 5434
    db_database = dcr_db_test
    db_database_admin = dcr_db_test_admin

### 3.1 [spaCy](https://spacy.io){:target="_blank"} Token Attributes

The tokens derived from the documents can be qualified via various attributes. 
The available options are described below.

    [dcr.spacy]
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
    
| Parameter                     | Default  | Description                                                                                                    |
|-------------------------------|----------|----------------------------------------------------------------------------------------------------------------|
 | spacy_tkn_attr_cluster        | false    | Brown cluster ID.                                                                                              |
 | spacy_tkn_attr_dep_           | false    | Syntactic dependency relation.                                                                                 |
 | spacy_tkn_attr_doc            | false    | The parent document.                                                                                           |
 | spacy_tkn_attr_ent_iob_       | true     | IOB code of named entity tag.                                                                                  |
 | spacy_tkn_attr_ent_kb_id_     | false    | Knowledge base ID that refers to the named entity <br>this token is a part of, if any.                         |
 | spacy_tkn_attr_ent_type_      | true     | Named entity type.                                                                                             |
 | spacy_tkn_attr_head          | false    | The syntactic parent, or “governor”, of this token.                                                            |
 | spacy_tkn_attr_i              | true     | The index of the token within the parent document.                                                             |
 | spacy_tkn_attr_idx            | false    | The character offset of the token within the parent document.                                                  |
 | spacy_tkn_attr_is_alpha       | false    | Does the token consist of alphabetic characters?                                                               |
 | spacy_tkn_attr_is_ascii       | false    | Does the token consist of ASCII characters? <br>Equivalent to all (ord(c) < 128 for c in token.text).          |
 | spacy_tkn_attr_is_bracket     | false    | Is the token a bracket?                                                                                        |
 | spacy_tkn_attr_is_currency    | true     | Is the token a currency symbol?                                                                                |
 | spacy_tkn_attr_is_digit       | true     | Does the token consist of digits?                                                                              |
 | spacy_tkn_attr_is_left_punct  | false    | Is the token a left punctuation mark, e.g. "(" ?                                                               |
 | spacy_tkn_attr_is_lower       | false    | Is the token in lowercase? Equivalent to token.text.islower().                                                 |
 | spacy_tkn_attr_is_oov         | true     | Is the token out-of-vocabulary?                                                                                |
 | spacy_tkn_attr_is_punct       | true     | Is the token punctuation?                                                                                      |
 | spacy_tkn_attr_is_quote       | false    | Is the token a quotation mark?                                                                                 |
 | spacy_tkn_attr_is_right_punct | false    | Is the token a right punctuation mark, e.g. ")" ?                                                              |
 | spacy_tkn_attr_is_sent_end    | true     | Does the token end a sentence?                                                                                 |
 | spacy_tkn_attr_is_sent_start  | true     | Does the token start a sentence?                                                                               |
 | spacy_tkn_attr_is_space       | false    | Does the token consist of whitespace characters? <br>Equivalent to token.text.isspace().                       |
 | spacy_tkn_attr_is_stop        | true     | Is the token part of a “stop list”?                                                                            |
 | spacy_tkn_attr_is_title       | true     | Is the token in titlecase?                                                                                     |
 | spacy_tkn_attr_is_upper       | false    | Is the token in uppercase? Equivalent to token.text.isupper().                                                 |
 | spacy_tkn_attr_lang_          | false    | Language of the parent document’s vocabulary.                                                                  |
 | spacy_tkn_attr_left_edge      | false    | The leftmost token of this token’s syntactic descendants.                                                      |
 | spacy_tkn_attr_lemma_         | true     | Base form of the token, with no inflectional suffixes.                                                         |
 | spacy_tkn_attr_lex            | false    | The underlying lexeme.                                                                                         |
 | spacy_tkn_attr_lex_id         | false    | Sequential ID of the token’s lexical type, used to index into tables, e.g. for word vectors.                   |
 | spacy_tkn_attr_like_email     | true     | Does the token resemble an email address?                                                                      |
 | spacy_tkn_attr_like_num       | true     | Does the token represent a number?                                                                             |
 | spacy_tkn_attr_like_url       | true     | Does the token resemble a URL?                                                                                 |
 | spacy_tkn_attr_lower_         | false    | Lowercase form of the token text. Equivalent to Token.text.lower().                                            |
 | spacy_tkn_attr_morph          | false    | Morphological analysis.                                                                                        |
 | spacy_tkn_attr_norm_          | true     | The token’s norm, i.e. a normalized form of the token text.                                                    |
 | spacy_tkn_attr_orth_          | false    | Verbatim text content (identical to Token.text). <br>Exists mostly for consistency with the other attributes.  |
 | spacy_tkn_attr_pos_           | true     | Coarse-grained part-of-speech from the Universal POS tag set.                                                  |
 | spacy_tkn_attr_prefix_        | false    | A length-N substring from the start of the token. <br>Defaults to N=1.                                         |
 | spacy_tkn_attr_prob           | false    | Smoothed log probability estimate of token’s word type <br>(context-independent entry in the vocabulary).      |
 | spacy_tkn_attr_rank           | false    | Sequential ID of the token’s lexical type, used to index <br>into tables, e.g. for word vectors.               |
 | spacy_tkn_attr_right_edge     | false    | The rightmost token of this token’s syntactic descendants.                                                     |
 | spacy_tkn_attr_sent           | false    | The sentence span that this token is a part of.                                                                |
 | spacy_tkn_attr_sentiment      | false    | A scalar value indicating the positivity or negativity of the token.                                           |
 | spacy_tkn_attr_shape_         | false    | Transform of the token’s string to show orthographic features.                                                 |
 | spacy_tkn_attr_suffix_        | false    | Length-N substring from the end of the token. Defaults to N=3.                                                 |
 | spacy_tkn_attr_tag_           | true     | Fine-grained part-of-speech.                                                                                   |
 | spacy_tkn_attr_tensor         | false    | The token’s slice of the parent Doc’s tensor.                                                                  |
 | spacy_tkn_attr_text           | true     | Verbatim text content.                                                                                         |
 | spacy_tkn_attr_text_with_ws   | false    | Text content, with trailing space character if present.                                                        |
 | spacy_tkn_attr_vocab          | false    | The vocab object of the parent Doc.                                                                            |
 | spacy_tkn_attr_whitespace_    | true     | Trailing space character if present.                                                                           |

More information about the [spaCy](https://spacy.io){:target="_blank"} token attributes can be found [here](https://spacy.io/api/token#attributes){:target="_blank"}.
**DCR** currently supports only a subset of the possible attributes, but this can easily be extended if required.

Detailed information about the universal POS tags can be found [here](https://universaldependencies.org/u/pos/){:target="_blank"}.