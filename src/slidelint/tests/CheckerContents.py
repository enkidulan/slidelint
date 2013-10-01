import os.path
import unittest
from testfixtures import compare

from slidelint.checkers import contents

here = os.path.dirname(os.path.abspath(__file__))


class TestLinterRunner(unittest.TestCase):

    def test_checker_helpers(self):
        compare(contents.main(msg_info='All'),
                [dict(id='W1001',
                      msg_name='no-text-found',
                      msg='No text found: No text found in presentation file',
                      help="No text found: No text found in presentation file",
                      page='')])
        compare(contents.main(msg_info=['W1001']),
                [dict(id='W1001',
                      msg_name='no-text-found',
                      msg='No text found: No text found in presentation file',
                      help="No text found: No text found in presentation file",
                      page='')])
        compare(contents.main(msg_info=['W8001']),
                [])

    def test_file_without_text(self):
        target_file = os.path.join(here, 'files', 'pdfs', 'empty_presentation.pdf')
        rez = contents.main(target_file=target_file)
        compare(rez,
                [dict(id='W1001', msg_name='no-text-found', msg='No text found: No text found in presentation file',help="No text found: No text found in presentation file", page='')])

    def test_file_with_text(self):
        target_file = os.path.join(here, 'files', 'pdfs', 'simple_text_presentation.pdf')
        rez = contents.main(target_file=target_file)
        compare(rez, [])
