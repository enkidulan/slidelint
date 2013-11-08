import os.path
import unittest
from testfixtures import compare

from slidelint.checkers import regex_grammar_checker

here = os.path.dirname(os.path.abspath(__file__))


class TestRegexGrammarChecker(unittest.TestCase):

    def test_regex_grammar_checker(self):
        target_file = os.path.join(here, 'files', 'pdfs', 'gender.pdf')
        kwargs = {
            'target_file': target_file,
            'source_file': 'gendered_pronouns',
            're_options': 'IGNORECASE',
            'msg_id': 'W2000',
            'msg_name': 'gender-mention',
            'msg': 'Gender Mention',
            'msg_help': 'Gendered pronouns are those that indicate gender: '
                        'he, she, him, her, hers, his, himself and herself. '
                        'All others, like "it, "one," and "they," are gender'
                        ' neutral.'}
        rez = regex_grammar_checker.main(**kwargs)
        compare(rez,
                [{u'help': u'Gendered pronouns are those that indicate gender:'
                           ' he, she, him, her, hers, his, himself and '
                           'herself. All others, like "it, "one," and "they,"'
                           ' are gender neutral.',
                  u'id': u'W2000',
                  u'msg': u'Gender Mention: " guys!" mentioned '
                          'in "Hello guys!"',
                  u'msg_name': u'gender-mention',
                  'page': 'Slide 1'},
                 {u'help': u'Gendered pronouns are those that indicate gender:'
                           ' he, she, him, her, hers, his, himself and '
                           'herself. All others, like "it, "one," and'
                           ' "they," are gender neutral.',
                  u'id': u'W2000',
                  u'msg': u'Gender Mention: "He " mentioned in "He wrote'
                          ' awesome code!"',
                  u'msg_name': u'gender-mention',
                  'page': 'Slide 3'}, ])

    def test_checker_helpers(self):
        kwargs = {
            'msg_info': 'All',
            'source_file': 'gendered_pronouns',
            're_options': 'IGNORECASE',
            'msg_id': 'W2000',
            'msg_name': 'gender-mention',
            'msg': 'Gender Mention',
            'msg_help': 'Gendered pronouns are those that indicate gender: he,'
                        ' she, him, her, hers, his, himself and herself. All '
                        'others, like "it, "one," and "they," are gender '
                        'neutral.'}
        help_msgs = regex_grammar_checker.main(**kwargs)
        compare(help_msgs,
                [{'help': 'Gendered pronouns are those that indicate gender:'
                          ' he, she, him, her, hers, his, himself and '
                          'herself. All others, like "it, "one," and '
                          '"they," are gender neutral.',
                  'id': 'W2000',
                  'msg': 'Gendered pronouns are those that indicate gender: '
                          'he, she, him, her, hers, his, himself and herself.'
                          ' All others, like "it, "one," and "they," '
                          'are gender neutral.',
                  'msg_name': 'gender-mention',
                  'page': ''}, ])
        kwargs['msg_info'] = ['W2000']
        help_msgs = regex_grammar_checker.main(**kwargs)
        compare(help_msgs,
                [{u'help': u'Gendered pronouns are those that indicate '
                           'gender: he, she, him, her, hers, his, himself'
                           ' and herself. All others, like "it, "one," and '
                           '"they," are gender neutral.',
                  u'id': u'W2000',
                  u'msg': u'Gendered pronouns are those that indicate '
                          'gender: he, she, him, her, hers, his, himself and'
                          ' herself. All others, like "it, "one," and '
                          '"they," are gender neutral.',
                  u'msg_name': u'gender-mention',
                  'page': ''}, ])
        kwargs['msg_info'] = ['W8001']
        compare(regex_grammar_checker.main(**kwargs),
                [])

if __name__ == '__main__':
    unittest.main()
