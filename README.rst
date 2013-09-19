
For PDF files parsing there is pdfminer - it's satisfies almost all
requirements and it's open-source pure python library, kind of old but well
working. It's has problem with color detection so for contrast check I will
use some other tool or extend pdfminer.

The most obvious choice for grammar checks and gender pronouns is nltk
library, but it's kind of 'heavy', so maybe I will look for some smaller
libraries.

For implementing pluggable system there is ConfigParser. Docopt or CLI is
pretty good thing to create command line interface.


About testing:
 1. Simple doctest for each function.
 2. Acceptance robotframework tests with bunch of valid and invalid slides for testing.


**********
Name space
**********

Category : \\w+\\.\\w+

Checker : \\w+

Message : \\w\\d+

****************
Pluggable system
****************

All checkers are grouped into the categories. Each checker should be register
through entry_points of setuptools in setup.py file.

::

    entry_points="""
        [slidelint.content_quality]
        grammar = slidelint.pipes.grammar:main
        gender_pronouns = slidelint.pipes.gender_pronouns:main
        """

In code example inside group slidelint.content_quality(the category)
are registered gender_pronouns and grammar checkers. Each checker should
take at least one argument - config options, and return list of check results
or list of messages definitions.

For creating slides checking pipeline define config file:

::

    [pipeline]
    categories =
        category1
        slidelint.category2

    [category1]
    name = slidelint.category1
    checkers =
        checker1
        checker2

    [checker1]
    entry_point = checker1
    arg1 = 1
    arg2 = 2

In this example pipeline consists from two categories. For each category
is defined its name - the setuptools entry_points group, and list of its checkers
 to apply. If category or its checkers list are not defined then all checker
 from this category will be applied. Also checker definition allows to pass to it some
arguments otherwise checker will be applied with its defaults arguments.

Also you can configured pipeline through command line parameters:

::

    slidelint -e checker3,slidelint.category3 -d slidelint.category2,checker2,checker1 example.pdf

Here to configuration was added new checker - checker3 and new category -
slidelint.category3, category slidelint.category2 and checker1 and checker2 checkers was removed,
so current pipeline representation will look like this:

::

    [pipeline]
    categories =
        category1
        slidelint.category3

    [category1]
    name = slidelint.category1
    checkers =
        checker3

Be careful - in case of non unique checkers names results of command line
pipeline configuration can be unpredictable. Enabling checker allowed only in
case if its category was enabled also, otherwise it will be ignored.
For configuration removing operation will be applied after extending.

Enabling and disabling messages by id do pluggins themselves.
