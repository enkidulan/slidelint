import re

message = re.compile(r"^[A-Z]\d{4}$")
checker = re.compile(r"^[a-z][a-z_]+[a-z]$")
category = re.compile(r"^[A-Z][a-zA-Z]+$")


def clasify(data):
    """Data is string with ids, separated by ',', it returns:
        ([messages_id, ...], [ckeckers_id, ...], [categories_id, ...])
    """
    grouped_ids = ([], [], [])  # messages, checkers, categories
    check_list = (message, checker, category)
    for name in data.split(','):
        results = [ns.match(name) and True for ns in check_list]
        if not any(results):
            raise ValueError("The '%s' in maleformer, it should satisfy on of"
                             "the expresions: '^[A-Z]\d{4}$' or '^[a-z]+$ or"
                             "'^[A-Z][a-z]+$'"%name)
        grouped_ids[results.index(True)].append(name)
    return grouped_ids
