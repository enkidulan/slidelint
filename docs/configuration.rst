Configuration file
==================

To define a set of checks that should be applied to the document use config file.

The config file architecture:
    * The main section is CATEGORIES. In this section the categories of checks that will be applied to a file are defined.
    * Categories sections. In the category section the list of checkers to apply is defined.
    * Checkers sections. In these sections checker configuration is defined.

Also there is no need to define a section for each checker or category to apply it,
just write its entry_points name.

To create a checking pipeline define config file:

::

    [CATEGORIES]
    enable =
        CategoryA
        CategoryB
        CategoryC
    disable =
        CategoryC

    [CategoryA]
    category = CategoryA
    enable =
        checker1
        checker2
        checker3
    disable =
        checker3

    [checker1]
    checker = checker1
    arg1 = 1
    arg2 = 2

In this example the checks set consists of two categories: CategoryA and CategoryB.
The first category is defined as a section in config file. It has a name and a list of its checkers for applying. Second category is not defined as section in config file so all checkers from this category will be applied by default. The same goes for checker’s definition. checker1 is defined as a section, it has its name and some custom arguments that will be passed on to it when it is called. The checker2 will be called with its default arguments. checker3 won't be called because it was disabled.


Configuring pipeline through command line
-------------------------------------------

Let’s suppose  that we have default configuration file that look like this:

::

    [CATEGORIES]
    enable =
        CategoryA
        CategoryB

    [CategoryA]
    category = CategoryA
    enable =
        checker1
        checker2

But slidelint was called with the following arguments:

::

    $ slidelint -e checker3,CategoryC -d CategoryB,checker2,checker1 example.pdf

So actual pipeline representation will look like this:

::

    [CATEGORIES]
    categories =
        CategoryA
        CategoryC

    [CategoryA]
    category = CategoryA
    enable =
        checker3

Checker enabling is allowed only in the enabled category. Removing operation goes after extending.
