import subprocess
import os.path
import unittest
from testfixtures import OutputCapture, compare, ShouldRaise

from slidelint.cli import lint
from slidelint.utils import MultiprocessingManager
from slidelint.utils import SubprocessTimeoutHelper, TimeoutError
from slidelint.tests.modules.linter.test_modules import exeption_raising_func

here = os.path.dirname(os.path.abspath(__file__))


class TestTimeoutHelper(unittest.TestCase):
    def test_enternal_exp(self):
        foo = SubprocessTimeoutHelper(['python', '-c', '2/0'], timeout=1)
        msg = "Subprocess died with exit code 1(Operation not permitted)!\n"\
              "python -c 2/0\n"\
              "Traceback (most recent call last):\n"\
              "  File \"<string>\", line 1, in <module>\n"\
              "ZeroDivisionError: integer division or modulo by zero\n"
        with ShouldRaise(IOError(msg)):
            foo()

    def test_timeout_exp(self):
        cmd = ['python', '-c', 'import time; time.sleep(2); 2/0']
        foo = SubprocessTimeoutHelper(cmd, timeout=1)
        msg = "['python', '-c', 'import time; time.sleep(2); 2/0'] process "\
              "was terminated after 1 seconds"
        with ShouldRaise(TimeoutError(msg)):
            foo()

    def test_output(self):
        cmd = ['python', '-c', 'print 2']
        foo = SubprocessTimeoutHelper(cmd, timeout=1)
        compare("".join(foo()), '2\n')

    def test_subprocess_handler_exp(self):
        class Foo(SubprocessTimeoutHelper):
            def subprocess_handler(self):
                5/0
        foo = Foo("")
        msg = 'integer division or modulo by zero'
        with ShouldRaise(ZeroDivisionError(msg)):
            foo()


class TestMultiprocessingManager(unittest.TestCase):
    def test_bad_args(self):
        mltprsm = MultiprocessingManager()
        mltprsm.append(exeption_raising_func, {'x': 0})
        exp = IOError(
            "The function 'exeption_raising_func' of "
            "'slidelint.tests.modules.linter.test_modules' module raised an "
            "Exception:\nexeption_raising_func() got an unexpected keyword"
            " argument 'x'",)
        with ShouldRaise(exp):
            [i for i in mltprsm]

    def test_exeption(self):
        mltprsm = MultiprocessingManager()
        mltprsm.append(exeption_raising_func, {'arg': 0})
        exp = IOError(
            "The function 'exeption_raising_func' of "
            "'slidelint.tests.modules.linter.test_modules' module"
            " raised an Exception:\ninteger division or modulo by zero")
        with ShouldRaise(exp):
            [i for i in mltprsm]

    def test_rezult(self):
        mltprsm = MultiprocessingManager()
        mltprsm.append(exeption_raising_func, {'arg': 1.0})
        mltprsm.append(exeption_raising_func, {'arg': 2.0})
        mltprsm.append(exeption_raising_func, {'arg': 4.0})
        compare([1.0, 0.5, 0.25], [i for i in mltprsm])


class TestLinterRunner(unittest.TestCase):
    def setUp(self):
        self.kwargs = {
            'target_file': 'presentation.pdf',
            'config_file': os.path.join(here, 'test_models.cfg'),
            'output': {'format': 'raw', 'files_output': None, 'ids': True},
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
            "********************** Slide Deck presentation.pdf\n"
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
