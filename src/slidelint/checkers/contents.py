""" No text found checker """

from slidelint.utils import help_wrapper
from slidelint.pdf_utils import convert_pdf_to_text

MESSAGES = (
    dict(id='W1001',
         msg_name='no-text-found',
         msg='No text found',
         help="No text found: No text found in presentation file"),)


def main(target_file=None, msg_info=None):
    """ No text found checker """
    if msg_info:
        return help_wrapper(MESSAGES, msg_info)
    for page in convert_pdf_to_text(target_file):
        for paragraph in page:
            if paragraph:
                return []
    return [dict(id='W1001',
                 msg_name='no-text-found',
                 msg='No text found',
                 page='',
                 help="No text found: No text found in presentation file"), ]
