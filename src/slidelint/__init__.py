""" Reads in PDF of presentation slides and checks common problems,
outputs a summary report on the problems. """

import logging.config as _logging_config
import os.path

_logging_config.fileConfig(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logging.conf'))
