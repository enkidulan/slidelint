#
import logging.config
import os.path

logging.config.fileConfig(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                       'logging.conf'))
