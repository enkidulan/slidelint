from setuptools import setup, find_packages
import os

version = '1.0dev'

long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='slidelint',
      version=version,
      description="Reads in PDF of presentation slides and checks common problems, outputs a summary report on the problems.",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='',
      license='apache2.0 (http://www.apache.org/licenses/LICENSE-2.0)',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      # namespace_packages=['slidelint'],
      extras_require={
          'tests': ['testfixtures',
                    'nose',
                    'nose-selecttests',
                    'coverage']
      },
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'docopt',
          'configparser',
          'colorama',
          'pdfminer',
          'nltk'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      slidelint = slidelint.cli:cli

      [slidelint.pluggins]
      Text.contents = slidelint.checkers.contents:main
      Text.fontsize = slidelint.checkers.fontsize:main

      [slidelint.tests]
      TestGroupOne.test_cheker_1 = slidelint.tests.files.test_modules:group1_cheker1
      TestGroupOne.test_cheker_2 = slidelint.tests.files.test_modules:group1_cheker2
      TestGroupTwo.test_cheker_3 = slidelint.tests.files.test_modules:group2_cheker1
      """,
      )
