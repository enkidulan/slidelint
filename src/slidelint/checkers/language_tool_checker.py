from slidelint.utils import help
from slidelint.pdf_utils import convert_pdf_to_text
import os
import subprocess
from lxml import etree
import urllib2
import urllib

lt_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'LanguageTool')


class LanguagetoolServer():

    def __init__(self, path, port='8081'):
        cmd = ['java', '-cp', os.path.join(path, 'languagetool-server.jar'),
               'org.languagetool.server.HTTPServer', '--port', port]
        self.port = port
        self.process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,)

    def grammar_checker(self, text, language="en-US"):
        url = 'http://127.0.0.1:%s' % self.port
        data = dict(language=language, text=text)
        req = urllib2.Request(url, data=urllib.urlencode(data))
        content = urllib2.urlopen(req).read()
        root = etree.fromstring(content)
        return root.findall('error')

    def __enter__(self):
        return self.grammar_checker

    def __exit__(self, type, value, traceback):
        self.process.kill()


messages = (
    dict(id='C1010',
         msg_name='language-tool',
         msg='Language tool',
         help="Language tool found error"),)


def main(target_file=None, msg_info=None):
    if msg_info:
        return help(messages, msg_info)
    pages = convert_pdf_to_text(target_file).replace('\n\n', ' ').split('\x0c')
    rez = []
    with LanguagetoolServer(lt_path) as grammar_checker:
        for num, page in enumerate(pages):
            for error in grammar_checker(page):
                rez.append({
                    'id': 'C1010',
                    'page': num,
                    'msg_name': 'language-tool-%s' % error.get('ruleId'),
                    'msg': '%s - %s' % (error.get('locqualityissuetype'),
                                            error.get('msg')),
                    'help': error.get('context')})
    return rez
