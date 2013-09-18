"""
Example of program with many options using docopt.

Usage:
  slidelint help-msg [<msg_id>...]
  slidelint [options] FILE

Arguments:
  FILE  Path to PDF presentation file
  msg_id  id of slidelint message

Options:
  -h --help              show this help message and exit
  --version              show version and exit
  -i --include-ids       include ids in report [default: False]
  --config=<configfile>  path to configuration file
  -f <format> --output-format=<format>  Set the output format
                                        (e.g. text,parseable,colorized,msvs,html)
                                        [default: text]
  --files-output
  -e <msg_ids> --enable=<msg_ids>  Enable the message, report, category or checker with the given id(s). You can either give multiple
                                         identifier separated by comma (,) or put this option multiple time.
  -d <msg_ids> --disable=<msg_ids>  Enable the message, report, category or checker with the given id(s). You can either give multiple
                                          identifier separated by comma (,) or put this option multiple time.
"""

from docopt import docopt
import configparser
import os.path
import pkg_resources
import re

import logging
logger = logging.getLogger(__name__)


def read_config(path):
    """ configparser reader """
    parser = configparser.ConfigParser()
    default_config = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  'default.cfg')
    if not path:
        logger.info("No config file found, using default configuration")
    parser.read(path or default_config)
    return parser


def id_clasify(data):
    """
    >>> id_clasify("cheko,cat.one,chekt,w123,cat.two,w234,chekn")
    (['w123', 'w234'], ['cheko', 'chekt', 'chekn'], ['cat.one', 'cat.two'])
    >>> id_clasify("chekn")
    ([], ['chekn'], [])
    >>> id_clasify("c456")
    (['c456'], [], [])
    >>> id_clasify("chekn.fds")
    ([], [], ['chekn.fds'])
    """
    if not data:
        return [], [], []
    messages = re.findall(r"\w\d{3}", data)
    checkers = [i for i in data.split(',') if re.match(r"^([a-zA-Z]+)$", i)]
    categories = re.findall(r"\w+\.\w+", data)
    return messages, checkers, categories


def load_checker(group, name):
    return [entrypoint.load() for entrypoint in
            pkg_resources.iter_entry_points(group, name)][0]


def belongs2category(category, checkers):
    return [checker for checker in checkers
            if [i for i in pkg_resources.iter_entry_points(category, checker)]]


def load_category_from_config_file(config, category, eckrs, dckrs):
    pipes = []
    checkers = filter(None, config[category]['checkers'].split('\n'))
    # finding checkers available for category
    enable = belongs2category(config[category]['name'], eckrs)
    checkers = [i for i in checkers + enable if i not in dckrs]
    for checker in checkers:
        if checker in config:
            # checker is in config file so load params and pipe by entry_point
            kwargs = dict(config[checker])
            entry_point = kwargs.pop('entry_point')
            pipe = load_checker(config[category]['name'], entry_point)
            pipes.append((pipe, kwargs))
        else:
            # there is no configuration for checker so just load him by name
            pipe = load_checker(config[category]['name'], checker)
            pipes.append((pipe, {}))
    return pipes


def load_pipes(config, categories, eckrs, dckrs):
    pipes = []
    for category in categories:
        if category in config:
            pipes += load_category_from_config_file(config, category, eckrs, dckrs)
        else:
            pipes += [entrypoint.load() for entrypoint in pkg_resources.iter_entry_points(category)]
    return pipes


def make_pipeline(config, (eckrs, ectrs), (dckrs, dctrs)):
    # getting list of categories for looking in
    categories = filter(None, config['pipeline']['categories'].split('\n'))
    categories = [i for i in categories + ectrs if i not in dctrs]
    pipes = load_pipes(config, categories, eckrs, dckrs)
    return pipes


def main():
    """ config reader and pipeline runner
{'--config': None,
 '--disable': None,
 '--enable': None,
 '--files-output': False,
 '--help': False,
 '--include-ids': False,
 '--output-format': 'text',
 '--version': False,
 '<msg_id>': [],
 'FILE': 'sample.pdf',
 'help-msg': False}

    """
    args = docopt(__doc__)
    config = read_config(args['--config'])
    args['--enable'], eckrs, ectrs = id_clasify(args['--enable'])
    args['--disable'], dckrs, dctrs = id_clasify(args['--disable'])
    pipeline = make_pipeline(config, (eckrs, ectrs), (dckrs, dctrs))
    # import pdb; pdb.set_trace()
    print [i[0](5) for i in pipeline]



