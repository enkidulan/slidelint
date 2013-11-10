Checkers messages isd name space
=================================

W1001 - contents
C1002 - fontsize
C1003 - danger zone
C2000-2300 - Language tool
C3000 - readability
W4000 - regexp


Text color to background contrast checker
=========================================

This checker compare grayscale character background colors histogram to character color.

::

    [readability]
    checker = readability
    scale_regress = 0.4
    max_similarity = 0.1
    cross_range = 70
    scale_waight = 2

Where:

    * cross_range - regress of values around text color on background histogram values for analyzing.
    * scale_regress - controls progressiveness of main color distance exponential coefficient of correlation function (it makes background histogram colors that distant from text color less important) Than this value bigger than less important are distant colors.
    * max_similarity - the max allowed value of color similarity between text and its background
    * scale_waight - control summary importance of similar colors.


Language tool checker
=====================

It's wrapper around languagetool, for more details look at http://www.languagetool.org

::

    [language_tool_checker]
    checker = language_tool_checker
    keep_alive = true

Language Tool server start pretty slow so you can keep its running at background
 with option "keep_alive = true"


Creating new regexp checker
============================

Write your regexp rules into file. Add new regex_grammar_checker checker to
configuration file in which put path to created file as a source_file argument,
and don't forget to define id, msg_name, msg and help options:

.. code-block::

    [gendered_pronouns]
    checker = regex_grammar_checker
    source_file = /path/to/file/with/regex
    re_options = (option for regexp compilation: IGNORECASE, DEBUG, ...)
    id = W2000
    msg_name = gender-mention
    msg = Gender Mention
    help = Gendered pronouns are those that indicate gender: he, she, him, her, hers, his, himself and herself. All others, like "it, "one," and "they," are gender neutral.

Also don't forget to add new checker to some category to make it available
for using.


Writing a checker
=================

Checker is a function that will be called at least with two arguments during the
checking process. This required argument is target_file(full path to pdf
file that should be checked) and msg_info(can be False - which means do checks;
 'All' - return me all help messages you have; or list of ids - return me only
 messages that are in this list if you have some).

 There are help_wrapper in slidelint.utils so you cat use it for help-messages
 handing or write your own:

::

    from slidelint.utils import help_wrapper

    messages = (
        dict(id='01000',
             msg_name='msg-name',
             msg='Message',
             help="Message help"),)

    def main(target_file=None, msg_info=None, custom_arg='default_value'):
        if msg_info:
            return help(messages, msg_info)
        return some_check(target_file, custom_arg)


