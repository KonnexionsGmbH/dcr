Module document
===============

Functions
---------

    
`process_inbox(logger, config, _engine)`
:   Process the files in the inbox.
    
    Documents of type doc, docx or txt are converted to pdf format and copied to the inbox_accepted directory.
    
    Documents of type pdf that do not consist only of a scanned image are copied unchanged to the inbox_accepted directory.
    
    Documents of type pdf consisting only of a scanned image are copied unchanged to the inbox_ocr directory.
    
    All other documents are copied to the inbox_rejected directory.
    
    For each document an entry is created in the database table document.
    
    Args:
        logger (Logger): Default logger.
        config (dict):   Configuration parameters.
        _engine (Engine): Database state.