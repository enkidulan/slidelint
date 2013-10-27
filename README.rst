.. image:: https://travis-ci.org/enkidulan/slidelint.png?branch=master
    :target: https://travis-ci.org/enkidulan/slidelint


.. contents::


.. warning::
    This package is still in deep development.


************
Installation
************

**System requirements:**
    * setuptools > 1.0
    * java-7 (for LanguageTool)
    * python-dev (python-develop)
    * python-lxml
    * zlib1g-dev



::

   $ sudo apt-get install openjdk-7-jre zlib1g-dev python-lxml python-dev poppler-utils poppler-data


Use zc.buildout **to install this package**:

.. code::

    $ git clone https://github.com/enkidulan/slidelint.git
    $ cd slidelint
    $ python bootstrap.py
    $ bin/buildout


************
Instructions
************


Getting a message description
-----------------------------

**Command pattern**:

  slidelint help-msg [<msg_id>...]

**Arguments**:

  msg_id  id of slidelint message

**Examples**:

    $ slidelint help-msg  -  return descriptions of all messages

    $ slidelint help-msg W0101  -  return description of W0101 message id

    $ slidelint help-msg W0101 C0404 W0505  -  return descriptions of W0101 C0404 W0505 messages ids


Run a file check
----------------

**Command pattern**:

  slidelint [options] FILE

**Arguments**:

  FILE  Path to PDF presentation file

**Options**:

::

  -h --help              show help message
  -i --include-ids       include ids in report [default: False]
  --config=<configfile>  path to configuration file
  -f <format> --output-format=<format>  Set the output format
                                        (e.g. text,parseable,colorized,msvs,html)
                                        [default: text]
  --files-output
  -e <msg_ids> --enable=<msg_ids>  Enable the message, category or checker with the given id(s). You can either give multiple
                                         identifier separated by comma (,)
  -d <msg_ids> --disable=<msg_ids>  Disable the message, category or checker with the given id(s). You can either give multiple
                                          identifier separated by comma (,)


**Examples**:

Read a configuration from default config and check presentation.pdf:

::

    $ slidelint presentation.pdf

Read a configuration from default config, check presentation.pdf, and present
the result as an html files(separated file for each category):

::

    $ slidelint --files-output  -f html presentation.pdf


Read a configuration from default config file. Disable all checks from 'ContentQuality'
category and disable check with name edges_danger_zone and message with id
C1002. Enable 'language_tool_checker' checker (e.g. when you want to disable
all checkers from ContentQuality that is enabled in config file but left only
language_tool_checker from ContentQuality category).

::

    $ slidelint -d C1002,ContentQuality,edges_danger_zone -e language_tool_checker  presentation.pdf

Read a configuration from my_config.cfg file, and include ids in the report and  presentation.pdf

::

    $ slidelint --config=my_config.cfg -i presentation.pdf


