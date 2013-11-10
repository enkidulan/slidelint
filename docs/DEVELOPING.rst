*****************
How to run tests?
*****************

Use nose(http://nose.readthedocs.org/) to run tests.

To run all test simply do:

::

    $ bin/nosetests slidelint

or if you want to execute some particular test just pass to nosetests
information about it location

::

    $ bin/nosetests src/slidelint/tests/checkers

in this example all tests for checkers will be executed

***************
Tests structure
***************

All test are located inside src/slidelint/tests/ directory and splinted into
following group:
    a. acceptance
    b. checkers
    c. modules

The **acceptance** directory contains tests which are designed to make
sure slidelint is working as a whole. Its contain good and bad real
presentations. And tests are simulate user command-line interaction,
which starts from slidelint installation through pip.


The **checkers** directory contains tests for checkers. Each checker have
their own directory for files and testcase. Fore more information about
particular checker test look at its test-suite doc-string
(and at test-cases also).

The **modules** directory provides test cases for make sure that all other
thing not related to checkers works correctly. Its contains tests for
output formatter, configuration file parser, ...

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
(at docs/checkers.rst you find how to do it) and register it as setup_tools
entry point as a part of slidelint.pluggins group (look at
docs/pluggable_system.rst for more instructions)

*************
Codding style
*************

Use pep8 and pylint with .pylintrc file which you can find add root
directory. Also repository contain pre-commit hook that will check code
quality with pylint.

**************
How to use git
**************

Information about how to fork github repository and send pull request
you can find here https://help.github.com/articles/fork-a-repo.
Also a lot of helpful information you can find here -
https://help.github.com/articles/syncing-a-fork

For detail information about how to use git look here http://githowto.com/
