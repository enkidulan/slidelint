from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTChar, LTTextLine, LTTextBox

messages = (
    dict(id='C1003',
         msg_name='too-close-to-edges',
         msg='Too close to edges',
         help="Too close to edges: Text should not appear close to the edges."),)


def main(target_file=None, msg_info=None):
    if msg_info:
        rez = list(messages) if msg_info == 'All' else [m for m in messages if m['id'] in msg_info]
        for m in rez:
            m['page'] = ""
            m['msg'] = m['help']
        return rez
    rez = check_edges_danger_zone(target_file)
    return rez


def check_edges_danger_zone(path):
    """ Looking through all page layouts for text and comparing it size
    to page size
    """
    # return []
    rez = []
    dist = 12
    for page_num, page_layout in document_pages_layouts(path):
        width_dist = page_layout.width / dist
        height_dist = page_layout.height / dist
        save_zone = (
            width_dist,
            height_dist,
            page_layout.width - width_dist,
            page_layout.height - height_dist)
        for character in layout_characters(page_layout):
            legal = (
                save_zone[0] < character.bbox[0],
                save_zone[1] < character.bbox[1],
                save_zone[2] > character.bbox[2],
                save_zone[3] > character.bbox[3])
            if not all(legal):
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
