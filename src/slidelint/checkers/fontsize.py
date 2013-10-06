from slidelint.utils import help
from slidelint.pdf_utils import document_pages_layouts, layout_characters

messages = (
    dict(id='C1002',
         msg_name='font-to-small',
         msg='Font is to small',
         help="Font is to small: Text should take up a minimum of 1/6th the page."),)


def main(target_file=None, msg_info=None, min_page_ratio='6'):
    if msg_info:
        return help(messages, msg_info)
    rez = check_text_size(target_file, min_page_ratio)
    return rez


def check_text_size(path, min_page_ratio='6'):
    """ Looking through all page layouts for text and comparing it size
    to page size
    """
    rez = []
    min_page_ratio = float(min_page_ratio)
    for page_num, page_layout in document_pages_layouts(path):
        # comparing only heights of page and text
        page_size = page_layout.height
        for character in layout_characters(page_layout):
            if character.size * min_page_ratio < page_size:
                msg = {}
                msg.update(messages[0])
                msg['page'] = '%s' % (page_num + 1)
                rez.append(msg)
                break
    return rez
