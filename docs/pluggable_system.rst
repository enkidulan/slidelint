****************
Pluggable system
****************

The pluggable system is implemented through pkg_resources. To add new checkers
you need to create a package and register checkers as setuptools
entry_points. Each checker should be defined as part of slidelint.pluggins entry_points
group. In this way slidelint implements checker categorization. All checkers are
reachable from slidelint by theirs name.


Defining new checkers and categories
====================================

To make new checker reachable for slidelint simply add it to package
entry_points as part of slidelint.pluggins group.

::

    entry_points="""
        [slidelint.pluggins]
        Text.contents = slidelint.checkers.contents:main
        Text.my_new_checker = my_package.my_new_checker:main
        """

In this code example checker 'my_new_checker' was added to 'Text'
category. You can define your own groups or use already existing categories.


Name space
==========

    * Category : [A-Z][a-zA-Z]+ (Text, MyNewCategory)
    * Checker : [a-z][a-z_0-9]+[a-z0-9] (contents, my_new_checker1)
    * Message : [A-Z]\d{4} (C0111, W0402)