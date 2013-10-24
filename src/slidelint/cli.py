"""
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
import os
from docopt import docopt
from slidelint.resources import PlugginsHandler
from slidelint.config_parser import LintConfig
from slidelint.outputs import output_handler
import time
from multiprocessing import Process

import logging
logger = logging.getLogger(__name__)


def lint(target_file, config_file, output, enable_disable_ids, msg_info, group="slidelint.pluggins"):
    pluggins = PlugginsHandler(group=group)
    config = LintConfig(config_file)
    config.compose(*enable_disable_ids)
    if msg_info:
        rezult = []
        for checker in pluggins.load_checkers():
            kwargs = {'msg_info': msg_info}
            kwargs.update(config.get_checker_args(checker.name))
            rezult += list(checker.check(**kwargs))
        msg_ids = []
    else:
        msg_ids = config.disable_messages  # mute messaging from appearing in report
        checkers = pluggins.load_checkers(
            categories=config.categories,
            checkers=config.checkers_isd,
            disabled_categories=config.disable_categories,
            disabled_checkers=config.disable_checkers
        )
        rezult = []
        # pp = []
        # for checker in checkers:
        #     kwargs = {'target_file': target_file}
        #     kwargs.update(config.get_checker_args(checker.name))
        #     pp.append(Process(target=checker.check, kwargs=kwargs))
        # for p in pp:
        #   p.start()
        # for p in pp:
        #   p.join()
        for checker in checkers:
            kwargs = {'target_file': target_file}
            # start = time.time()
            kwargs.update(config.get_checker_args(checker.name))
            rezult += checker.check(**kwargs)
            # end = time.time()
            # print "%s: %0.4f" % (checker.name, end - start)
    return output_handler(target_file, rezult, msg_ids, output['format'],
                          output['files_output'], output['ids'])


def cli():
    """
    User command line interface handler function
    """
    args = docopt(__doc__)
    target_file = args['FILE']
    config_file = args['--config']
    output = {'format': args['--output-format'],
              'files_output': args['--files-output'],
              'ids': args['--include-ids']
              }
    enable_disable_ids = (args['--enable'], args['--disable'])
    msg_info = "All" or args['<msg_id>'] if args['help-msg'] else False
    lint(target_file, config_file, output, enable_disable_ids, msg_info)
