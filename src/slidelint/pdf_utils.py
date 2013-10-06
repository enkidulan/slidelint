from io import BytesIO
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import (
    PDFResourceManager,
    PDFPageInterpreter,
    process_pdf
)
from pdfminer.converter import PDFPageAggregator, TextConverter
from pdfminer.layout import LAParams, LTChar, LTTextLine, LTTextBox


def convert_pdf_to_text(path):
    rsrcmgr = PDFResourceManager()
    retstr = BytesIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    process_pdf(rsrcmgr, device, fp)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str


def layout_characters(layout):
    for item in layout:
        if isinstance(item, LTChar):
            if ord(item._text) > 32:
                yield item
        elif isinstance(item, LTTextLine):
            for i in layout_characters(item):
                yield i
        elif isinstance(item, LTTextBox):
            for i in layout_characters(item):
                yield i


def document_pages_layouts(path):
    """ Basically read pdf document and parce it,
    yield page number and page layout
    """
    fp = open(path, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for n, page in enumerate(doc.get_pages()):
        interpreter.process_page(page)
        yield n, device.get_result()
