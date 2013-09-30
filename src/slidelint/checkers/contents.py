from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO

import re


messages = (
    dict(id='W1001',
         msg_name='no-text-found',
         msg='No text found',
         help="No text found: No text found in presentation file"),)


def main(target_file=None, msg_info=None):
    if msg_info:
        rez = list(messages) if msg_info == 'All' else [m for m in messages if m['id'] in msg_info]
        for m in rez:
            m['page'] = ""
            m['msg'] = m['help']
        return rez
    text = convert_pdf(target_file)
    rez = [] if re.findall('\w+', text) else list(messages)
    return rez


def convert_pdf(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
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
