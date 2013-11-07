import os.path
import unittest
from testfixtures import OutputCapture, compare

from slidelint.cli import lint

here = os.path.dirname(os.path.abspath(__file__))


class TestLinterRunner(unittest.TestCase):
    def setUp(self):
        self.kwargs = {
            'target_file': '/path/to/presentation.pdf',
            'config_file': os.path.join(here, 'files',
                                        'configurations', 'test_models.cfg'),
            'output': {'format': 'raw', 'files_output': False, 'ids': True},
            'enable_disable_ids': (None, None),
            'msg_info': None,
            'group': "slidelint.tests"}

    def test_get_messages_info_all(self):
        self.kwargs['msg_info'] = 'All'
        results = lint(**self.kwargs)
        compare(
            results,
            [dict(id='W1010', msg_name='warning-W1010',
                  msg='warning message with id W1010',
                  page='', help='full help message'),
             dict(id='C1011', msg_name='critical-C1011',
                  msg='warning message with id C1011',
                  page='', help='full help message'),
             dict(id='W1020', msg_name='warning-W1020',
                  msg='warning message with id W1020',
                  page='', help='full help message'),
             dict(id='C1021', msg_name='critical-C1021',
                  msg='warning message with id C1021',
                  page='', help='full help message'),
             dict(id='W2010', msg_name='warning-W2010',
                  msg='warning message with id W2010',
                  page='', help='full help message'),
             dict(id='C2011', msg_name='critical-C2011',
                  msg='warning message with id C2011',
                  page='', help='full help message')])

    def test_get_messages_info_list_ids(self):
        self.kwargs['msg_info'] = ['W1010', 'W2010', 'C2011']
        results = lint(**self.kwargs)
        compare(
            results,
            [dict(id='W1010', msg_name='warning-W1010',
                  msg='warning message with id W1010', page='',
                  help='full help message'),
             dict(id='W2010', msg_name='warning-W2010',
                  msg='warning message with id W2010', page='',
                  help='full help message'),
             dict(id='C2011', msg_name='critical-C2011',
                  msg='warning message with id C2011', page='',
                  help='full help message')])

    def test_get_messages_info_text_output(self):
        self.kwargs['msg_info'] = 'All'
        self.kwargs['output']['format'] = 'text'
        with OutputCapture() as output:
            lint(**self.kwargs)
        output.compare(
            "********************** Slide Deck /path/to/presentation.pdf\n"
            "W1010:: warning message with id W1010 (warning-W1010)\n"
            "C1011:: warning message with id C1011 (critical-C1011)\n"
            "W1020:: warning message with id W1020 (warning-W1020)\n"
            "C1021:: warning message with id C1021 (critical-C1021)\n"
            "W2010:: warning message with id W2010 (warning-W2010)\n"
            "C2011:: warning message with id C2011 (critical-C2011)\n")

    def test_file_check(self):
        results = list(lint(**self.kwargs))
        compare(
            results,
            [dict(id='C2011', msg_name='critical-C2011',
                  msg='warning message with id C2011', page='1'),
             dict(id='C1011', msg_name='critical-C1011',
                  msg='warning message with id C1011 arg1 is '
                      '"10"; arg2 is "20"', page='2')])

if __name__ == '__main__':
    unittest.main()
