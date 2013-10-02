import os.path
from configparser import ConfigParser
from slidelint import namespace

import logging
logger = logging.getLogger(__name__)

here = os.path.dirname(os.path.abspath(__file__))


def enables_disables(entry):
    enables = filter(None, entry['enable'].split('\n') if 'enable' in entry else [])
    disables = filter(None, entry['disable'].split('\n') if 'disable' in entry else [])
    return enables, disables


class LintConfig():
    """Reads config from given file(or default file) and parse it.
    Also extend self enable/disable lists with given(as comma separated string
    - command line option) enable/disable ids
    """
    def __init__(self, configfile_path=""):
        path = configfile_path and os.path.isfile(configfile_path) and configfile_path
        if not path:
            logger.warn("No config file found, using default configuration")
            path = os.path.join(here, 'default.cfg')
        self.config = ConfigParser()
        self.config.read(path)
        self.categories = []
        self.disable_categories = []
        self.checkers = []
        self.checkers_isd = []
        self.disable_checkers = []
        self.messages = []
        self.disable_messages = []
        self.checker_args_cache = None
        self.parse_config()

    def handle_categories(self):
        """
        Handling loading of categories and theirs entries to enable lists
        """
        rez_cat = []
        for category in self.categories:
            if category in self.disable_categories:
                continue
            if category in self.config:
                name = namespace.valid_category_id(self.config[category]['category'])
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
        self.categories = rez_cat

    def handle_disable_categories(self):
        rez_cat = []
        for category in self.disable_categories:
            if category in self.config:
                name = self.config[category]['category']
            else:
                name = category
            rez_cat.append(namespace.valid_category_id(name))
        self.disable_categories = rez_cat

    def handle_checkers(self):
        """
        Handling loading of checkers and theirs args to enable lists
        """
        rez_chkr = []
        for checker in self.checkers:
            if checker in self.config:
                kwargs = dict(self.config[checker].items())
                name = namespace.valid_checker_id(kwargs.pop('checker'))
                rez_chkr.append((name, kwargs))
            else:
                rez_chkr.append((namespace.valid_checker_id(checker), {}))
        self.checkers = rez_chkr

    def handle_disable_checkers(self):
        rez_chkr = []
        for checker in self.disable_checkers:
            name = self.config[checker]['checker'] if checker in self.config else checker
            rez_chkr.append(namespace.valid_checker_id(name))
        self.disable_checkers = rez_chkr

    def parse_config(self):
        """
        Transform config file into Pluggins acceptable list of enables and
        disables.
        """
        if 'CATEGORIES' in self.config:
            self.categories, self.disable_categories = enables_disables(self.config['CATEGORIES'])
        if 'CHECKERS' in self.config:
            self.checkers, self.disable_checkers = enables_disables(self.config['CHECKERS'])
        if 'MESSAGES' in self.config:
            self.messages, self.disable_messages = enables_disables(self.config['MESSAGES'])
        map(namespace.valid_message_id, self.messages)
        map(namespace.valid_message_id, self.disable_messages)
        self.handle_disable_categories()  # should be before handle_categories
        self.handle_categories()  # should be after handle_disable_categories
        self.handle_checkers()
        self.handle_disable_checkers()
        self.checkers_isd = [i[0] for i in self.checkers]

    def compose(self, enables, disables):
        """
        Extends config file configuration with additional parameters
        """
        messages, checkers, categories = namespace.clasify(enables)
        self.categories += categories
        self.checkers += [(i, {}) for i in checkers]
        self.messages += messages
        messages, checkers, categories = namespace.clasify(disables)
        self.disable_categories += categories
        self.disable_checkers += checkers
        self.disable_messages += messages
        self.checkers_isd = [i[0] for i in self.checkers]

    def get_checker_args(self, name):
        if not self.checker_args_cache:
            self.checker_args_cache = dict(self.checkers)
        return self.checker_args_cache.get(name, {})
