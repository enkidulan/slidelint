"""
The *_redability.pdf files contain slides with different text color
contrasting to the background:
  1. bad text contrast(non gray-scale) - should fail with default args
  2. good text contrast(gray on white, gray on black) - should pass with
     default args
  3. bad text contrast(gray on white) - should fail with default args
  4. bad text contrast(gray on black) - should fail with default args
  5. white crossed white too much - should fail with default args
  6. white almost crossed white and black almost crossed black - should
     pass with default args
  7. black crossed black too much - should fail with default args
  8. white text on light image - should fail with default args
  9. white text with background on light image - should pass with
     default args
  10. black text on dark image - should fail with default args
  11. black text with background on dark image - should pass with
      default args

The tests check:
  * whether help messages are provided
  * whether checks with default agrs work correctly
  * whether checker args can be changed

"""
import os.path
import unittest
from testfixtures import compare, ShouldRaise, tempdir

from slidelint.checkers import readability
from slidelint.tests.utils import subprocess_context_helper

here = os.path.dirname(os.path.abspath(__file__))


def subprocess_helper(temp_dir, cmd):
    with subprocess_context_helper(temp_dir, cmd) as config_file:
        readability.tranform2html(
            temp_dir.path,
            temp_dir.path, config_file)


class TestContentsChecker(unittest.TestCase):
    @tempdir()
    def test_pdftohtml_fails(self, temp_dir):
        # Program doesn't exist
        with ShouldRaise(OSError):
            subprocess_helper(
                temp_dir, ['not_existing_program', '/tmp'])
        # Program fails to work
        with ShouldRaise(IOError):
            subprocess_helper(
                temp_dir, ['python', '-c', '5/0'])
        # Program segfaults
        with ShouldRaise(IOError):
            subprocess_helper(
                temp_dir,
                ['python', '-c',
                 'import signal; import sys; sys.exit(signal.SIGSEGV)'])

    def test_custom_args(self):
        # for prefix in ('msoffice', ):
        # for prefix in ('libreoffice', ):
        for prefix in ('msoffice', 'libreoffice'):
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
                [{'help': 'Projectors are notorious for not having good '
                          'contrast. Your text to too close to the '
                          'background color and might be unreadable.',
                  'id': 'C3000',
                  'msg': 'Low text color to background contrast.',
                  'msg_name': 'text-readability',
                  'page': 'Slide 5'},
                 {'help': 'Projectors are notorious for not having good '
                          'contrast. Your text to too close to the '
                          'background color and might be unreadable.',
                  'id': 'C3000',
                  'msg': 'Low text color to background contrast.',
                  'msg_name': 'text-readability',
                  'page': 'Slide 7'},
                 {'help': 'Projectors are notorious for not having good '
                          'contrast. Your text to too close to the '
                          'background color and might be unreadable.',
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
                [{'help': 'Projectors are notorious for not having good '
                          'contrast. Your text to too close to the '
                          'background color and might be unreadable.',
                  'id': 'C3000',
                  'msg': 'Low text color to background contrast.',
                  'msg_name': 'text-readability',
                  'page': 'Slide 1'},
                 {'help': 'Projectors are notorious for not having good '
                          'contrast. Your text to too close to the '
                          'background color and might be unreadable.',
                  'id': 'C3000',
                  'msg': 'Low text color to background contrast.',
                  'msg_name': 'text-readability',
                  'page': 'Slide 3'},
                 {'help': 'Projectors are notorious for not having good '
                          'contrast. Your text to too close to the '
                          'background color and might be unreadable.',
                  'id': 'C3000',
                  'msg': 'Low text color to background contrast.',
                  'msg_name': 'text-readability',
                  'page': 'Slide 4'},
                 {'help': 'Projectors are notorious for not having good '
                          'contrast. Your text to too close to the '
                          'background color and might be unreadable.',
                  'id': 'C3000',
                  'msg': 'Low text color to background contrast.',
                  'msg_name': 'text-readability',
                  'page': 'Slide 5'},
                 {'help': 'Projectors are notorious for not having good '
                          'contrast. Your text to too close to the '
                          'background color and might be unreadable.',
                  'id': 'C3000',
                  'msg': 'Low text color to background contrast.',
                  'msg_name': 'text-readability',
                  'page': 'Slide 7'},
                 {'help': 'Projectors are notorious for not having good '
                          'contrast. Your text to too close to the '
                          'background color and might be unreadable.',
                  'id': 'C3000',
                  'msg': 'Low text color to background contrast.',
                  'msg_name': 'text-readability',
                  'page': 'Slide 8'},
                 {'help': 'Projectors are notorious for not having good '
                          'contrast. Your text to too close to the '
                          'background color and might be unreadable.',
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
