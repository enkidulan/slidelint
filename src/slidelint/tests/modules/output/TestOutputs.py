import os
import unittest
from testfixtures import OutputCapture, TempDirectory, compare
from slidelint.outputs import output_handler


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.work_dir = os.getcwd()
        self.path = "presentation.pdf"
        self.rezults = [
            {'id': 'W1010',
             'page': '2',
             'msg': 'message 1',
             'msg_name': 'short-name-1'},
            {'id': 'C5010',
             'page': '4',
             'msg': 'message 4',
             'msg_name': 'short-name-4'}]

    def tearDown(self):
        os.chdir(self.work_dir)

    def test_defaults(self):
        with OutputCapture() as output:
            output_handler(self.path, self.rezults)
        output.compare(
            "********************** Slide Deck presentation.pdf\n"
            "W:2: message 1 (short-name-1)\n"
            "C:4: message 4 (short-name-4)\n")

    def test_message_show_ids(self):
        with OutputCapture() as output:
            output_handler(self.path, self.rezults, show_id=True)
        output.compare(
            "********************** Slide Deck presentation.pdf\n"
            "W1010:2: message 1 (short-name-1)\n"
            "C5010:4: message 4 (short-name-4)\n")

    def test_message_mute_ids(self):
        with OutputCapture() as output:
            output_handler(self.path, self.rezults, mute_ids=['W1010'])
        output.compare(
            "********************** Slide Deck presentation.pdf\n"
            "C:4: message 4 (short-name-4)\n")

    def test_parseable_format(self):
        with OutputCapture() as output:
            output_handler(self.path, self.rezults, output_format='parseable')
        output.compare(
            "********************** Slide Deck presentation.pdf\n"
            "presentation.pdf:2: [W1010(short-name-1), ] message 1\n"
            "presentation.pdf:4: [C5010(short-name-4), ] message 4\n")

    def test_msvs_format(self):
        with OutputCapture() as output:
            output_handler(self.path, self.rezults, output_format='msvs')
        output.compare(
            "********************** Slide Deck presentation.pdf\n"
            "presentation.pdf(2): [W1010(short-name-1)] message 1\n"
            "presentation.pdf(4): [C5010(short-name-4)] message 4\n")

    def test_colorized_format(self):
        with OutputCapture() as output:
            output_handler(self.path, self.rezults, output_format='colorized')
        output.compare(
            "********************** Slide Deck presentation.pdf\n"
            "W:2: message 1 (short-name-1)\x1b[39m\n"
            "\x1b[31mC:4: message 4 (short-name-4)\x1b[39m\n")

    def test_html_format(self):
        with OutputCapture() as output:
            output_handler(self.path, self.rezults, output_format='html')
        output.compare(
            "<!DOCTYPE html>\n"
            "<html>\n"
            "<body>\n"
            "<h1>Slide Deck presentation.pdf</h1>\n"
            "<p>W1010:2: message 1 (short-name-1)</p>\n"
            "<p>C5010:4: message 4 (short-name-4)</p>\n"
            "</body>\n"
            "</html>")

    def test_file_output(self):
        with TempDirectory() as d:
            os.chdir(d.path)
            output_handler(self.path, self.rezults, report_file=True)
            compare(
                d.read('presentation.lintrez'),
                "********************** Slide Deck presentation.pdf\n"
                "W:2: message 1 (short-name-1)\n"
                "C:4: message 4 (short-name-4)\n\n")
