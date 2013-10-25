from slidelint.utils import help
from slidelint.pdf_utils import convert_pdf_to_text
import os
import subprocess
from lxml import etree
import urllib2
import urllib
import socket
from appdirs import user_data_dir
import requests

package_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lt_path = os.path.join(package_root, 'LanguageTool')


def get_free_port(file_to_store):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.bind(('', 0))
    sock.listen(socket.SOMAXCONN)
    ipaddr, port = sock.getsockname()
    sock.close()
    with open(file_to_store, 'wb') as f:
        f.write(str(port))
    return str(port)


def get_port(used_port):
    if os.path.isfile(used_port):
        port = open(used_port, 'r').read().strip(' \n')
        if not port:
            return False, get_free_port(used_port)
        try:
            r = requests.get('http://localhost:%s' % port, timeout=0.3)
        except:
            return False, get_free_port(used_port)
        if 'LanguageTool' in r.text:
            return True, port
    return False, get_free_port(used_port)


class LanguagetoolServer():

    def __init__(self, path):
        config_dir = user_data_dir('slidelint')
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        used_port = os.path.join(config_dir, 'used_port')
        started, self.port = get_port(used_port)
        if not started:
            cmd = ['java', '-cp', os.path.join(path, 'languagetool-server.jar'),
                   'org.languagetool.server.HTTPServer', '--port', self.port]
            self.process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,)
            while 'Server started' not in self.process.stdout.readline():
                # waiting for server start
                pass

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
        pass
        # self.process.kill()


messages = (
    dict(id='C1010',
         msg_name='language-tool',
         msg='Language tool',
         help="Language tool found error"),)


def main(target_file=None, msg_info=None):
    if msg_info:
        return help(messages, msg_info)
    pages = convert_pdf_to_text(target_file)
    rez = []
    with LanguagetoolServer(lt_path) as grammar_checker:
        for num, page in enumerate(pages):
            for paragraph in page:
                # fixing new-lines and spaces for languagetool
                paragraph = paragraph.replace(' \n', ' ').replace('\n ', ' ').replace('\n', ' ')
                for error in grammar_checker(paragraph):
                    rez.append({
                        'id': 'C1010',
                        'page': '%s' % (num + 1),
                        'msg_name': error.get('ruleId'),
                        'msg': '%s - %s' % (error.get('locqualityissuetype'),
                                                error.get('msg')),
                        'help': error.get('context')})
    return rez
