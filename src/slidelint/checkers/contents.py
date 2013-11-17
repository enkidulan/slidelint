""" No text found checker """

from slidelint.utils import help_wrapper
from slidelint.pdf_utils import convert_pdf_to_text

MESSAGES = (
    dict(id='W1001',
         msg_name='no-text-found',
         msg='No text found',
         help="No text found: No text found in presentation file"),)


@help_wrapper(MESSAGES)
def main(target_file=None, ):
    """ No text found checker """
    for page in convert_pdf_to_text(target_file):
        for paragraph in page:
            if paragraph:
                return []
    return [dict(id='W1001',
                 msg_name='no-text-found',
                 msg='No text found',
                 page='',
                 help="No text found: No text found in presentation file"), ]
