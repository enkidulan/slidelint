*****************
How to run tests?
*****************

Use nose(http://nose.readthedocs.org/) to run tests.

To run all test simply do:

::

    $ bin/nosetests slidelint

or if you want to execute some particular test just pass to nosetests
information about its location

::

    $ bin/nosetests src/slidelint/tests/checkers

in this example all tests for checkers will be executed

***************
Tests structure
***************

All test are located inside src/slidelint/tests/ directory and split into
following group:
    * acceptance
    * checkers
    * modules

The **acceptance** directory contains tests which are designed to make
sure slidelint works as a whole. It contains good and bad presentations.
And tests simulate user command-line interaction starting from
 slidelint installation through pip.


The **checkers** directory contains tests for checkers. Each checker has
its own directory for files and testcases. Fore more information about
particular checker test look at its test-suite doc-string
(and at the test-cases).

The **modules** directory provides test cases to make sure that all other
things not related to checkers work correctly. It contains tests for
output formatter, configuration file parser, ...

For more details take a look at **/src/slidelint/tests/Readme.rst** file.

*****************************
How to write a new test case?
*****************************

Just follow instructions that you can find at
http://docs.python.org/2/library/unittest.html and put your file with
test case into one of subdirectories of src/slidelint/tests directory.


***************************
How to write a new checker?
***************************

To add a new checker to a slidelint you need to add a checking module
(at docs/checkers.rst you can find how to do it) and register it as setup_tools
entry point as a part of slidelint.pluggins group (look at
docs/pluggable_system.rst for more instructions)

*************
Coding style
*************

Use pep8 and pylint with .pylintrc file which you can find at root
directory. Also repository contains pre-commit hook that will check code
quality with pylint, to active it just do at the package root:

::

    $ cp pre-commit .git/hooks/

**************
How to use git
**************

Information about how to make fork github repository and send pull request
you can find here https://help.github.com/articles/fork-a-repo.
Also a lot of helpful information you can find here -
https://help.github.com/articles/syncing-a-fork

For more detailed information about how to use git look here http://githowto.com/
