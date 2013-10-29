"""
Output handler and formatters
"""
import os
import sys
from colorama import Fore

import logging
user_messages = logging.getLogger('user_messages')

class BaseReporter():
    only_full_id = False
    header = ["********************** Slide Deck {path}"]
    footer = [""]

    def __init__(self, show_id, mute_ids, path):
        self.show_id = self.only_full_id or show_id
        self.mute_ids = mute_ids
        self.path = path
        self.update_title(path)

    def update_title(self, path):
        self.header[0] = self.header[0].format(path=self.path)

    def preformatfix(self, msg):
        msg['msg_id'] = msg['id'][0] if not self.show_id else msg['id']
        msg['path'] = self.path
        return msg

    def apply_formating(self, messages):
        def encoding_normalazer(messages):
            for msg in messages:
                for k, v in msg.items():
                    msg[k] = v.encode('utf-8') if isinstance(v, basestring) else v
                yield msg
        return [self.formatter.format(**msg) for msg in encoding_normalazer(messages)]

    def __call__(self, report):
        filtred = [self.preformatfix(msg) for msg in report if msg['id'] not in self.mute_ids]
        fixed_isd = [self.preformatfix(msg) for msg in filtred]
        return "\n".join(self.header + self.apply_formating(fixed_isd) + self.footer) + "\n"


class TextReporter(BaseReporter):
    formatter = '{msg_id}:{page}: {msg} ({msg_name})'


class ParseableTextReporter(BaseReporter):
    only_full_id = True
    formatter = '{path}:{page}: [{msg_id}({msg_name}), ] {msg}'


class VSTextReporter(BaseReporter):
    only_full_id = True
    formatter = '{path}({page}): [{msg_id}({msg_name})] {msg}'


class ColorizedTextReporter(BaseReporter):
    formatter = '{msg_id}:{page}: {msg} ({msg_name})'
    COLOR_MAPPING = {
        'C': Fore.RED,
        'W': "",
    }

    def apply_formating(self, messages):
        return [self.COLOR_MAPPING.get(msg['id'][0], "") + self.formatter.format(**msg) + Fore.RESET
                for msg in messages]


class HTMLTextReporter(BaseReporter):
    # TODO: add fancy JS formatter like in robotframework
    formatter = '{msg_id}:{page}: {msg} ({msg_name})'
    only_full_id = True
    header = [
        "<!DOCTYPE html>",
        "<html>",
        "<body>",
        "<h1>Slide Deck %s</h1>"]
    footer = [
        "</body>",
        "</html>"]

    def update_title(self, path):
        self.header[-1] = self.header[-1] % self.path

    def apply_formating(self, messages):
        return ['<p>' + self.formatter.format(**msg) +'</p>' for msg in messages]


REPORTERS_MAPING = {
    'text': TextReporter,
    'parseable': ParseableTextReporter,
    'colorized': ColorizedTextReporter,
    'msvs': VSTextReporter,
    'html': HTMLTextReporter}


def output_handler(path, rezults, mute_ids=[], format='text', report_file=False, show_id=False):
    """
    Formating check results and handling its output.
    Takes:
        * path - path to checking file: 'path/to/file.pdf'
        * rezults - results of checks :
                [{'id': 'W1010',
                  'page': '2',
                  'msg': 'message 1',
                  'msg_name': 'short-name-1'}, ...]
        * format - output format(in case of unknown format the default 'text'
                   will be applied) : text|parseable|colorized|msvs|html
        * mute_ids - messages ids to not include in report: ['W1010', 'C2345']
        * report_file - store report to file or to sys.stdout, report file
          will be stored in the work directory with same name as checking
          target file but with prefix '.lintrez'. Options : True|False
        * show_id - show or not full message id in report('W' of 'W0101'): True|Fasle
    """
    # raw format for testing purposes or some other level of communication
    if format == 'raw':
        return rezults
    if format not in REPORTERS_MAPING:
        user_messages.info("No '%s' formatter found(use one of '%s'), using text formating",
                           format, REPORTERS_MAPING.keys())
    formater = REPORTERS_MAPING.get(format, TextReporter)(show_id, mute_ids, path)
    formated_report = formater(rezults)
    if report_file:
        name = path.rsplit(os.path.sep, 1)[1][:-3] + 'lintrez'
        with open(name, 'wb') as f:
            f.write(formated_report)
    else:
        sys.stdout.write(formated_report)
