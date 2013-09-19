
*********
User case
*********


Getting message id description
-------------------------------

**Command pattern**:

  slidelint help-msg [<msg_id>...]

**Arguments**:
  msg_id  id of slidelint message

**Examples**:

    $ slidelint help-msg  -  return all messaged description
    $ slidelint help-msg W0101  -  return description of W0101
    $ slidelint help-msg W0101 C0404 W0505  -  return description of W0101 C0404 W0505


Run file checking
-----------------

**Command pattern**:

  slidelint [options] FILE

**Arguments**:
  FILE  Path to PDF presentation file

**Options**:
  -h --help              show this help message and exit
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

Reads configuration from default config and check presentation.pdf:

::

    $ slidelint presentation.pdf -

Reads configuration from default config, check presentation.pdf and write
result to file in html format:

::

    $ slidelint --files-output  -f html presentation.pdf -


Reads configuration from default config; enabling all checks from new_package.new_category
category; disabling all checks from slidelint.content_quality, disabling edges check
and message with id C5001 from appearing; check presentation.pdf

::

    $ slidelint -e new_package.new_category -d slidelint.content_quality,edges,C5001  presentation.pdf -

Reads configuration from my_config.cfg file, include ids in report and  presentation.pdf

::

    $ slidelint --config=my_config.cfg -i presentation.pdf


***********
Name spaces
***********

    * Category : \\w+\\.\\w+ - module.category, module.othercategory
    * Checker : \\w+ - checker, grammarchecker, contrast
    * Message : \\w\\d{4} - C0111, W0402

****************
Pluggable system
****************

Pluggable system are implemented trough pkg_resources. To add a new checkers
you need to create a package and register checkers as setuptools
entry_points. Each checker should be defined as a pats of some entry_points group
- by this way slidelint implement checkers categorization. All checkers are
reachable from slidelint by a group name.

Defining new checkers and categories
====================================

To make new checker reachable for slidelint simply add it to package
entry_points as part of some group.

::

    entry_points="""
        [slidelint.content_quality]
        grammar = slidelint.pipes.grammar:main
        my_new_checker = slidelint.pipes.my_new_checker:main
        """

In this code example inside group my_new_checker was added to slidelint.content_quality
group(category). You can define your own groups or use already existing groups.


Configuration file
==================

To define a set of checks that should be applied to the document use config file.
The config file architecture:
    * The main section is pipeline. In this section are defined checks that will be applied to file
    * Categories sections. In category section are defined list of category checker that should be applied
    * Checkers sections. Use it to configure checking rule for checker
Also there is no need to define each precise checker or category to apply it -
just write its entry points name.

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

In this example pipeline consists from two categories.
The first category is defined as section in config file. It has a name - the
setuptools entry_points group, and a list of its checkers to apply.
Second category is not defined as config file section - instead in pipeline
categories list is written its name. In this case all checkers from this category will
be applied. The same goes to checkers definition - checker1 is defined as section,
it has its entry_point id and custom argument that will passed to it when it will
be called. The checker2 will be called with its default args.


Pipeline configuration thought command line
-------------------------------------------

Lets spouse that we have default configuration file that look like this:

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

But slidelint was called with next arguments:

::

    $ slidelint -e checker3,slidelint.category3 -d slidelint.category2,checker2,checker1 example.pdf

So actual pipeline representation will look like this:

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
case if its category was enabled also, otherwise checker will be ignored.
Removing goes after extending.


Writing a checker
=================

Checker is a function that will be called at list with one argument during the
checking process. This required argument is option passed by user to slidelint,
basically it's dictionary that look like this:

::

    {'--config': None,
     '--disable': [],
     '--enable': [],
     '--files-output': False,
     '--help': False,
     '--include-ids': False,
     '--output-format': 'text',
     '--version': False,
     'msg_id': [],
     'FILE': '',
     'help-msg': False}

Checker also should handle messages help and messages enabling/disabling.
Inside '--disable' and '--enable' at this step will be only messages ids.

::

    MESSAGES = {"W0101":("Desction", "Help")}
    MUTE_LIST = []

    def my_checker(options, custom_arg="")
        if options['help-msg']:
            help_msg = [MESSAGES[k][0] for k in options['msg_id'] if k in MESSAGES]
            return [i[0] for i in MESSAGES.values()] if not options['msg_id'] else help_msg
        results = [{'id':'W0101', 'slide':2, 'description':'....'}] # do some checks
        mute = [i for i in MUTE_LIST + options['--disable'] if i not in options['--enable']]
        return [message for message in results if message['id'] not in mute]
