"""
The *_edges_danger_zone.pdf files have 6 slides, all of them contain a text
which is attached to some of page edge and have some rotation:
   * at 1 and 3 slides text are really close to the edges
   * at 2 and 4 slides text are not so close to edges as at 1 and 3
     but still too close for default allowed value
   * at 5 and 6 slides text are perfectly far away from the page edges

The tests are checks:
  1. that help messages are provided
  2. that with default edges danger zone value the checks of
     1,2,3 and 4 slides are fails
  3. that with custom edges danger zone value which allows text to be more
     close to the edges the checks fails only for 1 and 3 slides
"""
import os.path
import unittest
from testfixtures import compare

from slidelint.checkers import edges_danger_zone

here = os.path.dirname(os.path.abspath(__file__))


class TestEdgesDangerZoneChecker(unittest.TestCase):

    def test_checker_helpers(self):
        compare(edges_danger_zone.main(msg_info='All'),
                [dict(id='C1003',
                      msg_name='too-close-to-edges',
                      msg='Too close to edges: Text should not appear '
                          'closer than 1/12th(by default) of the'
                          ' page size to the edges.',
                      help='Too close to edges: Text should not appear '
                           'closer than 1/12th(by default) of the'
                           ' page size to the edges.',
                      page='')])
        compare(edges_danger_zone.main(msg_info=['C1003']),
                [dict(id='C1003',
                      msg_name='too-close-to-edges',
                      msg='Too close to edges: Text should not appear '
                          'closer than 1/12th(by default) of the'
                          ' page size to the edges.',
                      help='Too close to edges: Text should not appear '
                           'closer than 1/12th(by default) of the'
                           ' page size to the edges.',
                      page='')])
        compare(edges_danger_zone.main(msg_info=['W8001']),
                [])

    def test_default(self):
        for prefix in ('libreoffice', 'msoffice'):
            target_file = os.path.join(
                here, prefix+'_edges_danger_zone.pdf')
            rez = edges_danger_zone.main(target_file=target_file)
            compare(rez,
                    [dict(id='C1003', msg_name='too-close-to-edges',
                          msg='Too close to edges: Text should not appear '
                              'closer than 1/12.0th of the page size '
                              'to the edges.',
                          help='Too close to edges: Text should not appear '
                               'closer than 1/12th(by default) of the'
                               ' page size to the edges.',
                          page='Slide 1'),
                     dict(id='C1003', msg_name='too-close-to-edges',
                          msg='Too close to edges: Text should not appear '
                              'closer than 1/12.0th of the page size '
                              'to the edges.',
                          help='Too close to edges: Text should not appear '
                               'closer than 1/12th(by default) of the'
                               ' page size to the edges.',
                          page='Slide 2'),
                     dict(id='C1003', msg_name='too-close-to-edges',
                          msg='Too close to edges: Text should not appear '
                              'closer than 1/12.0th of the page size '
                              'to the edges.',
                          help='Too close to edges: Text should not appear '
                               'closer than 1/12th(by default) of the'
                               ' page size to the edges.',
                          page='Slide 3'),
                     dict(id='C1003', msg_name='too-close-to-edges',
                          msg='Too close to edges: Text should not appear '
                              'closer than 1/12.0th of the page size '
                              'to the edges.',
                          help='Too close to edges: Text should not appear '
                               'closer than 1/12th(by default) of the'
                               ' page size to the edges.',
                          page='Slide 4')])

    def test_custom_args(self):
        for prefix in ('libreoffice', 'msoffice'):
            target_file = os.path.join(
                here, prefix+'_edges_danger_zone.pdf')
            rez = edges_danger_zone.main(
                target_file=target_file,
                min_page_ratio='23')
            compare(rez,
                    [dict(id='C1003', msg_name='too-close-to-edges',
                          msg='Too close to edges: Text should not appear '
                              'closer than 1/23.0th of the page size '
                              'to the edges.',
                          help='Too close to edges: Text should not appear '
                               'closer than 1/12th(by default) of the'
                               ' page size to the edges.',
                          page='Slide 1'),
                     dict(id='C1003', msg_name='too-close-to-edges',
                          msg='Too close to edges: Text should not appear '
                              'closer than 1/23.0th of the page size '
                              'to the edges.',
                          help='Too close to edges: Text should not appear '
                               'closer than 1/12th(by default) of the'
                               ' page size to the edges.',
                          page='Slide 3')])

if __name__ == '__main__':
    unittest.main()
