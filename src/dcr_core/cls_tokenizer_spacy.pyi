import spacy.tokens

class TokenizerSpacy:
    TokenToken = dict[str, bool | float | int | str]
    TokenTokens = list[TokenToken]

    TokenSent = dict[str, float | int | None | str | TokenTokens]
    TokenSents = list[TokenSent]

    TokenPara = dict[str, int | TokenSents]
    TokenParas = list[TokenPara]

    TokenPage = dict[str, int | TokenParas]
    TokenPages = list[TokenPage]

    TokenDocument = dict[str, int | TokenPages | str]

    def __init__(self) -> None:
        self._column_no: int = 0
        self._column_span: int = 0
        self._coord_llx: float = 0.0
        self._coord_urx: float = 0.0
        self._document_id: int = 0
        self._exist: bool = False
        self._file_name_next: str = ""
        self._file_name_orig: str = ""
        self._line_type: str = ""
        self._nlp: spacy.Language = None
        self._no_lines_footer: int = 0
        self._no_lines_header: int = 0
        self._no_lines_in_doc: int = 0
        self._no_lines_in_page: int = 0
        self._no_lines_in_para: int = 0
        self._no_lines_toc: int = 0
        self._no_pages_in_doc: int = 0
        self._no_paras_in_doc: int = 0
        self._no_paras_in_page: int = 0
        self._no_sents_in_doc: int = 0
        self._no_sents_in_page: int = 0
        self._no_tokens_in_doc: int = 0
        self._no_tokens_in_page: int = 0
        self._no_tokens_in_para: int = 0
        self._no_tokens_in_sent: int = 0
        self._page_no: int = 0
        self._para_lines: list[str] = []
        self._para_no: int = 0
        self._para_no_prev: int = 0
        self._para_text: str = ""
        self._pipeline_name: str = ""
        self._processing_ok: bool = False
        self._row_no: int = 0
        self._sent_no: int = 0
        self._sentence: str = ""
        self._token_paras: TokenizerSpacy.TokenParas = []
        self._token_sents: TokenizerSpacy.TokenSents = []
        self._token_tokens: TokenizerSpacy.TokenTokens = []
        self.token_pages: TokenizerSpacy.TokenPages = []
        ...
    def _finish_document(self) -> None: ...
    def _finish_page(self) -> None: ...
    def _finish_para(self) -> None: ...
    def _finish_sent(self) -> None: ...
    @staticmethod
    def _get_token_attributes(token: spacy.tokens.Token) -> TokenToken: ...
    def _init_document(self) -> None: ...
    def _init_page(self) -> None: ...
    def _init_para(self) -> None: ...
    def _init_sent(self) -> None: ...
    def _process_page(self) -> None: ...
    def _process_para(self) -> None: ...
    def _process_sents(self) -> None: ...
    def _process_tokens(self) -> None: ...
    def exists(self) -> bool: ...
    def process_document(
        self,
        document_id: int,
        file_name_next: str,
        file_name_orig: str,
        no_lines_footer: int,
        no_lines_header: int,
        no_lines_toc: int,
        pipeline_name: str,
    ) -> None: ...
    def processing_ok(self) -> bool: ...
