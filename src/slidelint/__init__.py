import logging.config as __logging_config
import os.path

__here = os.path.dirname(os.path.abspath(__file__))

__logging_config.fileConfig(os.path.join(__here, 'logging.conf'))
