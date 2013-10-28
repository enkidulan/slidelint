""" config file based checker - runs text against set of regexps.
messages and regexps are defined in the config file"""
import re
import os.path
from slidelint.utils import help as help_msg_formatter
from slidelint.pdf_utils import convert_pdf_to_text

here = os.path.dirname(os.path.abspath(__file__))


def get_file_path(path):
    """ Files REGEX finder  """
    path = path.strip()
    if not os.path.sep in path:
        path = os.path.join(here, 'regex_rules', path)
    if os.path.isfile(path):
        return path
    raise ValueError("The file with REGEX rules can't be found: '%s'" % path)


def main(target_file=None, source_file=None, re_options=None, id=None,
         msg_name=None, msg=None, help=None, msg_info=None):
    """ Runner fro regexp config files. Takes rules_source file can """
    pattern = open(get_file_path(source_file), 'rb').read()
    options = [getattr(re, o) for o in re_options.split('\n') if o]
    regexp = re.compile(pattern, *options)
    if msg_info:
        return help_msg_formatter(
                    (dict(id=id, msg_name=msg_name, msg=msg, help=help),),
                    msg_info)
    pages = convert_pdf_to_text(target_file)
    rez = []
    for num, page in enumerate(pages):
        for paragraph in page:
                match = regexp.search(paragraph)
                if match:
                    rez.append({
                        'id': id,
                        'page': 'Slide %s' % (num + 1),
                        'msg_name': msg_name,
                        'msg': '%s: "%s" mentioned in "%s"' % (msg, str(match.group()), paragraph),
                        'help': help})
    return rez
