.. image:: https://travis-ci.org/enkidulan/slidelint.png?branch=master
    :target: https://travis-ci.org/enkidulan/slidelint


.. contents::


************
Installation
************

**System requirements:**

    * setuptools > 1.0
    * java-7 (for LanguageTool)
    * python-dev (python-develop)
    * libxml2-dev
    * libxslt-dev
    * zlib1g-dev


To install system requirements on Ubuntu run follow commands:

::

    $ sudo pip install setuptools --upgrade
    $ sudo apt-get install openjdk-7-jre zlib1g-dev libxml2-dev libxslt-dev python-lxml python-dev poppler-utils poppler-data



You can **install slide** with pip:

.. code::

    bin/pip install https://github.com/enkidulan/slidelint/archive/master.tar.gz

or zc.buildout (http://buildout.org):

.. code::

    $ git clone https://github.com/enkidulan/slidelint.git
    $ cd slidelint
    $ python bootstrap.py
    $ bin/buildout

There is no need to run "python bootstrap.py" each time,
but you need indeed to run "python bootstrap.py" in the following cases:

    * you building a new buildout
    * you want to switch to a different python
    * you want to switch to a different version of setuptools or zc.buildot


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
                                        (e.g. text,parseable,colorized,msvs,html,json)
                                        [default: text]
  --files-output=<result_file>     save linting results to result_file file
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

    $ slidelint --files-output=linting.txt  -f html presentation.pdf


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


For **more documentation** look at docs directory.
