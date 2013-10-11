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
                [{'help': 'It would be a honour. It was only shown on ITV and no...',
                  'id': 'C1010',
                  'msg': "misspelling - Use 'an' instead of 'a' if the following word starts with a vowel sound, e.g. 'an article', 'an hour'",
                  'msg_name': 'language-tool-EN_A_VS_AN',
                  'page': '1'},
                 {'help': 'It would be a honour. It was only shown on ITV and not B.B.C...',
                  'id': 'C1010',
                  'msg': 'misspelling - Possible spelling mistake found',
                  'msg_name': 'language-tool-MORFOLOGIK_RULE_EN_US',
                  'page': '1'},
                 {'help': '...would be a honour. It was only shown on ITV and not B.B.C.',
                  'id': 'C1010',
                  'msg': 'misspelling - Possible spelling mistake found',
                  'msg_name': 'language-tool-MORFOLOGIK_RULE_EN_US',
                  'page': '1'},
                 {'help': "...t they're coats in the cloakroom I know alot about precious stones.",
                  'id': 'C1010',
                  'msg': 'misspelling - Possible spelling mistake found',
                  'msg_name': 'language-tool-MORFOLOGIK_RULE_EN_US',
                  'page': '3'}])

    def test_checker_helpers(self):
        compare(language_tool_checker.main(msg_info='All'),
                [{'help': 'Language tool found error',
                  'id': 'C1010',
                  'msg': 'Language tool found error',
                  'msg_name': 'language-tool',
                  'page': ''}])
        compare(language_tool_checker.main(msg_info=['C1010']),
                [{'help': 'Language tool found error',
                  'id': 'C1010',
                  'msg': 'Language tool found error',
                  'msg_name': 'language-tool',
                  'page': ''}])
        compare(language_tool_checker.main(msg_info=['W8001']),
                [])

if __name__ == '__main__':
    unittest.main()
