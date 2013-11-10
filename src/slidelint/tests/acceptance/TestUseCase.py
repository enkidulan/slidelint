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


class TestAcceptance(unittest.TestCase):

    def setUp(self):
        self.target_file = os.path.join(
            here, 'presentation3.pdf')
        self.dir = os.getcwd()

    def test_pip_instalation(self):
        with tempdir.TempDir() as t:
            with api.lcd(t):
                run("virtualenv --no-site-packages .")
                run("bin/pip install https://github.com/enkidulan/"
                    "slidelint/archive/master.tar.gz")

    def test_info_option(self):
        with api.lcd(self.dir):
            rez = run("bin/slidelint -i src/slidelint/tests/acceptance"
                      "/presentation3.pdf")
            testfixtures.compare(
                rez,
                'No config file found, using default configuration\n'
                '********************** Slide Deck src/slidelint/tests'
                '/acceptance/presentation3.pdf\n'
                'C1003:Slide 12: Too close to edges: Text should not appear closer than 1/12.0th of the page size to the edges. (too-close-to-edges)\n'
                'C3000:Slide 9: Low text color to background contrast. '
                '(text-readability)\n'
                'C3000:Slide 11: Low text color to background contrast. '
                '(text-readability)\n'
                'C1002:Slide 1: Font is to small: Text should take up a minimum of 1/6.0th the page. (font-to-small)\n'
                'C1002:Slide 2: Font is to small: Text should take up a minimum of 1/6.0th the page. (font-to-small)\n'
                'C1002:Slide 3: Font is to small: Text should take up a minimum of 1/6.0th the page. (font-to-small)\n'
                'C1002:Slide 4: Font is to small: Text should take up a minimum of 1/6.0th the page. (font-to-small)\n'
                'C1002:Slide 5: Font is to small: Text should take up a minimum of 1/6.0th the page. (font-to-small)\n'
                'C1002:Slide 6: Font is to small: Text should take up a minimum of 1/6.0th the page. (font-to-small)\n'
                'C1002:Slide 7: Font is to small: Text should take up a minimum of 1/6.0th the page. (font-to-small)\n'
                'C1002:Slide 8: Font is to small: Text should take up a minimum of 1/6.0th the page. (font-to-small)\n'
                'C1002:Slide 9: Font is to small: Text should take up a minimum of 1/6.0th the page. (font-to-small)\n'
                'C1002:Slide 10: Font is to small: Text should take up a minimum of 1/6.0th the page. (font-to-small)\n'
                'C1002:Slide 11: Font is to small: Text should take up a minimum of 1/6.0th the page. (font-to-small)\n'
                'C1002:Slide 12: Font is to small: Text should take up a minimum of 1/6.0th the page. (font-to-small)\n'
                'C2002:Slide 9: typographical - This sentence does not start '
                'with an uppercase letter (UPPERCASE_SENTENCE_START)\n'
                'C2002:Slide 9: typographical - This sentence does not start '
                'with an uppercase letter (UPPERCASE_SENTENCE_START)\n'
                'C2002:Slide 9: typographical - This sentence does not start '
                'with an uppercase letter (UPPERCASE_SENTENCE_START)\n'
                'C2005:Slide 9: misspelling - Possible spelling mistake found '
                '(MORFOLOGIK_RULE_EN_US)\n'
                'C2002:Slide 11: typographical - This sentence does not start '
                'with an uppercase letter (UPPERCASE_SENTENCE_START)\n'
                "C2000:Slide 11: misspelling - Use 'An' instead of 'A' if the "
                "following word starts with a vowel sound, e.g. 'an article', "
                "'an hour' (EN_A_VS_AN)\n"
                'C2005:Slide 11: misspelling - Possible spelling mistake '
                'found (MORFOLOGIK_RULE_EN_US)\n'
                'W4000:Slide 10: Gender Mention: " him" mentioned in "PICTURE'
                ' WITH \n'
                'CAPTION LAYOUT \n'
                'Caption him" (gender-mention)\n'
                'W4000:Slide 11: Gender Mention: "she" mentioned in "she" '
                '(gender-mention)'
            )

    def test_output_format(self):
        with api.lcd(self.dir):
            rez = run("bin/slidelint -f parseable src/slidelint/"
                      "tests/acceptance/presentation3.pdf")
            testfixtures.compare(
                rez,
                'No config file found, using default configuration\n'
                '********************** Slide Deck src/slidelint/tests/'
                'acceptance/presentation3.pdf\n'
                'src/slidelint/tests/acceptance/presentation3.pdf:Slide 12: '
                '[C1003(too-close-to-edges), ] Too close to edges: Text should not appear closer than 1/12.0th of the page size to the edges.\n'
                'src/slidelint/tests/acceptance/presentation3.pdf:Slide 9: '
                '[C3000(text-readability), ] Low text color to background '
                'contrast.\n'
                'src/slidelint/tests/acceptance/presentation3.pdf:Slide 11: '
                '[C3000(text-readability), ] Low text color to background '
                'contrast.\n'
                'src/slidelint/tests/acceptance/presentation3.pdf:Slide 1: '
                '[C1002(font-to-small), ] Font is to small: Text should take up a minimum of 1/6.0th the page.\n'
                'src/slidelint/tests/acceptance/presentation3.pdf:Slide 2: '
                '[C1002(font-to-small), ] Font is to small: Text should take up a minimum of 1/6.0th the page.\n'
                'src/slidelint/tests/acceptance/presentation3.pdf:Slide 3: '
                '[C1002(font-to-small), ] Font is to small: Text should take up a minimum of 1/6.0th the page.\n'
                'src/slidelint/tests/acceptance/presentation3.pdf:Slide 4: '
                '[C1002(font-to-small), ] Font is to small: Text should take up a minimum of 1/6.0th the page.\n'
                'src/slidelint/tests/acceptance/presentation3.pdf:Slide 5: '
                '[C1002(font-to-small), ] Font is to small: Text should take up a minimum of 1/6.0th the page.\n'
                'src/slidelint/tests/acceptance/presentation3.pdf:Slide 6: '
                '[C1002(font-to-small), ] Font is to small: Text should take up a minimum of 1/6.0th the page.\n'
                'src/slidelint/tests/acceptance/presentation3.pdf:Slide 7: '
                '[C1002(font-to-small), ] Font is to small: Text should take up a minimum of 1/6.0th the page.\n'
                'src/slidelint/tests/acceptance/presentation3.pdf:Slide 8: '
                '[C1002(font-to-small), ] Font is to small: Text should take up a minimum of 1/6.0th the page.\n'
                'src/slidelint/tests/acceptance/presentation3.pdf:Slide 9: '
                '[C1002(font-to-small), ] Font is to small: Text should take up a minimum of 1/6.0th the page.\n'
                'src/slidelint/tests/acceptance/presentation3.pdf:Slide 10: '
                '[C1002(font-to-small), ] Font is to small: Text should take up a minimum of 1/6.0th the page.\n'
                'src/slidelint/tests/acceptance/presentation3.pdf:Slide 11: '
                '[C1002(font-to-small), ] Font is to small: Text should take up a minimum of 1/6.0th the page.\n'
                'src/slidelint/tests/acceptance/presentation3.pdf:Slide 12: '
                '[C1002(font-to-small), ] Font is to small: Text should take up a minimum of 1/6.0th the page.\n'
                'src/slidelint/tests/acceptance/presentation3.pdf:Slide 9: '
                '[C2002(UPPERCASE_SENTENCE_START), ] typographical - This '
                'sentence does not start with an uppercase letter\n'
                'src/slidelint/tests/acceptance/presentation3.pdf:Slide 9: '
                '[C2002(UPPERCASE_SENTENCE_START), ] typographical - This '
                'sentence does not start with an uppercase letter\n'
                'src/slidelint/tests/acceptance/presentation3.pdf:Slide 9: '
                '[C2002(UPPERCASE_SENTENCE_START), ] typographical - This '
                'sentence does not start with an uppercase letter\n'
                'src/slidelint/tests/acceptance/presentation3.pdf:Slide 9: '
                '[C2005(MORFOLOGIK_RULE_EN_US), ] misspelling - Possible '
                'spelling mistake found\n'
                'src/slidelint/tests/acceptance/presentation3.pdf:Slide 11: '
                '[C2002(UPPERCASE_SENTENCE_START), ] typographical - This '
                'sentence does not start with an uppercase letter\n'
                "src/slidelint/tests/acceptance/presentation3.pdf:Slide 11: "
                "[C2000(EN_A_VS_AN), ] misspelling - Use 'An' instead of 'A'"
                " if the following word starts with a vowel sound, e.g. 'an "
                "article', 'an hour'\n"
                'src/slidelint/tests/acceptance/presentation3.pdf:Slide 11: '
                '[C2005(MORFOLOGIK_RULE_EN_US), ] misspelling - Possible '
                'spelling mistake found\n'
                'src/slidelint/tests/acceptance/presentation3.pdf:Slide 10: '
                '[W4000(gender-mention), ] Gender Mention: " him" mentioned '
                'in "PICTURE WITH \n'
                'CAPTION LAYOUT \n'
                'Caption him"\n'
                'src/slidelint/tests/acceptance/presentation3.pdf:Slide 11: '
                '[W4000(gender-mention), ] Gender Mention: "she" mentioned '
                'in "she"')

    def test_enablind_disabling(self):
        with api.lcd(self.dir):
            rez = run("bin/slidelint -i -f colorised -d C1002,ContentQuality"
                      ",edges_danger_zone -e language_tool_checker  src/"
                      "slidelint/tests/acceptance/presentation3.pdf")
            testfixtures.compare(
                rez,
                'No config file found, using default configuration\n'
                "No 'colorised' formatter found(use one of '['parseable', "
                "'text', 'colorized', 'html', 'msvs']'), using text "
                "formating\n"
                '********************** Slide Deck src/slidelint/tests/'
                'acceptance/presentation3.pdf\n'
                'C3000:Slide 9: Low text color to background contrast. '
                '(text-readability)\n'
                'C3000:Slide 11: Low text color to background contrast.'
                ' (text-readability)\n'
                'C2002:Slide 9: typographical - This sentence does not'
                ' start with an uppercase letter (UPPERCASE_SENTENCE_START)\n'
                'C2002:Slide 9: typographical - This sentence does not '
                'start with an uppercase letter (UPPERCASE_SENTENCE_START)\n'
                'C2002:Slide 9: typographical - This sentence does not '
                'start with an uppercase letter (UPPERCASE_SENTENCE_START)\n'
                'C2005:Slide 9: misspelling - Possible spelling mistake '
                'found (MORFOLOGIK_RULE_EN_US)\n'
                'C2002:Slide 11: typographical - This sentence does not '
                'start with an uppercase letter (UPPERCASE_SENTENCE_START)\n'
                "C2000:Slide 11: misspelling - Use 'An' instead of 'A' if "
                "the following word starts with a vowel sound, e.g. "
                "'an article', 'an hour' (EN_A_VS_AN)\n"
                'C2005:Slide 11: misspelling - Possible spelling mistake '
                'found (MORFOLOGIK_RULE_EN_US)')

    def test_file_output_file(self):
        with api.lcd(self.dir):
            rez = run("bin/slidelint -f html --files-output src/slidelint/"
                      "tests/acceptance/presentation.pdf")
            testfixtures.compare(
                rez,
                "No config file found, using default configuration")
            rez = run("cat presentation.lintrez")
            testfixtures.compare(
                rez,
                "<!DOCTYPE html>\n"
                "<html>\n"
                "<body>\n"
                "<h1>Slide Deck src/slidelint/tests/acceptance/"
                "presentation.pdf</h1>\n"
                "<p>C3000:Slide 3: Low text color to background contrast. (text-readability)</p>\n"
                "<p>C1002:Slide 1: Font is to small: Text should take up a minimum of 1/6.0th the page. (font-to-small)</p>\n"
                "<p>C1002:Slide 2: Font is to small: Text should take up a minimum of 1/6.0th the page. (font-to-small)</p>\n"
                "<p>C1002:Slide 3: Font is to small: Text should take up a minimum of 1/6.0th the page. (font-to-small)</p>\n"
                "<p>C1002:Slide 4: Font is to small: Text should take up a minimum of 1/6.0th the page. (font-to-small)</p>\n"
                "<p>C1002:Slide 5: Font is to small: Text should take up a minimum of 1/6.0th the page. (font-to-small)</p>\n"
                "<p>C2005:Slide 5: misspelling - Possible spelling mistake "
                "found (MORFOLOGIK_RULE_EN_US)</p>\n"
                "<p>C2005:Slide 5: misspelling - Possible spelling mistake"
                " found (MORFOLOGIK_RULE_EN_US)</p>\n"
                "</body>\n"
                "</html>")

    def test_custom_config_file(self):
        with api.lcd(self.dir):
            rez = run("bin/slidelint --config=src/slidelint/tests/acceptance/"
                      "my_config.cfg src/slidelint/tests/acceptance"
                      "/presentation3.pdf")
            testfixtures.compare(
                rez,
                "********************** Slide Deck src/slidelint/tests/"
                "acceptance/presentation3.pdf\n"
                "C:Slide 3: Too close to edges: Text should not appear closer than 1/10.0th of the page size to the edges. (too-close-to-edges)\n"
                "C:Slide 4: Too close to edges: Text should not appear closer than 1/10.0th of the page size to the edges. (too-close-to-edges)\n"
                "C:Slide 6: Too close to edges: Text should not appear closer than 1/10.0th of the page size to the edges. (too-close-to-edges)\n"
                "C:Slide 7: Too close to edges: Text should not appear closer than 1/10.0th of the page size to the edges. (too-close-to-edges)\n"
                "C:Slide 8: Too close to edges: Text should not appear closer than 1/10.0th of the page size to the edges. (too-close-to-edges)\n"
                "C:Slide 9: Too close to edges: Text should not appear closer than 1/10.0th of the page size to the edges. (too-close-to-edges)\n"
                "C:Slide 10: Too close to edges: Text should not appear closer than 1/10.0th of the page size to the edges. (too-close-to-edges)\n"
                "C:Slide 11: Too close to edges: Text should not appear closer than 1/10.0th of the page size to the edges. (too-close-to-edges)\n"
                "C:Slide 12: Too close to edges: Text should not appear closer than 1/10.0th of the page size to the edges. (too-close-to-edges)\n"
                "C:Slide 11: Low text color to background contrast."
                " (text-readability)\n"
                "C:Slide 6: Font is to small: Text should take up a minimum of 1/36.0th the page. (font-to-small)\n"
                "C:Slide 7: Font is to small: Text should take up a minimum of 1/36.0th the page. (font-to-small)\n"
                "C:Slide 8: Font is to small: Text should take up a minimum of 1/36.0th the page. (font-to-small)\n"
                "C:Slide 9: Font is to small: Text should take up a minimum of 1/36.0th the page. (font-to-small)\n"
                "C:Slide 11: Font is to small: Text should take up a minimum of 1/36.0th the page. (font-to-small)\n"
                "W:Slide 10: Gender Mention: \" him\" mentioned in "
                "\"PICTURE WITH \n"
                "CAPTION LAYOUT \n"
                "Caption him\" (gender-mention)\n"
                "W:Slide 11: Gender Mention: \"she\" mentioned in "
                "\"she\" (gender-mention)")

if __name__ == '__main__':
    unittest.main()
