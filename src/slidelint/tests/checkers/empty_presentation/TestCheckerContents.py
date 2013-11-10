"""
The *_empty_presentation.pdf files contain no text at all.
The *_presentation_with_content.pdf files contain some text.

The tests check:
  1. whether help messages are provided
  2. whether checking of *_empty_presentation.pdf files fail
  3. whether checking of *_presentation_with_content.pdf files pass
"""
import os.path
import unittest
from testfixtures import compare

from slidelint.checkers import contents

here = os.path.dirname(os.path.abspath(__file__))


class TestContentsChecker(unittest.TestCase):

    def test_file_without_text(self):
        for prefix in ('libreoffice', 'msoffice'):
            target_file = os.path.join(
                here, prefix+'_empty_presentation.pdf')
            rez = contents.main(target_file=target_file)
            compare(
                rez,
                [dict(id='W1001',
                      msg_name='no-text-found',
                      msg='No text found',
                      help="No text found: No text found in presentation file",
                      page='')]
            )

    def test_file_with_text(self):
        for prefix in ('libreoffice', 'msoffice'):
            target_file = os.path.join(
                here, prefix+'_presentation_with_content.pdf')
            rez = contents.main(target_file=target_file)
            compare(rez, [])

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

if __name__ == '__main__':
    unittest.main()
