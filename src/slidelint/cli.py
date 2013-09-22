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
import configparser
import os.path
import pkg_resources
import logging
logger = logging.getLogger(__name__)

docoptself

def read_config(path):
    """ configparser reader """
    parser = configparser.ConfigParser()
    default_config = os.path.join(os.path.dirname(os.path.abspath(__file__)),                                  'default.cfg')
    if not path:
        logger.info("No config file found, using default configuration")
    parser.read(path or default_config)
    return parser

def load_pipes(group='slidelint.pipes'):
    return [entrypoint.load() for entrypoint in
            pkg_resources.iter_entry_points(group=group)]


def make_pipeline(config, to_enable, to_disable):
    pipes = load_pipes()
    print pipes

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
    pipeline = make_pipeline(config, args['--enable'], args['--disable'])
    print arg
