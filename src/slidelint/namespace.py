""" namespace helper module - it contains functions for names
validation and classification """
import re

MESSAGE = re.compile(r"^[A-Z]\d{4}$")
CHECKER = re.compile(r"^[a-z][a-z_0-9]+[a-z0-9]$")
CATEGORY = re.compile(r"^[A-Z][a-zA-Z]+$")


def valid_category_id(name):
    """ validate category name """
    if not CATEGORY.match(name):
        raise NameError("Id '%s' is not allowed for category" % name)
    return name


def valid_checker_id(name):
    """ validate checker name """
    if not CHECKER.match(name):
        raise NameError("Id '%s' is not allowed for checker" % name)
    return name


def valid_message_id(name):
    """ validate message name """
    if not MESSAGE.match(name):
        raise NameError("Id '%s' is not allowed for message" % name)
    return name


VALIDATORS_MAPPING = {
    "message": valid_message_id,
    "checker": valid_checker_id,
    "category": valid_category_id,
}


def validate_ids(validator_name, names):
    """ name space validator"""
    validator = VALIDATORS_MAPPING[validator_name]
    for name in names:
        validator(name)


def clasify(data):
    """Data is string with ids, separated by ',', it returns:
        ([messages_id, ...], [ckeckers_id, ...], [categories_id, ...])
    """
    grouped_ids = ([], [], [])  # messages, checkers, categories
    if data:
        check_list = (MESSAGE, CHECKER, CATEGORY)
        for name in data.split(','):
            results = [ns.match(name) and True for ns in check_list]
            if not any(results):
                raise ValueError("The '%s' in maleformer, it should satisfy "
                                 "on of the expresions: '^[A-Z]\\d{4}$' "
                                 "or '^[a-z]+$ or '^[A-Z][a-z]+$'" % name)
            grouped_ids[results.index(True)].append(name)
    return grouped_ids
