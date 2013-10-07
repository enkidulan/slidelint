import os.path
import unittest
from testfixtures import compare

from slidelint.checkers import language_tool_checker

here = os.path.dirname(os.path.abspath(__file__))


class TestContentsChecker(unittest.TestCase):

    def test_language_tool_checker(self):
        target_file = os.path.join(here, 'files', 'pdfs', 'grammar.pdf')
        rez = language_tool_checker.main(target_file=target_file)
        compare(rez,
                [dict(id='W1001', msg_name='no-text-found', msg='No text found: No text found in presentation file',
                      help="No text found: No text found in presentation file", page='')])

    def test_checker_helpers(self):
        compare(language_tool_checker.main(msg_info='All'),
                [dict(id='W1001',
                      msg_name='no-text-found',
                      msg='No text found: No text found in presentation file',
                      help="No text found: No text found in presentation file",
                      page='')])
        compare(language_tool_checker.main(msg_info=['W1001']),
                [dict(id='W1001',
                      msg_name='no-text-found',
                      msg='No text found: No text found in presentation file',
                      help="No text found: No text found in presentation file",
                      page='')])
        compare(language_tool_checker.main(msg_info=['W8001']),
                [])

if __name__ == '__main__':
    unittest.main()
