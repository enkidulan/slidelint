import unittest
import testfixtures
from slidelint.resources import PlugginsHandler
from slidelint.resources import EntryPoint as _


class Loadable():
    def __init__(self, name):
        self.name = name

    def load(self):
        return self.name

ALL_ENTRIES = [
    _('checkera', 'CategoryA', Loadable('CategoryA.checkera')),  # 0+---
    _('checkerb', 'CategoryA', Loadable('CategoryA.checkerb')),  # 1+-++
    _('checkerc', 'CategoryA', Loadable('CategoryA.checkerc')),  # 2+---
    _('checkerd', 'CategoryB', Loadable('CategoryB.checkerd')),  # 3++++
    _('checkere', 'CategoryB', Loadable('CategoryB.checkere')),  # 4+++-
    _('checkerf', 'CategoryC', Loadable('CategoryC.checkerf')),  # 5--++
    _('checkerg', 'CategoryD', Loadable('CategoryD.checkerg'))]  # 6+++-


REZ_ENTRIES = [_(n, c, e.load()) for n, c, e in ALL_ENTRIES]


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.handler = PlugginsHandler("")
        self.handler.checkers = ALL_ENTRIES

    def test_all_categiries(self):
        rez = self.handler.load_checkers()
        should_be = REZ_ENTRIES
        testfixtures.compare(rez, should_be)

    def test_enable_category(self):
        rez = self.handler.load_checkers(categories=['CategoryB', 'CategoryD'])
        should_be = REZ_ENTRIES[3:5] + [REZ_ENTRIES[6]]
        testfixtures.compare(rez, should_be)

    def test_disable_category(self):
        rez = self.handler.load_checkers(
            disabled_categories=['CategoryA', 'CategoryD'])
        should_be = REZ_ENTRIES[3:6]
        testfixtures.compare(rez, should_be)

    def test_enable_checker(self):
        rez = self.handler.load_checkers(
            disabled_categories=['AllCategories'],
            checkers=['checkera', 'checkere'])
        should_be = [REZ_ENTRIES[0], REZ_ENTRIES[4]]
        testfixtures.compare(rez, should_be)

    def test_disable_checker(self):
        rez = self.handler.load_checkers(
            disabled_checkers=['checkera', 'checkerf', 'checkerg'])
        should_be = REZ_ENTRIES[1:5]
        testfixtures.compare(rez, should_be)

    def test_mixed(self):
        rez = self.handler.load_checkers(
            categories=['CategoryA', 'CategoryB', 'CategoryD'],
            disabled_categories=['CategoryA'],
            checkers=['checkerb', 'checkerf'],
            disabled_checkers=['checkere', 'checkerg'])
        should_be = [REZ_ENTRIES[3], REZ_ENTRIES[1], REZ_ENTRIES[5]]
        testfixtures.compare(rez, should_be)
