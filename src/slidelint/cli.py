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
from docopt import docopt
from slidelint.resources import PlugginsHandler
from slidelint.config_parser import LintConfig
from slidelint.outputs import OutputHandler

import logging
logger = logging.getLogger(__name__)


def lint(target_file, config_file, output, enable_disable_ids, msg_info):
    pluggins = PlugginsHandler()
    if msg_info:
        rezult = [p.check(msg_info=msg_info) for p in pluggins.load_checkers()]
        msg_ids = []
    else:
        config = LintConfig(config_file)
        config.compose(*enable_disable_ids)
        msg_ids = config.disable_messages  # mute messaging from appearing in report
        checkers = pluggins.load_checkers(
            categories=config.categories,
            checkers=config.checkers_isd,
            disabled_categories=config.disabled_categories,
            disabled_checkers=config.disabled_checkers
        )
        rezult = []
        for checker in checkers:
            kwargs = {'target_file': target_file}
            kwargs.update(config.get_checker_args(checker.name))
            rezult.append(checker.check(kwargs))
    return OutputHandler(rezult, msg_ids, output['format'], output['files_output'], output['ids'])


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
