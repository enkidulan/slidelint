import unittest
from testfixtures import compare, ShouldRaise
from slidelint import namespace


class TestSequenceFunctions(unittest.TestCase):

    def test_message_re(self):
        self.assertIsNotNone(namespace.valid_message_id("W1025"))
        with ShouldRaise(NameError("Id 'e1025' is not allowed for message")):
            self.assertIsNone(namespace.valid_message_id("e1025"))
        with ShouldRaise(NameError("Id '1W025' is not allowed for message")):
            self.assertIsNone(namespace.valid_message_id("1W025"))

    def test_checker_re(self):
        self.assertIsNotNone(namespace.valid_checker_id("validname"))
        self.assertIsNotNone(namespace.valid_checker_id("valid_name_1"))
        with ShouldRaise(NameError("Id 'Invalidname' is not allowed for "
                                   "checker")):
            namespace.valid_checker_id("Invalidname")
        with ShouldRaise(NameError("Id '_invalidname' is not allowed for "
                                   "checker")):
            namespace.valid_checker_id("_invalidname")
        with ShouldRaise(NameError("Id 'invalidname_' is not allowed for "
                                   "checker")):
            namespace.valid_checker_id("invalidname_")
        with ShouldRaise(NameError("Id '3invalidname' is not allowed for "
                                   "checker")):
            namespace.valid_checker_id("3invalidname")

    def test_categoty_re(self):
        self.assertIsNotNone(namespace.valid_category_id("ValidName"))
        self.assertIsNotNone(namespace.valid_category_id("Validname"))
        with ShouldRaise(NameError("Id 'Invalid_name' is not allowed "
                                   "for category")):
            namespace.valid_category_id("Invalid_name")

    def test_validate_id(self):
        namespace.validate_ids('message', ['W1025'])
        namespace.validate_ids('checker', ['checker_validname'])
        namespace.validate_ids('category', ['ValidCategoryName'])
        with ShouldRaise(NameError("Id 'imValidCategoryName' is not allowed "
                                   "for category")):
            namespace.validate_ids('category', ['imValidCategoryName'])
        with ShouldRaise(NameError("Id 'checker_Invalidname' is not allowed "
                                   "for checker")):
            namespace.validate_ids('checker', ['checker_Invalidname'])
        with ShouldRaise(NameError("Id 'W10205' is not allowed for message")):
            namespace.validate_ids('message', ['W10205'])

    def test_clasify(self):
        cmd = "cheker_a,Category,cheker,W1234,OtherCategory,E2345"
        compare(namespace.clasify(cmd),
                (['W1234', 'E2345'],
                 ['cheker_a', 'cheker'],
                 ['Category', 'OtherCategory']))
        compare(namespace.clasify("W1234"),
                (['W1234'], [], []))
        compare(namespace.clasify("cheker"),
                ([], ['cheker'], []))
        compare(namespace.clasify("Category"),
                ([], [], ['Category']))

if __name__ == '__main__':
    unittest.main()
