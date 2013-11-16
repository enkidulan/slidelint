
**************
Slidelint test
**************

Slidelint test are separated into three groups:

    * acceptance
    * checkers
    * modules


acceptance tests
================

This tests are designed to make sure slidelint is working as a whole.

It's contain example presentations files with its original sources:

    * bad_presentation.pdf - completely horrible presentation which contain
      all sorts of issues which slidelint was created to detect
    * good_presentation.pdf- almost perfect presentation
    * not_so_bad_presentation.pdf - presentation with couple of issues

Also its contain configurations files config1, config2 and config3. The first
one looks almost like default configuration file, but setting of some
checkers are a little bit changed. The config2 file contain no checkers
configurations, only categories are configured there - basically it's for
checking how checkers are runs when no configuration are provided for them.
The third one configuration file is for testing categories configuration.


The tests checks most common usage-cases of slidelint:

    * package installation with pip:

      ::

        bin/pip install https://github.com/enkidulan/slidelint/archive/master.tar.gz

    *  simple presentation linting:

      ::

        bin/slidelint -f parseable  presentation.pdf

    *  messages ids, checkers and groups eanabling and disabling throught comand line

      ::

        bin/slidelint -i -f colorized -d C1002,ContentQuality,edges_danger_zone -e language_tool_checker presentation.pdf

    *  outputing results to file:

      ::

        bin/slidelint -f html --files-output  presentation.pdf

    *  using custom configiration files

      ::

        bin/slidelint --config=configfile presentation.pdf

The expected presentations checks results are persisted into
presentation_name.check_type.txt files (for example "good_presentation.config1.txt").
And can be easily updated with "rebaseline" script(only for buildout installations).

checkers tests
==============

This tests are designed to make sure that an individual checkers are
correctly detecting what they should. Checkers tests are not affected by any
changes in default configuration or other parts of slidelint.
Each checker test-suite have its own set of PDFs files(with its original sources)
that is a custom designed to specifically cover checker problems. For more
information about specific checker test look at its test-case docstring.


modules test
============

This tests are designed to make sure that other parts of slidelint (such as
configuration file parser, output formatter, ...) are working correctly.

