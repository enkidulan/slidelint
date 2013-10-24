import os
import unittest
import testfixtures
import tempdir
from fabric import api

here = os.path.dirname(os.path.abspath(__file__))


def run(*arg, **kwargs):
    kwargs['capture'] = True
    try:
        return api.local(*arg, **kwargs)
    except SystemExit, message:
        raise ValueError(
             "[%s] run() received nonzero return code 1 while executing "
             "%s:\n%s" % (api.env.host_string, repr(arg), message.message))


class TestInstallation(unittest.TestCase):

    def setUp(self):
        self.target_file = os.path.join(here, 'files', 'pdfs', 'presentation.pdf')
        self.dir = tempdir.TempDir()

    def tearDown(self):
        self.dir.dissolve()

    def test_pip_install(self):
        with api.lcd(self.dir.name):
            run("virtualenv --no-site-packages .")
            run("bin/pip install https://github.com/enkidulan/slidelint/archive/master.tar.gz")
            rez = run("bin/slidelint %s" % self.target_file)

    def test_pip_easy_install(self):
        with api.lcd(self.dir.name):
            run("virtualenv --no-site-packages .")
            run("bin/easy_install https://github.com/enkidulan/slidelint/archive/master.tar.gz")
            rez = run("bin/slidelint %s" % self.target_file)


if __name__ == '__main__':
    unittest.main()
