"""
Usage:
  slidelint help-msg [<msg_id>...]
  slidelint [options] FILE

Arguments:
  FILE  Path to PDF presentation file
  msg_id  id of slidelint message

Options:
  -h --help              show this help message and exit
  -i --include-ids       include ids in report [default: False]
  --config=<configfile>  path to configuration file
  -f <format> --output-format=<format>  Set the output format
                                        (e.g. text,parseable,colorized,
                                        msvs,html,json) [default: text]
  --files-output=<result_file>     save linting results to result_file file
  -e <msg_ids> --enable=<msg_ids>  Enable the message, report, category or
                                   checker with the given id(s). You can either
                                   give multiple identifier separated by comma
                                   (,) or put this option multiple time.
  -d <msg_ids> --disable=<msg_ids>  Disable the message, report, category or
                                    checker with the given id(s). You can
                                    either give multiple identifier separated
                                    by comma (,) or put this option
                                    multiple time.

"""
from docopt import docopt
from slidelint.resources import PlugginsHandler
from slidelint.config_parser import LintConfig
from slidelint.outputs import output_handler
from slidelint.utils import MultiprocessingManager

import logging
LOGGER = logging.getLogger(__name__)


def lint(target_file, config_file, output, enable_disable_ids,
         msg_info, group="slidelint.pluggins"):
    """ main function that bring all thing together: loads slidelint pluggins,
    parses config file, handles command-line options, runs checkers and
    formats output.

    It takes:

        * target_file - path to pdf file or None
        * config_file - path to config file or None
        * output - it's a dict object for controlling results output:
            format - format of the output report, it's None
                     or one of [text', 'parseable', 'colorized',
                     'msvs', 'html'],
            files_output - file path, empty string or None, if empty
                           string than report will be
                           written to file otherwise printed to stdout,
            ids - if True then messages ids will be added to report
        * enable_disable_ids - command-line options for enabling/disabling
                               messages/checkers/categories, takes
        * msg_info -  ['list of messages ids,], None, or 'All' """
    pluggins = PlugginsHandler(group=group)
    config = LintConfig(config_file)
    config.compose(pluggins.checkers, *enable_disable_ids)
    if msg_info:
        # displaying help messages
        rezult = []
        for checker in pluggins.load_checkers():
            kwargs = {'msg_info': msg_info}
            kwargs.update(config.get_checker_args(checker.name))
            rezult += list(checker.check(**kwargs))
        msg_ids = []
        output['ids'] = True
    else:
        # run checkers
        # mute messaging from appearing in report
        msg_ids = config.disable_messages
        checkers = pluggins.load_checkers(
            categories=config.categories,
            checkers=config.checkers_ids,
            disabled_categories=config.disable_categories,
            disabled_checkers=config.disable_checkers
        )
        # lets run all checkers separately in different processes
        rezult = MultiprocessingManager()
        for checker in checkers:
            kwargs = {'target_file': target_file}
            kwargs.update(config.get_checker_args(checker.name))
            rezult.append(checker.check, kwargs)
    return output_handler(target_file, rezult, msg_ids, output['format'],
                          output['files_output'], output['ids'])


def cli():
    """
    User command line interface handler - parses command-line options and
    run linting
    """
    args = docopt(__doc__)
    target_file = args['FILE']
    config_file = args['--config']
    output = {'format': args['--output-format'],
              'files_output': args['--files-output'],
              'ids': args['--include-ids']
              }
    enable_disable_ids = (args['--enable'], args['--disable'])
    msg_info = args['<msg_id>'] or "All" if args['help-msg'] else None
    lint(target_file, config_file, output, enable_disable_ids, msg_info)
