import os.path
import unittest
from testfixtures import compare

from slidelint.checkers import fontsize

here = os.path.dirname(os.path.abspath(__file__))


class TestFontSizeChecker(unittest.TestCase):

    def test_checker_helpers(self):
        compare(fontsize.main(msg_info='All'),
                [dict(id='C1002',
                      msg_name='font-to-small',
                      msg='Font is to small: Text should take up a minimum of 1/6th the page.',
                      help="Font is to small: Text should take up a minimum of 1/6th the page.",
                      page='')])
        compare(fontsize.main(msg_info=['C1002']),
                [dict(id='C1002',
                      msg_name='font-to-small',
                      msg='Font is to small: Text should take up a minimum of 1/6th the page.',
                      help="Font is to small: Text should take up a minimum of 1/6th the page.",
                      page='')])
        compare(fontsize.main(msg_info=['W8001']),
                [])

    def test_file_with_small_text(self):
      for prefix in ('GD', 'LO'):
        target_file = os.path.join(here, 'files', 'pdfs', prefix+'_small_text.pdf')
        rez = fontsize.main(target_file=target_file)
        compare(rez,
                [dict(id='C1002', msg_name='font-to-small', msg='Font is to small: Text should take up a minimum of 1/6th the page.',
                      help="Font is to small: Text should take up a minimum of 1/6th the page.",
                      page='1')])

    def test_file_with_large_text(self):
      for prefix in ('GD', 'LO'):
        target_file = os.path.join(here, 'files', 'pdfs', prefix+'_simple_text_presentation.pdf')
        rez = fontsize.main(target_file=target_file)
        compare(rez, [])

if __name__ == '__main__':
    unittest.main()
