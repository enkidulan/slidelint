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
                      msg='Too close to edges: Text should not appear close to the edges.',
                      help="Too close to edges: Text should not appear close to the edges.",
                      page='')])
        compare(edges_danger_zone.main(msg_info=['C1003']),
                [dict(id='C1003',
                      msg_name='too-close-to-edges',
                      msg='Too close to edges: Text should not appear close to the edges.',
                      help="Too close to edges: Text should not appear close to the edges.",
                      page='')])
        compare(edges_danger_zone.main(msg_info=['W8001']),
                [])

    def test_text_is_to_close_to_edges(self):
      for prefix in ('GD', 'LO'):
        target_file = os.path.join(here, 'files', 'pdfs', prefix+'_edges_danger_zone.pdf')
        rez = edges_danger_zone.main(target_file=target_file)
        compare(rez,
                [dict(id='C1003', msg_name='too-close-to-edges',
                      msg='Too close to edges: Text should not appear close to the edges.',
                      help="Too close to edges: Text should not appear close to the edges.",
                      page='1'),
                dict(id='C1003', msg_name='too-close-to-edges',
                      msg='Too close to edges: Text should not appear close to the edges.',
                      help="Too close to edges: Text should not appear close to the edges.",
                      page='2'),
                dict(id='C1003', msg_name='too-close-to-edges',
                      msg='Too close to edges: Text should not appear close to the edges.',
                      help="Too close to edges: Text should not appear close to the edges.",
                      page='3'),
                dict(id='C1003', msg_name='too-close-to-edges',
                      msg='Too close to edges: Text should not appear close to the edges.',
                      help="Too close to edges: Text should not appear close to the edges.",
                      page='4')])

    def test_text_if_not_near_edges(self):
      for prefix in ('GD', 'LO'):
        target_file = os.path.join(here, 'files', 'pdfs', prefix+'_simple_text_presentation.pdf')
        rez = edges_danger_zone.main(target_file=target_file)
        compare(rez, [])

if __name__ == '__main__':
    unittest.main()
