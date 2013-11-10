"""
The *_redability.pdf files contain slides with different text contrast to
background color:
  1. bad text contrast(non gray-scale) - should fail with default args
  2. good text contrast(gray on white, gray on black) - should pass with default args
  3. bad text contrast(gray on white) - should fail with default args
  4. bad text contrast(gray on black) - should fail with default args
  5. white crossed white too much - should fail with default args
  6. white almost crossed white and black almost crossed black - should pass with default args
  7. black crossed black too much - should fail with default args
  8. white text on whitish image - should fail with default args
  9. white text with background on whitish image - should pass with default args
  10. black text on blackish image - should fail with default args
  11. black text with background on blackish image - should pass with default args

The tests are checks:
  * that help messages are provided
  * that checks with default agrs work correctly
  * that checker args can be changed

"""
import os.path
import unittest
from testfixtures import compare

from slidelint.checkers import readability

here = os.path.dirname(os.path.abspath(__file__))


class TestContentsChecker(unittest.TestCase):

    def test_custom_args(self):
        # for prefix in ('msoffice', ):
        # for prefix in ('libreoffice', ):
        for prefix in ( 'msoffice', 'libreoffice'):
            target_file = os.path.join(
                here, prefix+'_redability.pdf')
            rez = readability.main(
                target_file=target_file,
                scale_regress=1.5,
                max_similarity=0.1,
                cross_range=50,
                scale_waight=1,
            )
            compare(
                rez,
                [{'help': 'Projectors are notorious for not having good contrast. Your text to too close to the background color and might be unreadable.',
                  'id': 'C3000',
                  'msg': 'Low text color to background contrast.',
                  'msg_name': 'text-readability',
                  'page': 'Slide 5'},
                 {'help': 'Projectors are notorious for not having good contrast. Your text to too close to the background color and might be unreadable.',
                  'id': 'C3000',
                  'msg': 'Low text color to background contrast.',
                  'msg_name': 'text-readability',
                  'page': 'Slide 7'},
                 {'help': 'Projectors are notorious for not having good contrast. Your text to too close to the background color and might be unreadable.',
                  'id': 'C3000',
                  'msg': 'Low text color to background contrast.',
                  'msg_name': 'text-readability',
                  'page': 'Slide 10'}])

    def test_default_args(self):
        for prefix in ('msoffice', 'libreoffice'):
            target_file = os.path.join(
                here, prefix+'_redability.pdf')
            rez = readability.main(target_file=target_file)
            compare(
                rez,
                [{'help': 'Projectors are notorious for not having good contrast. Your text to too close to the background color and might be unreadable.',
                  'id': 'C3000',
                  'msg': 'Low text color to background contrast.',
                  'msg_name': 'text-readability',
                  'page': 'Slide 1'},
                 {'help': 'Projectors are notorious for not having good contrast. Your text to too close to the background color and might be unreadable.',
                  'id': 'C3000',
                  'msg': 'Low text color to background contrast.',
                  'msg_name': 'text-readability',
                  'page': 'Slide 3'},
                 {'help': 'Projectors are notorious for not having good contrast. Your text to too close to the background color and might be unreadable.',
                  'id': 'C3000',
                  'msg': 'Low text color to background contrast.',
                  'msg_name': 'text-readability',
                  'page': 'Slide 4'},
                 {'help': 'Projectors are notorious for not having good contrast. Your text to too close to the background color and might be unreadable.',
                  'id': 'C3000',
                  'msg': 'Low text color to background contrast.',
                  'msg_name': 'text-readability',
                  'page': 'Slide 5'},
                 {'help': 'Projectors are notorious for not having good contrast. Your text to too close to the background color and might be unreadable.',
                  'id': 'C3000',
                  'msg': 'Low text color to background contrast.',
                  'msg_name': 'text-readability',
                  'page': 'Slide 7'},
                 {'help': 'Projectors are notorious for not having good contrast. Your text to too close to the background color and might be unreadable.',
                  'id': 'C3000',
                  'msg': 'Low text color to background contrast.',
                  'msg_name': 'text-readability',
                  'page': 'Slide 8'},
                 {'help': 'Projectors are notorious for not having good contrast. Your text to too close to the background color and might be unreadable.',
                  'id': 'C3000',
                  'msg': 'Low text color to background contrast.',
                  'msg_name': 'text-readability',
                  'page': 'Slide 10'}])

    def test_checker_helpers(self):
        compare(
            readability.main(msg_info='All'),
            [{'help': 'Projectors are notorious for not having good contrast.',
              'id': 'C3000',
              'msg': 'Projectors are notorious for not having good contrast.',
              'msg_name': 'text-readability',
              'page': ''}])
        compare(
            readability.main(msg_info=['C3000']),
            [{'help': 'Projectors are notorious for not having good contrast.',
              'id': 'C3000',
              'msg': 'Projectors are notorious for not having good contrast.',
              'msg_name': 'text-readability',
              'page': ''}])
        compare(readability.main(msg_info=['W8001']),
                [])

if __name__ == '__main__':
    unittest.main()
