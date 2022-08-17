from tetlib_py import *


class TET(object):

    CT_NORMAL = 0
    CT_SEQ_START = 1
    CT_SEQ_CONT = 10
    CT_INSERTED = 12

    ATTR_NONE = 0x00000000
    ATTR_SUB = 0x00000001
    ATTR_SUP = 0x00000002
    ATTR_DROPCAP = 0x00000004
    ATTR_SHADOW = 0x00000008
    ATTR_DEHYPHENATION_PRE = 0x00000010
    ATTR_DEHYPHENATION_ARTIFACT = 0x00000020
    ATTR_DEHYPHENATION_POST = 0x00000040
    ATTR_ARTIFACT = 0x00000100
    ATTR_ANNOTATION = 0x00000200
    ATTR_PATTERN = 0x00000400
    ATTR_SOFTMASK = 0x00000800

    TR_FILL = 0
    TR_STROKE = 1
    TR_FILLSTROKE = 2
    TR_INVISIBLE = 3
    TR_FILL_CLIP = 4
    TR_STROKE_CLIP = 5
    TR_FILLSTROKE_CLIP = 6
    TR_CLIP = 7

    IF_TIFF = 10
    IF_JPEG = 20
    IF_JP2 = 31
    IF_JPF = 32
    IF_J2K = 33
    IF_JBIG2 = 50

    def __init__(self):
        self.__p = None
        self.__p = TET_new()
        # don't set unicaplang, would be incompatible to TET 4.0
        # without unicaplang get_text() can return UTF8 by default
        # and UTF16/UTF32 on demand */
        if self.__p:
            TET_set_option(self.__p, "binding={python} objorient")

    # it is recommended not to use __del__ as it is not guaranteed
    # when this will be executed (see Python Esential Reference Page 94).
    # so we also implement a delete method and invalidate self.__p
    # whenever this will be called.
    def __del__(self):
        if self.__p:
            TET_delete(self.__p)

    def delete(self):
        if self.__p:
            TET_delete(self.__p)
        self.__p = None

    def close_document(self, doc):
        TET_close_document(self.__p, doc)

    def close_page(self, page):
        TET_close_page(self.__p, page)

    def convert_to_unicode(self, inputformat, inputstring, optlist):
        return TET_convert_to_unicode(self.__p, inputformat, inputstring, optlist)

    def create_pvf(self, filename, data, optlist):
        TET_create_pvf(self.__p, filename, data, optlist)

    def delete_pvf(self, filename):
        return TET_delete_pvf(self.__p, filename)

    def get_apiname(self):
        return TET_get_apiname(self.__p)

    def get_char_info(self, page):
        return TET_get_char_info(self.__p, page)

    def get_color_info(self, doc, colorid, optlist):
        return TET_get_color_info(self.__p, doc, colorid, optlist)

    def get_errmsg(self):
        return TET_get_errmsg(self.__p)

    def get_errnum(self):
        return TET_get_errnum(self.__p)

    def get_image_data(self, doc, imageid, optlist):
        return TET_get_image_data(self.__p, doc, imageid, optlist)

    def get_image_info(self, page):
        return TET_get_image_info(self.__p, page)

    def get_text(self, page):
        return TET_get_text(self.__p, page)

    def info_pvf(self, filename, keyword):
        return TET_info_pvf(self.__p, filename, keyword)

    def open_document(self, filename, optlist):
        return TET_open_document(self.__p, filename, optlist)

    def open_page(self, doc, pagenumber, optlist):
        return TET_open_page(self.__p, doc, pagenumber, optlist)

    def pcos_get_number(self, doc, path):
        return TET_pcos_get_number(self.__p, doc, path)

    def pcos_get_string(self, doc, path):
        return TET_pcos_get_string(self.__p, doc, path)

    def pcos_get_stream(self, doc, optlist, path):
        return TET_pcos_get_stream(self.__p, doc, optlist, path)

    def set_option(self, optlist):
        TET_set_option(self.__p, optlist)

    def write_image_file(self, doc, imageid, optlist):
        return TET_write_image_file(self.__p, doc, imageid, optlist)

    def process_page(self, doc, pageno, optlist):
        return TET_process_page(self.__p, doc, pageno, optlist)

    def get_tetml(self, doc, optlist):
        return TET_get_tetml(self.__p, doc, optlist)
