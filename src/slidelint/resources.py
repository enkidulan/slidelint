import pkg_resources
from collections import namedtuple

Checker = namedtuple('Checker', ['name', 'category', 'entry_point'])


class PlugginsHandler():
    """Loads all entry points from pkg_resources that belongs to the group,
    by default - slidelint.pluggins"""

    def __init__(self, group="slidelint.pluggins"):
        """Construct list of all entry_points belongs to the group
        """
        checkers = []
        for dist in pkg_resources.working_set:
            entries = dist.get_entry_map(group)
            for full_name, entrie in entries.items():
                category, name = full_name.split(".")
                checkers.append(Checker(name, category, entrie))
        self.checkers = checkers

    def load_checkers(self, categories=['AllCategories'], checkers=[],
                      disabled_categories=[], disabled_checkers=[]):
        """
        Return list of Checker namedtuple objects ('name', 'category', 'entry_point')
        If no args passed return all checkers.
        """
        checkers_for_loading = self.checkers if categories[0] == "AllCategories" else \
            [c for c in self.checkers if c.category in categories]
        if disabled_categories:
            checkers_for_loading = [] if disabled_categories[0] == "AllCategories" else \
                [c for c in checkers_for_loading if c.category not in disabled_categories]
        if checkers:
            checkers_for_loading += [c for c in self.checkers if c.name in checkers and c not in checkers_for_loading]
        if disabled_checkers:
            checkers_for_loading = [c for c in checkers_for_loading if c.name not in disabled_checkers]
        return checkers_for_loading
