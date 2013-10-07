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
          'configparser',  # only for python2
          'colorama',
          'pdfminer',
          'lxml',
          # '3to2',
          # 'language_tool', # don't work with python2
          # 'nltk', # not release for python3
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      slidelint = slidelint.cli:cli

      [slidelint.pluggins]
      Text.contents = slidelint.checkers.contents:main
      Text.fontsize = slidelint.checkers.fontsize:main
      Text.edges_danger_zone = slidelint.checkers.edges_danger_zone:main
      ContentQuality.language_tool_checker = slidelint.checkers.language_tool_checker:main

      [slidelint.tests]
      TestGroupOne.test_cheker_1 = slidelint.tests.files.test_modules:group1_cheker1
      TestGroupOne.test_cheker_2 = slidelint.tests.files.test_modules:group1_cheker2
      TestGroupTwo.test_cheker_3 = slidelint.tests.files.test_modules:group2_cheker1
      """,
      )


def dowload_language_tool():
    import zipfile
    import urllib2
    import shutil
    import tempfile
    here = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src', 'slidelint')
    language_tool = os.path.join(here, 'LanguageTool')
    if os.path.exists(language_tool):
        # no need to load LanguageTool again
        return
    url = 'http://www.languagetool.org/download/LanguageTool-stable.zip'
    req = urllib2.urlopen(url)
    with tempfile.NamedTemporaryFile() as tf:
        shutil.copyfileobj(req, tf)
        tf.file.seek(0)
        zfile = zipfile.ZipFile(tf.name)
        zfile.extractall(here)
        os.rename(os.path.join(here, zfile.namelist()[0]), language_tool)


dowload_language_tool()
