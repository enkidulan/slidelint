"""
Output handlers and formatters
"""
import os
import sys
from colorama import Fore

import logging
USER_MESSAGES = logging.getLogger('user_messages')


def encoding_normalazer(messages):
    """ encodes message report text to utf-8 """
    for msg in messages:
        for key, value in msg.items():
            if isinstance(value, basestring):
                value = value.encode('utf-8')
            msg[key] = value
        yield msg


class BaseReporter(object):
    """ Basic class for creating reports from raw checks results"""
    only_full_id = False
    header = ["********************** Slide Deck {path}"]
    footer = [""]
    formatter = None

    def __init__(self, show_id, mute_ids, path):
        self.show_id = self.only_full_id or show_id
        self.mute_ids = mute_ids
        self.path = os.path.split(path)[1]
        self.update_title()

    def update_title(self):
        """ setts title of report """
        self.header[0] = self.header[0].format(path=self.path)

    def preformatfix(self, msg):
        """ update result message message data """
        msg['msg_id'] = msg['id'][0] if not self.show_id else msg['id']
        msg['path'] = self.path
        return msg

    def apply_formating(self, messages):
        """ formats report messages """
        return [self.formatter.format(**msg)
                for msg in encoding_normalazer(messages)]

    def __call__(self, report):
        filtred = [self.preformatfix(msg)
                   for msg in report if msg['id'] not in self.mute_ids]
        fixed_isd = [self.preformatfix(msg) for msg in filtred]
        rez = self.header + self.apply_formating(fixed_isd) + self.footer
        return "\n".join(rez) + "\n"


class TextReporter(BaseReporter):
    """ Text reporter """
    formatter = '{msg_id}:{page}: {msg} ({msg_name})'


class ParseableTextReporter(BaseReporter):
    """ Parseable Text reporter """
    only_full_id = True
    formatter = '{path}:{page}: [{msg_id}({msg_name}), ] {msg}'


class VSTextReporter(BaseReporter):
    """ VS Text reporter """
    only_full_id = True
    formatter = '{path}({page}): [{msg_id}({msg_name})] {msg}'


class ColorizedTextReporter(BaseReporter):
    """ Colorized Text reporter """
    formatter = '{msg_id}:{page}: {msg} ({msg_name})'
    COLOR_MAPPING = {
        'C': Fore.RED,  # pylint: disable=E1101
        'W': "",
    }

    def apply_formating(self, messages):
        # pylint: disable=E1101
        return [self.COLOR_MAPPING.get(msg['id'][0], "") +
                self.formatter.format(**msg) + Fore.RESET
                for msg in messages]


class HTMLTextReporter(BaseReporter):
    """ HTML Text reporter """
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

    def update_title(self):
        self.header[-1] = self.header[-1] % self.path

    def apply_formating(self, messages):
        return ['<p>' + self.formatter.format(**msg) + '</p>'
                for msg in messages]


REPORTERS_MAPING = {
    'text': TextReporter,
    'parseable': ParseableTextReporter,
    'colorized': ColorizedTextReporter,
    'msvs': VSTextReporter,
    'html': HTMLTextReporter}


def output_handler(path, rezults, mute_ids='', output_format='text',
                   report_file=False, show_id=False):
    """
    Formating check results and handling its output.
    Takes:
        * path - path to checking file: 'path/to/file.pdf'
        * rezults - results of checks :
                [{'id': 'W1010',
                  'page': '2',
                  'msg': 'message 1',
                  'msg_name': 'short-name-1'}, ...]
        * output_format - output format(in case of unknown format
                          the default 'text' will be applied) :
                          text|parseable|colorized|msvs|html
        * mute_ids - messages ids to not include in report: ['W1010', 'C2345']
        * report_file - store report to file or to sys.stdout, report file
          will be stored in the work directory with same name as checking
          target file but with prefix '.lintrez'. Options : True|False
        * show_id - show or not full message id in report('W' of 'W0101'):
                    True|Fasle
    """
    # raw format for testing purposes or some other level of communication
    if output_format == 'raw':
        return rezults
    if output_format not in REPORTERS_MAPING:
        USER_MESSAGES.info(
            "No '%s' formatter found(use one of '%s'), using text formating",
            output_format,
            REPORTERS_MAPING.keys())
    formater = REPORTERS_MAPING.get(output_format, TextReporter)(
        show_id, mute_ids, path)
    formated_report = formater(rezults)
    if report_file:
        name = os.path.split(path)[1][:-3] + 'lintrez'
        with open(name, 'wb') as output_file:
            output_file.write(formated_report)
    else:
        sys.stdout.write(formated_report)
