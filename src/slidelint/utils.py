import os.path
import re
import configparser

import logging
logger = logging.getLogger(__name__)

HERE = os.path.dirname(os.path.abspath(__file__))

def read_config(path):
    """
    configparser reader

      >>> parser = read_config('not/existing/path')
      No config file found, using default configuration
      >>> parser['pipeline']['categories'].split()
      [u'text', u'content_quality']

      >>> with open('/tmp/test', 'w') as f:
      ...   f.write('[pipeline]\\ncategories = \\n    cat1')
      >>> parser = read_config('/tmp/test')
      >>> parser['pipeline']['categories'].split()
      [u'cat1']

    """
    parser = configparser.ConfigParser()
    path = os.path.isfile(path) and path
    default_config = os.path.join(HERE, 'default.cfg')
    if not path:
        logger.warn("No config file found, using default configuration")
    parser.read(path or default_config)
    return parser


def id_clasify(data):
    """Data is string with ids, separated by ',', it returns:

    (messages_ids, ckeckers_ids, categories_ids)

    >>> id_clasify("cheko,cat.one,chekt,w1234,cat.two,w2345,chekn")
    (['w1234', 'w2345'], ['cheko', 'chekt', 'chekn'], ['cat.one', 'cat.two'])
    >>> id_clasify("chekn")
    ([], ['chekn'], [])
    >>> id_clasify("c4567")
    (['c4567'], [], [])
    >>> id_clasify("chekn.fds")
    ([], [], ['chekn.fds'])
    """
    if not data:
        return [], [], []
    messages = re.findall(r"\w\d{4}", data)
    checkers = [i for i in data.split(',') if re.match(r"^([a-zA-Z]+)$", i)]
    categories = re.findall(r"\w+\.\w+", data)
    return messages, checkers, categories


def data_writer(data, format):
    with open('report.'+format, 'wb') as f:
        f.write(data)
