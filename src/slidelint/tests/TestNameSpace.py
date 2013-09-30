import unittest
from testfixtures import compare
from slidelint import namespace


class TestSequenceFunctions(unittest.TestCase):

    def test_message_re(self):
        self.assertIsNotNone(namespace.message.match("W1025"))
        self.assertIsNone(namespace.message.match("e1025"))
        self.assertIsNone(namespace.message.match("1W025"))

    def test_checker_re(self):
        self.assertIsNotNone(namespace.checker.match("validname"))
        self.assertIsNotNone(namespace.checker.match("valid_name_1"))
        self.assertIsNone(namespace.checker.match("Invalidname"))
        self.assertIsNone(namespace.checker.match("_invalidname"))
        self.assertIsNone(namespace.checker.match("invalidname_"))
        self.assertIsNone(namespace.checker.match("3invalidname"))

    def test_categoty_re(self):
        self.assertIsNotNone(namespace.category.match("ValidName"))
        self.assertIsNotNone(namespace.category.match("Validname"))
        self.assertIsNone(namespace.category.match("Invalid_name"))

    def test_clasify(self):
        compare(namespace.clasify("cheker_a,Category,cheker,W1234,OtherCategory,E2345"),
                (['W1234', 'E2345'], ['cheker_a', 'cheker'], ['Category', 'OtherCategory']))
        compare(namespace.clasify("W1234"),
                (['W1234'], [], []))
        compare(namespace.clasify("cheker"),
                ([], ['cheker'], []))
        compare(namespace.clasify("Category"),
                ([], [], ['Category']))
