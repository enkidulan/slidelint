import logging
logger = logging.getLogger(__name__)

def text(messages):
    pass

def parseable(messages):
    pass

def clorized(messages):
    pass

def msvs(messages):
    pass

def html(messages):
    pass

FORMATTERS = \
    {'text': text,
      'parseable': parseable,
      'clorized': clorized,
      'msvs': msvs,
      'html': html}

class Formatter():
    def __init__(self, format):
        self.format = format if format in FORMATTERS else 'text'
        if format != self.format:
            logger.warn("Format '%s' is unsupported using '%s' instead",
                        format, self.format)
        self.formatter = FORMATTERS[self.format]

    def __call__(self, messages):
        return self.formatter(messages)
