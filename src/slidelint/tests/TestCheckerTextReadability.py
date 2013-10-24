import os.path
import unittest
from testfixtures import compare

from slidelint.checkers import readability

here = os.path.dirname(os.path.abspath(__file__))


class TestContentsChecker(unittest.TestCase):

    def test_readability(self):
        target_file = os.path.join(here, 'files', 'pdfs', 'text_redability.pdf')
        rez = readability.main(target_file=target_file)
        compare(rez,
          [{'help': 'Change text or background color',
            'id': 'C3000',
            'msg': 'Text is not readable enough',
            'msg_name': 'text-readability',
            'page': '1'},
           {'help': 'Change text or background color',
            'id': 'C3000',
            'msg': 'Text is not readable enough',
            'msg_name': 'text-readability',
            'page': '4'},
           {'help': 'Change text or background color',
            'id': 'C3000',
            'msg': u'Text is not readable enough',
            'msg_name': 'text-readability',
            'page': '5'},
           {'help': 'Change text or background color',
            'id': 'C3000',
            'msg': 'Text is not readable enough',
            'msg_name': 'text-readability',
            'page': '6'}])

    def test_checker_helpers(self):
        compare(readability.main(msg_info='All'),
                [{'help': 'Change text or background color',
                  'id': 'C3000',
                  'msg': 'Change text or background color',
                  'msg_name': 'text-readability',
                  'page': ''}])
        compare(readability.main(msg_info=['W8001']),
                [])

if __name__ == '__main__':
    unittest.main()
