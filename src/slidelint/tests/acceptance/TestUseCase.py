import os
import unittest
import testfixtures
import tempdir
from fabric import api

here = os.path.dirname(os.path.abspath(__file__))
bad_presentation = os.path.join(here, 'bad_presentation.pdf')
not_so_bad_presentation = os.path.join(here, 'not_so_bad_presentation.pdf')
good_presentation = os.path.join(here, 'good_presentation.pdf')
config1 = os.path.join(here, 'config1')
config2 = os.path.join(here, 'config2')
config3 = os.path.join(here, 'config3')

REBASE = False


def run(*arg, **kwargs):
    kwargs['capture'] = True
    try:
        return api.local(*arg, **kwargs)
    except SystemExit, message:
        raise ValueError(
            "[%s] run() received nonzero return code 1 while executing "
            "%s:\n%s" % (api.env.host_string, repr(arg), message.message))


class TestAcceptance(unittest.TestCase):

    def setUp(self):
        self.dir = os.getcwd()

    def test_pip_instalation(self):
        with tempdir.TempDir() as t:
            with api.lcd(t):
                run("virtualenv --no-site-packages .")
                run("bin/pip install https://github.com/enkidulan/"
                    "slidelint/archive/master.tar.gz")

    def test_info_option(self):
        with api.lcd(self.dir):
            rez = run("bin/slidelint -i %s" % bad_presentation)
            rez_file = bad_presentation[:-3] + 'infooption_default.txt'
            if REBASE:
                with open(rez_file, 'wb') as f:
                    f.write(rez)
            else:
                testfixtures.compare(
                    rez,
                    open(rez_file, 'rb').read())

    def test_output_format(self):
        with api.lcd(self.dir):
            rez = run("bin/slidelint -f parseable %s" % bad_presentation)
            rez_file = bad_presentation[:-3] + 'parsableformat_default.txt'
            if REBASE:
                with open(rez_file, 'wb') as f:
                    f.write(rez)
            else:
                testfixtures.compare(
                    rez,
                    open(rez_file, 'rb').read())

    def test_enablind_disabling(self):
        with api.lcd(self.dir):
            rez = run("bin/slidelint -i -f colorized -d C1002,ContentQuality"
                      ",edges_danger_zone -e "
                      "language_tool_checker %s" % bad_presentation)
            rez_file =\
                bad_presentation[:-3] + 'cmdlineenablingdisabling_default.txt'
            if REBASE:
                with open(rez_file, 'wb') as f:
                    f.write(rez)
            else:
                testfixtures.compare(
                    rez,
                    open(rez_file, 'rb').read())

    def test_file_output_file(self):
        with api.lcd(self.dir):
            rez = run("bin/slidelint -f html --files-output  "
                      "%s" % bad_presentation)
            testfixtures.compare(
                rez,
                "No config file found, using default configuration")
            rez = run("cat bad_presentation.lintrez")
            rez_file = bad_presentation[:-3] + 'fileoutput_default.txt'
            if REBASE:
                with open(rez_file, 'wb') as f:
                    f.write(rez)
            else:
                testfixtures.compare(
                    rez,
                    open(rez_file, 'rb').read())

    def test_custom_config_file(self):
        with api.lcd(self.dir):
            presentations = (
                good_presentation,
                not_so_bad_presentation,
                bad_presentation)
            configs = (config1, config2, config3)
            for presentation in presentations:
                for config in configs:
                    config_suf = config.rsplit(os.path.sep, 1)[1] + '.txt'
                    rez_file = presentation[:-3] + config_suf
                    rez = run("bin/slidelint --config=%s "
                              "%s" % (config, presentation))
                    if REBASE:
                        with open(rez_file, 'wb') as f:
                            f.write(rez)
                    else:
                        testfixtures.compare(
                            rez,
                            open(rez_file, 'rb').read())

if __name__ == '__main__':
    import sys
    if 'rebaseline' in sys.argv:
        del sys.argv[sys.argv.index('rebaseline')]
        REBASE = True
    unittest.main()
