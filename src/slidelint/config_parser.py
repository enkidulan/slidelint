""" Configuration files parsing utilities """
import os.path
from configparser import ConfigParser
from slidelint import namespace

import logging
LOGGER = logging.getLogger(__name__)
USER_MESSAGES = logging.getLogger('user_messages')


def enables_disables(entry):
    """ Passes and cleans 'enable' and 'disable' entries for
    some section. It takes dict alike 'entry' object and return tuple of
    lists (enable, disable) entries of that section."""
    enables = [i for i in entry.get('enable', '').split('\n') if i]
    disables = [i for i in entry.get('disable', '').split('\n') if i]
    return enables, disables


class LintConfig(object):
    """Reads config from given file(or default file) and parse it.
    Also extend self enable/disable lists with given(as comma separated string
    - command line option) enable/disable ids.
    """
    def __init__(self, configfile_path=""):
        path = configfile_path and \
            os.path.isfile(configfile_path) and \
            configfile_path
        if not path:
            USER_MESSAGES.info(
                "No config file found, using default configuration")
            here = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(here, 'default.cfg')
        self.config = ConfigParser()
        self.config.read(path)
        self.categories = []
        self.disable_categories = []
        self.checkers = []
        self.checkers_ids = []
        self.disable_checkers = []
        self.messages = []
        self.disable_messages = []
        self.checker_args_cache = None
        self.parse_config()

    def _handle_categories(self):
        """
        Hands loading of categories and theirs entries from config file.
        """
        rez_cat = []
        for category in self.categories:
            if category in self.disable_categories:
                continue
            if category in self.config:
                name = namespace.valid_category_id(
                    self.config[category]['category'])
                if name in self.disable_categories:
                    continue
                rez = enables_disables(self.config[category])
                # category defined as section but has no configuration so take
                # its name only
                if not any(rez):
                    rez_cat.append(name)
                else:
                    self.checkers += rez[0]
                    self.disable_checkers += rez[1]
            else:
                rez_cat.append(namespace.valid_category_id(category))
        return rez_cat

    def _handle_disable_categories(self):
        """ Parses config and returns categories ids for disabling """
        rez_cat = []
        for category in self.disable_categories:
            if category in self.config:
                name = self.config[category]['category']
            else:
                name = category
            rez_cat.append(namespace.valid_category_id(name))
        return rez_cat

    def _handle_checkers(self):
        """
        Handles loading of checkers and theirs args to enable lists
        """
        rez_chkr = []
        for checker in self.checkers:
            if checker in self.config:
                kwargs = dict(self.config[checker].items())
                name = namespace.valid_checker_id(kwargs.pop('checker'))
                rez_chkr.append((name, kwargs))
            else:
                rez_chkr.append((namespace.valid_checker_id(checker), {}))
        return rez_chkr

    def _handle_disable_checkers(self):
        """ Parses config file and returns checkers ids for disabling """
        rez_chkr = []
        for checker in self.disable_checkers:
            name = self.config[checker]['checker'] \
                if checker in self.config else checker
            rez_chkr.append(namespace.valid_checker_id(name))
        return rez_chkr

    def parse_config(self):
        """
        Transform config file into Pluggins acceptable list of enables and
        disables.
        """
        if 'CATEGORIES' in self.config:
            self.categories, self.disable_categories = \
                enables_disables(self.config['CATEGORIES'])
        if 'CHECKERS' in self.config:
            self.checkers, self.disable_checkers = \
                enables_disables(self.config['CHECKERS'])
        if 'MESSAGES' in self.config:
            self.messages, self.disable_messages = \
                enables_disables(self.config['MESSAGES'])
        namespace.validate_ids('message', self.messages)
        namespace.validate_ids('message', self.disable_messages)
        # handle_disable_categories should be called before handle_categories
        self.disable_categories = self._handle_disable_categories()
        # handle_categories should be called after handle_disable_categories
        self.categories = self._handle_categories()
        self.checkers = self._handle_checkers()
        self.disable_checkers = self._handle_disable_checkers()
        self.checkers_ids = [i[0] for i in self.checkers]

    def compose(self, pluggins, enables, disables):
        """
        Extends configuration with additional parameters (command line options)
        """
        messages, echeckers, categories = namespace.clasify(enables)
        self.categories += categories
        self.checkers += [(i, {}) for i in echeckers]
        self.messages += messages
        messages, checkers, categories = namespace.clasify(disables)
        self.disable_categories += categories
        self.disable_checkers += \
            [c.name for c in pluggins if c.category
             in self.disable_categories and c.name not in echeckers]
        self.disable_checkers += checkers
        self.disable_messages += messages
        self.checkers_ids = [i[0] for i in self.checkers]

    def get_checker_args(self, name):
        """ parses checker args from config-file; returns kwarg dict"""
        if not self.checker_args_cache:
            self.checker_args_cache = dict(self.checkers)
        return self.checker_args_cache.get(name, {})
