from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTChar, LTTextLine, LTTextBox

messages = (
    dict(id='C1002',
         msg_name='font-to-small',
         msg='Font is to small',
         help="Font is to small: Text should take up a minimum of 1/6th the page."),)


def main(target_file=None, msg_info=None):
    if msg_info:
        rez = list(messages) if msg_info == 'All' else [m for m in messages if m['id'] in msg_info]
        for m in rez:
            m['page'] = ""
            m['msg'] = m['help']
        return rez
    rez = check_text_size(target_file)
    return rez


def check_text_size(path):
    """ Looking through all page layouts for text and comparing it size
    to page size
    """
    rez = []
    k_min_size = 6
    for page_num, page_layout in document_pages_layouts(path):
        # comparing only heights of page and text
        page_size = page_layout.height
        for character in layout_characters(page_layout):
            if character.size * k_min_size < page_size:
                msg = {}
                msg.update(messages[0])
                msg['page'] = '%s' % (page_num + 1)
                rez.append(msg)
                break
    return rez


def layout_characters(layout):
    for item in layout:
        if isinstance(item, LTChar):
            yield item
        if isinstance(item, LTTextLine):
            for i in layout_characters(item):
                yield i
        if isinstance(item, LTTextBox):
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
