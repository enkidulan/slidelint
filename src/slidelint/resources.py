import pkg_resources

def load_checker(group, name):
    """ loading checker(entry point) from category(group) from pkg_resources
    returns only first found item
    """
    return [entrypoint.load() for entrypoint in
            pkg_resources.iter_entry_points(group, name)][0]


def belongs2category(category, checkers):
    """ Takes category(pkg_resources entry_point group) and list of
    checkers(entry_points names). Returns checkers that belong to category"""
    return [checker for checker in checkers
            if [i for i in pkg_resources.iter_entry_points(category, checker)]]
