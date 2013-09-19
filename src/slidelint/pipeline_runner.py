"""
slidelint version 1.0dev

PDF slides common problems checker.

Usage:
  slidelint help-msg [msg_id...]
  slidelint [options] FILE

Arguments:
  FILE  Path to PDF presentation file
  msg_id  id of slidelint message

Options:
  -h --help              show this help message and exit
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

from slidelint import  formatters
from slidelint.utils import read_config, id_clasify
from slidelint.resources import load_checker, belongs2category

import logging
logger = logging.getLogger(__name__)


def load_category_from_config_file(config, category, eckrs, dckrs):
    """ Loads categories items from pkg_resources.
    Takes :
      * config - config with defined pipeline, categories, etc...
      * category - category(entry_points of pkg_resources) which entries should be loaded
      * eckrs - list of additional checkers to load.
      * dckrs - list of checkers that should not be load from category (work
                only for checkers what was described in category)
    >>> import os.path
    >>> config = read_config(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests', 'test.cfg'))
    >>> import pkg_resources
    >>> class Loadable():
    ...    def __init__(self, name):
    ...        self.name = name
    ...    def load(self):
    ...        return self.name
    >>> def iter_entry_points(cat, chkr):
    ...    if cat == 'some.group':
    ...       return chkr in ('checker1', 'checker2', 'checker3') and  [Loadable(chkr)] or []
    >>> pkg_resources.iter_entry_points = iter_entry_points

    >>> load_category_from_config_file(config, 'cat1', (), ())
    [(u'checker1', {}), (u'checker2', {u'arg': u'some arg'})]

    >>> load_category_from_config_file(config, 'cat1', ('checker3',), ('checker_with_args',))
    [(u'checker1', {}), ('checker3', {})]

    >>> load_category_from_config_file(config, 'cat1', ('checker3',), ())
    [(u'checker1', {}), (u'checker2', {u'arg': u'some arg'}), ('checker3', {})]



    """
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
    """
    Handel categories loading, return loaded categories pipes.

    >>> import pkg_resources
    >>> load_category_from_config_file = lambda x: []
    >>> import os.path
    >>> config = read_config(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests', 'test.cfg'))
    >>> class Loadable():
    ...    def __init__(self, name):
    ...        self.name = name
    ...    def load(self):
    ...        return self.name
    >>> def iter_entry_points(cat):
    ...    if cat == 'new.category':
    ...       return map(Loadable, ('checker4', 'checker5'))
    ...    return []
    >>> pkg_resources.iter_entry_points = iter_entry_points
    >>> load_pipes(config, ('new.category',), (), ())
    [('checker4', {}), ('checker5', {})]
    >>> load_pipes(config, ('unregistred.category'), (), ())
    []
    """
    pipes = []
    for category in categories:
        if category in config:
            pipes += load_category_from_config_file(config, category, eckrs, dckrs)
        else:
            pipes += [(entrypoint.load(), {}) for entrypoint in pkg_resources.iter_entry_points(category)]
    return pipes


def make_pipeline(config, (eckrs, ectrs), (dckrs, dctrs)):
    """ getting list of categories for looking in """
    categories = filter(None, config['pipeline']['categories'].split('\n'))
    categories = [i for i in categories + ectrs if i not in dctrs]
    pipes = load_pipes(config, categories, eckrs, dckrs)
    return pipes


def run_pipeline(pipeline, config):
    """ run pipeline and collect its messages """
    messages = []
    for pipe, kwargs in pipeline:
        messages += pipe(config, kwargs)
    return messages


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
     'msg_id': [],
     'FILE': 'sample.pdf',
     'help-msg': False}
    """
    args = docopt(__doc__)
    config = read_config(args['--config'])
    args['--enable'], eckrs, ectrs = id_clasify(args['--enable'])
    args['--disable'], dckrs, dctrs = id_clasify(args['--disable'])
    pipeline = make_pipeline(config, (eckrs, ectrs), (dckrs, dctrs))
    messages = run_pipeline(pipeline, args)
    formatter = formatters.Formatter(config['--output-format'])
    output = formatter(messages)
    if config['--files-output']:
        return data_writer(output, formatter.format)
    print output
