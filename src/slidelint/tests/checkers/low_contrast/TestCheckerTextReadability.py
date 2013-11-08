import os.path
import unittest
from testfixtures import compare

from slidelint.checkers import readability

here = os.path.dirname(os.path.abspath(__file__))


class TestContentsChecker(unittest.TestCase):

    def test_readability(self):
        target_file = os.path.join(here, 'text_redability.pdf')
        rez = readability.main(target_file=target_file)
        compare(
            rez,
            [{'help': 'Projectors are notorious for not having good contrast.'
                      ' Your text to too close to the background color and '
                      'might be unreadable.',
              'id': 'C3000',
              'msg': 'Low text color to background contrast.',
              'msg_name': 'text-readability',
              'page': 'Slide 1'},
             {'help': 'Projectors are notorious for not having good contrast.'
                      ' Your text to too close to the background color and '
                      'might be unreadable.',
              'id': 'C3000',
              'msg': 'Low text color to background contrast.',
              'msg_name': 'text-readability',
              'page': 'Slide 4'},
             {'help': 'Projectors are notorious for not having good contrast.'
                      ' Your text to too close to the background color and'
                      ' might be unreadable.',
              'id': 'C3000',
              'msg': u'Low text color to background contrast.',
              'msg_name': 'text-readability',
              'page': 'Slide 5'},
             {'help': 'Projectors are notorious for not having good contrast.'
                      ' Your text to too close to the background color and'
                      ' might be unreadable.',
              'id': 'C3000',
              'msg': 'Low text color to background contrast.',
              'msg_name': 'text-readability',
              'page': 'Slide 6'}])

    def test_checker_helpers(self):
        compare(
            readability.main(msg_info='All'),
            [{'help': 'Projectors are notorious for not having good contrast.',
              'id': 'C3000',
              'msg': 'Projectors are notorious for not having good contrast.',
              'msg_name': 'text-readability',
              'page': ''}])
        compare(readability.main(msg_info=['W8001']),
                [])

if __name__ == '__main__':
    unittest.main()
