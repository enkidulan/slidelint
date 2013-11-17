""" Text color to background contrast checker """
from slidelint.utils import help_wrapper
import os
import tempdir
import subprocess
from lxml import html
from slidelint.pdf_utils import document_pages_layouts
from pdfminer.layout import LTChar, LTTextLine, LTTextBox
from PIL import Image
import re
from math import exp
from itertools import imap, izip

MESSAGES = (
    dict(id='C3000',
         msg_name='text-readability',
         msg='Text is not readable enough',
         help="Projectors are notorious for not having good contrast."),)


def layout_characters(layout):
    """ yields character boxes or character for layout"""
    for item in layout:
        if isinstance(item, LTChar):
            # pylint: disable=W0212
            if not 'cid' in item._text:
                if ord(item._text) > 32:
                    yield item
        elif isinstance(item, LTTextLine):
            yield [i for i in layout_characters(item)]
        elif isinstance(item, LTTextBox):
            for i in layout_characters(item):
                yield i


def tranform2html(source, dist, out_name='out.html'):
    """ pdftohtml wrapper for transforming PDF to HTML with
    page background images, it returns raw html and list of full
    images paths"""
    outpath = os.path.join(dist, out_name)
    cmd = ['pdftohtml', '-c', '-noframes', '-zoom', '1',
           source, outpath]
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,)
    output = []
    while True:
        output.append(process.stdout.readline())
        retcode = process.poll()
        if process.returncode == 0:
            break
        elif retcode is not None:
            output.extend(process.stdout.readlines())
            output.insert(
                0,
                "pdftohtml died with exit code %s!\n" % retcode
            )
            output.insert(1, " ".join(cmd) + "\n")
            raise IOError("".join(output))
    files = os.listdir(dist)
    files.sort()
    files.pop(files.index(out_name))
    raw_html = open(outpath, 'rb').read()
    return raw_html, [os.path.join(dist, f) for f in files]


class TextColorExtractor(object):
    """ extracts page characters color per page, works with
    pdftohtml generated pages"""
    # this should be replaced by character color extraction
    # from PDF directly
    def __init__(self, raw_html):
        root = html.fromstring(raw_html)
        body = root.find('body')
        styles = [re.findall(r'\.(ft\w+)\{.*color:#([\w|\d]+).*\}', i.text)
                  for i in body.findall("style")]
        self.class_color_mapping = dict(sum(styles, []))
        self.pages = [page for page in body.findall('div')]

    def __call__(self, page_num):
        page = self.pages[page_num]
        colors = []
        for paragraph in page.findall('p'):
            color = self.class_color_mapping[paragraph.get('class', 'ft00')]
            colors.append(
                [(color, character)
                 for character in "".join(paragraph.itertext())
                 if character not in (u'\xa0',) and ord(character) > 32])
        return {
            'text': sum([[j[1] for j in i] for i in colors], []),
            'colors': sum([[j[0] for j in i] for i in colors], [])
        }


def get_text_color_and_background(text_colors, page_layout, page_background):
    """ yields character text, color and background """
    # pylint: disable=R0914
    for characters in layout_characters(page_layout):
        text_set = [i._text for i in characters]  # pylint: disable=W0212
        first = ''.join(text_colors['text']).find(''.join(text_set))
        last = first + len(text_set)
        text_range = slice(first, last)
        del text_colors['text'][text_range]
        colors_set = text_colors['colors'][text_range]
        del text_colors['colors'][text_range]
        for character, color in izip(characters, colors_set):
            # pylint: disable=W0141
            coord_x0, coord_y0, coord_x1, coord_y1 = map(int, character.bbox)
            box = (coord_x0, page_layout.height - coord_y1,
                   coord_x1, page_layout.height - coord_y0)
            character_background = page_background.crop(box)
            yield color, character_background


def goes_throught_pages(source):
    """ yields characters info and its background per page """
    with tempdir.TempDir() as dist:
        raw_html, images = tranform2html(source, dist)
        color_extractor = TextColorExtractor(raw_html)
        document_layout = document_pages_layouts(source)
        for (page_num, page_layout), image in izip(document_layout, images):
            page_background = Image.open(image)
            page_text_colors = color_extractor(page_num)
            page_images = get_text_color_and_background(
                page_text_colors, page_layout, page_background)
            yield page_num, page_images


def html_color_to_grayscale(colorstring):
    """ convert #RRGGBB to an (R, G, B) tuple """
    colorstring = colorstring.strip()
    if colorstring[0] == '#':
        colorstring = colorstring[1:]
    if len(colorstring) != 6:
        raise ValueError("input #%s is not in #RRGGBB format" % colorstring)
    red, green, blue = colorstring[:2], colorstring[2:4], colorstring[4:]
    red, green, blue = [int(n, 16) for n in (red, green, blue)]
    grayscale = red * 299/1000 + green * 587/1000 + blue * 114/1000
    return int(grayscale)


class VisibilityChecker(object):
    """ class for comparing character color to its background"""
    def __init__(self, scale_regress=1, cross_range=50, scale_waight=1):
        self.scale_regress = scale_regress
        self.scale_waight = scale_waight
        self.cross_range = cross_range
        self.exp_scale = [exp(i/10.0) ** self.scale_regress
                          for i in range(1, self.cross_range + 1)]

    def _colors_slice_sum(self, colors_slice):
        """ weight sum of near colors """
        return sum([d / k for k, d in zip(self.exp_scale, colors_slice)])

    def __call__(self, html_color, background):
        histogram = background.convert('L').histogram()
        grayscale_color = html_color_to_grayscale(html_color)
        start = grayscale_color - self.cross_range
        end = grayscale_color + self.cross_range
        total_colors = sum(histogram) + 1
        left_colors_slice = \
            histogram[start if start > 0 else 0:grayscale_color]
        right_colors_slice = \
            histogram[grayscale_color + 1:end if end < 256 else None]
        main_color = histogram[grayscale_color]
        similar_colors = sum(
            imap(self._colors_slice_sum,
                 (left_colors_slice[::-1], right_colors_slice))
        )
        weight = main_color + similar_colors * self.scale_waight
        similarity = weight / total_colors
        return similarity


@help_wrapper(MESSAGES)
def main(target_file=None, scale_regress=0.4,
         max_similarity=0.1, cross_range=70, scale_waight=2):
    """ Text readability checker"""
    scale_regress = float(scale_regress)
    scale_waight = float(scale_waight)
    max_similarity = float(max_similarity)
    cross_range = int(cross_range)
    rez = []
    visibility_checker = VisibilityChecker(
        scale_regress, cross_range, scale_waight)
    for page_num, page_data in goes_throught_pages(target_file):
        for character_color, background in page_data:
            similarity = visibility_checker(character_color, background)
            if similarity > max_similarity:
                rez.append(dict(id='C3000',
                                msg_name='text-readability',
                                msg='Low text color to background contrast.',
                                help="Projectors are notorious for not having "
                                     "good contrast. Your text to too close "
                                     "to the background color and might "
                                     "be unreadable.",
                                page='Slide %s' % (page_num + 1)))
                break
    return rez
