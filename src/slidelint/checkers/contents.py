from slidelint.utils import help
from slidelint.pdf_utils import convert_pdf_to_text

messages = (
    dict(id='W1001',
         msg_name='no-text-found',
         msg='No text found',
         help="No text found: No text found in presentation file"),)


def main(target_file=None, msg_info=None):
    if msg_info:
        return help(messages, msg_info)
    text = convert_pdf_to_text(target_file)
    rez = []
    if not text:
        for m in messages:
            page_status = {'page': ''}
            page_status.update(m)
            rez.append(page_status)
    return rez
