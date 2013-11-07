""" utils for working with pdf file"""
from io import BytesIO
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import (
    PDFResourceManager,
    PDFPageInterpreter,
    process_pdf
)
from pdfminer.converter import PDFPageAggregator, TextConverter
from pdfminer.layout import LAParams, LTChar, LTTextLine, LTTextBox
import string
from itertools import ifilter, imap


def split_to_sentences_per_pages(text):
    """ splitting pdfminer outputted text into list of pages and cleanup
    paragraphs"""
    def split_into_sentences(line):
        """cleanup paragraphs"""
        return ifilter(None, (i.strip() for i in line.split('\n\n')))
    return ifilter(None, imap(split_into_sentences, text.split('\x0c')))


def convert_pdf_to_text(path):
    """ converting full PDF document to simple text """
    rsrcmgr = PDFResourceManager()
    retstr = BytesIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    with open(path, 'rb') as source_file:
        process_pdf(rsrcmgr, device, source_file)
    device.close()
    # returning only printable symbols for simplifying
    text = "".join(j for j in retstr.getvalue() if j in string.printable)
    retstr.close()
    return split_to_sentences_per_pages(text)


def layout_characters(layout):
    """ provides characters information """
    for item in layout:
        if isinstance(item, LTChar):
            # no need to yield 'invisible' symbols
            # pylint: disable=W0212
            if len(item._text) == 1:
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
    parser = PDFParser(open(path, 'rb'))
    doc = PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for num, page in enumerate(doc.get_pages()):
        interpreter.process_page(page)
        yield num, device.get_result()
