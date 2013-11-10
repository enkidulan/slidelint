"""
The *_font_gradient.pdf files have 16 slides which contain a different
sized text:
   * the firs slide contain 1/1 sized text - the text have same hide with
     its page
   * the firs slide contain 1/2 sized text - the text twice smaller than
     its page
   * ...
     but still too close for default allowed value
   * the firs slide contain 1/16 sized text - the sixteen lines can be placed
     on page one upon other

The tests are checks:
  1. that help messages are provided
  2. that with default size value(1/6) the checks of 7..16 slides are fails
  3. that with custom size value 1/7 the checks of 8..16 slides are fails
  4. that with custom size value 1/10 the checks of 11..16 slides are fails
  5. that with custom size value 1/16 the checks of all slides are passes

Also this check depends on font type and its features.
"""
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
                      msg='Font is to small: Text should take up a minimum '
                          'of 1/6th(by default) the page.',
                      help='Font is to small: Text should take up a minimum '
                           'of 1/6th(by default) the page.',
                      page='')])
        compare(fontsize.main(msg_info=['C1002']),
                [dict(id='C1002',
                      msg_name='font-to-small',
                      msg='Font is to small: Text should take up a minimum '
                          'of 1/6th(by default) the page.',
                      help='Font is to small: Text should take up a minimum '
                           'of 1/6th(by default) the page.',
                      page='')])
        compare(fontsize.main(msg_info=['W8001']),
                [])

    def test_default(self):
        for prefix in ('libreoffice', 'msoffice'):
            target_file = os.path.join(
                here, prefix+'_font_gradient.pdf')
            rez = fontsize.main(target_file=target_file)
            compare(rez,
                    [{'help': 'Font is to small: Text should take up a '
                              'minimum of 1/6th(by default) the page.',
                      'id': 'C1002',
                      'msg': 'Font is to small: Text should take up a minimum'
                             ' of 1/6.0th the page.',
                      'msg_name': 'font-to-small',
                      'page': 'Slide 7'},
                     {'help': 'Font is to small: Text should take up a '
                              'minimum of 1/6th(by default) the page.',
                      'id': 'C1002',
                      'msg': 'Font is to small: Text should take up a minimum'
                             ' of 1/6.0th the page.',
                      'msg_name': 'font-to-small',
                      'page': 'Slide 8'},
                     {'help': 'Font is to small: Text should take up a '
                              'minimum of 1/6th(by default) the page.',
                      'id': 'C1002',
                      'msg': 'Font is to small: Text should take up a minimum'
                             ' of 1/6.0th the page.',
                      'msg_name': 'font-to-small',
                      'page': 'Slide 9'},
                     {'help': 'Font is to small: Text should take up a '
                              'minimum of 1/6th(by default) the page.',
                      'id': 'C1002',
                      'msg': 'Font is to small: Text should take up a minimum'
                             ' of 1/6.0th the page.',
                      'msg_name': 'font-to-small',
                      'page': 'Slide 10'},
                     {'help': 'Font is to small: Text should take up a '
                              'minimum of 1/6th(by default) the page.',
                      'id': 'C1002',
                      'msg': 'Font is to small: Text should take up a minimum'
                             ' of 1/6.0th the page.',
                      'msg_name': 'font-to-small',
                      'page': 'Slide 11'},
                     {'help': 'Font is to small: Text should take up a '
                              'minimum of 1/6th(by default) the page.',
                      'id': 'C1002',
                      'msg': 'Font is to small: Text should take up a minimum'
                             ' of 1/6.0th the page.',
                      'msg_name': 'font-to-small',
                      'page': 'Slide 12'},
                     {'help': 'Font is to small: Text should take up a '
                              'minimum of 1/6th(by default) the page.',
                      'id': 'C1002',
                      'msg': 'Font is to small: Text should take up a minimum'
                             ' of 1/6.0th the page.',
                      'msg_name': 'font-to-small',
                      'page': 'Slide 13'},
                     {'help': 'Font is to small: Text should take up a '
                              'minimum of 1/6th(by default) the page.',
                      'id': 'C1002',
                      'msg': 'Font is to small: Text should take up a minimum'
                             ' of 1/6.0th the page.',
                      'msg_name': 'font-to-small',
                      'page': 'Slide 14'},
                     {'help': 'Font is to small: Text should take up a '
                              'minimum of 1/6th(by default) the page.',
                      'id': 'C1002',
                      'msg': 'Font is to small: Text should take up a minimum'
                             ' of 1/6.0th the page.',
                      'msg_name': 'font-to-small',
                      'page': 'Slide 15'},
                     {'help': 'Font is to small: Text should take up a '
                              'minimum of 1/6th(by default) the page.',
                      'id': 'C1002',
                      'msg': 'Font is to small: Text should take up a minimum'
                             ' of 1/6.0th the page.',
                      'msg_name': 'font-to-small',
                      'page': 'Slide 16'}])

    def test_1_of_7(self):
        for prefix in ('libreoffice', 'msoffice'):
            target_file = os.path.join(
                here, prefix+'_font_gradient.pdf')
            rez = fontsize.main(target_file=target_file, min_page_ratio=7)
            compare(rez,
                    [{'help': 'Font is to small: Text should take up a '
                              'minimum of 1/6th(by default) the page.',
                      'id': 'C1002',
                      'msg': 'Font is to small: Text should take up a minimum'
                             ' of 1/7.0th the page.',
                      'msg_name': 'font-to-small',
                      'page': 'Slide 8'},
                     {'help': 'Font is to small: Text should take up a '
                              'minimum of 1/6th(by default) the page.',
                      'id': 'C1002',
                      'msg': 'Font is to small: Text should take up a minimum'
                             ' of 1/7.0th the page.',
                      'msg_name': 'font-to-small',
                      'page': 'Slide 9'},
                     {'help': 'Font is to small: Text should take up a '
                              'minimum of 1/6th(by default) the page.',
                      'id': 'C1002',
                      'msg': 'Font is to small: Text should take up a minimum'
                             ' of 1/7.0th the page.',
                      'msg_name': 'font-to-small',
                      'page': 'Slide 10'},
                     {'help': 'Font is to small: Text should take up a '
                              'minimum of 1/6th(by default) the page.',
                      'id': 'C1002',
                      'msg': 'Font is to small: Text should take up a minimum'
                             ' of 1/7.0th the page.',
                      'msg_name': 'font-to-small',
                      'page': 'Slide 11'},
                     {'help': 'Font is to small: Text should take up a '
                              'minimum of 1/6th(by default) the page.',
                      'id': 'C1002',
                      'msg': 'Font is to small: Text should take up a minimum'
                             ' of 1/7.0th the page.',
                      'msg_name': 'font-to-small',
                      'page': 'Slide 12'},
                     {'help': 'Font is to small: Text should take up a '
                              'minimum of 1/6th(by default) the page.',
                      'id': 'C1002',
                      'msg': 'Font is to small: Text should take up a minimum'
                             ' of 1/7.0th the page.',
                      'msg_name': 'font-to-small',
                      'page': 'Slide 13'},
                     {'help': 'Font is to small: Text should take up a '
                              'minimum of 1/6th(by default) the page.',
                      'id': 'C1002',
                      'msg': 'Font is to small: Text should take up a minimum'
                             ' of 1/7.0th the page.',
                      'msg_name': 'font-to-small',
                      'page': 'Slide 14'},
                     {'help': 'Font is to small: Text should take up a '
                              'minimum of 1/6th(by default) the page.',
                      'id': 'C1002',
                      'msg': 'Font is to small: Text should take up a minimum'
                             ' of 1/7.0th the page.',
                      'msg_name': 'font-to-small',
                      'page': 'Slide 15'},
                     {'help': 'Font is to small: Text should take up a '
                              'minimum of 1/6th(by default) the page.',
                      'id': 'C1002',
                      'msg': 'Font is to small: Text should take up a minimum'
                             ' of 1/7.0th the page.',
                      'msg_name': 'font-to-small',
                      'page': 'Slide 16'}])

    def test_1_of_10(self):
        for prefix in ('libreoffice', 'msoffice'):
            target_file = os.path.join(
                here, prefix+'_font_gradient.pdf')
            rez = fontsize.main(target_file=target_file, min_page_ratio=10)
            compare(rez,
                    [{'help': 'Font is to small: Text should take up a '
                              'minimum of 1/6th(by default) the page.',
                      'id': 'C1002',
                      'msg': 'Font is to small: Text should take up a minimum'
                             ' of 1/10.0th the page.',
                      'msg_name': 'font-to-small',
                      'page': 'Slide 11'},
                     {'help': 'Font is to small: Text should take up a '
                              'minimum of 1/6th(by default) the page.',
                      'id': 'C1002',
                      'msg': 'Font is to small: Text should take up a minimum'
                             ' of 1/10.0th the page.',
                      'msg_name': 'font-to-small',
                      'page': 'Slide 12'},
                     {'help': 'Font is to small: Text should take up a '
                              'minimum of 1/6th(by default) the page.',
                      'id': 'C1002',
                      'msg': 'Font is to small: Text should take up a minimum'
                             ' of 1/10.0th the page.',
                      'msg_name': 'font-to-small',
                      'page': 'Slide 13'},
                     {'help': 'Font is to small: Text should take up a '
                              'minimum of 1/6th(by default) the page.',
                      'id': 'C1002',
                      'msg': 'Font is to small: Text should take up a minimum'
                             ' of 1/10.0th the page.',
                      'msg_name': 'font-to-small',
                      'page': 'Slide 14'},
                     {'help': 'Font is to small: Text should take up a '
                              'minimum of 1/6th(by default) the page.',
                      'id': 'C1002',
                      'msg': 'Font is to small: Text should take up a minimum'
                             ' of 1/10.0th the page.',
                      'msg_name': 'font-to-small',
                      'page': 'Slide 15'},
                     {'help': 'Font is to small: Text should take up a '
                              'minimum of 1/6th(by default) the page.',
                      'id': 'C1002',
                      'msg': 'Font is to small: Text should take up a minimum'
                             ' of 1/10.0th the page.',
                      'msg_name': 'font-to-small',
                      'page': 'Slide 16'}])

    def test_1_of_16(self):
        for prefix in ('libreoffice', 'msoffice'):
            target_file = os.path.join(
                here, prefix+'_font_gradient.pdf')
            rez = fontsize.main(target_file=target_file, min_page_ratio=16)
            compare(rez,
                    [])

if __name__ == '__main__':
    unittest.main()
