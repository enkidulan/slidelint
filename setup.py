from setuptools import setup, find_packages
import os
import sys
import zipfile
import urllib2
import shutil
from tempfile import NamedTemporaryFile
from setuptools.command.develop import develop
from setuptools.command.install import install
from os.path import join

here = os.path.dirname(os.path.abspath(__file__))


class RequestProgressWrapper():
    """ Simple helper for displaying file download progress;
    if works with file-like objects"""
    def __init__(self, obj):
        self.obj = obj
        self.total_size = float(obj.info().getheader('Content-Length').strip())
        self.url = obj.url
        self.bytes_so_far = 0

    def read(self, length):
        self.bytes_so_far += length
        percent = self.bytes_so_far / self.total_size
        percent = round(percent * 100, 2)
        sys.stdout.write("%s: downloaded %d of %d bytes (%0.f%%)\r" %
           (self.url, self.bytes_so_far, self.total_size, percent))
        sys.stdout.flush()
        return self.obj.read(length)

    def __del__(self):
        sys.stdout.write('\n')


def download_ziped_resource(path, url, name, unzip=False):
    """ files download helper """
    full_path = join(path, name)
    if os.path.exists(full_path):
        return
    req = urllib2.urlopen(url)
    data_destination = NamedTemporaryFile() if unzip else open(full_path, 'wb')
    with data_destination as f:
        shutil.copyfileobj(RequestProgressWrapper(req), f)
        if unzip:
            f.file.seek(0)
            zfile = zipfile.ZipFile(f.name)
            zfile.extractall(path)
            os.rename(os.path.join(path, zfile.namelist()[0]), full_path)


def data_loader(command_subclass):
    """A decorator for classes subclassing one of the setuptools commands.

    It modifies the run() method so that it prints a friendly greeting.
    """
    orig_run = command_subclass.run

    def modified_run(self):
        orig_run(self)
        base_path = join(self.install_lib or join(here, 'src'), 'slidelint')
        self.execute(
            download_ziped_resource,
            (base_path,
             'http://www.languagetool.org/download/LanguageTool-stable.zip',
             'LanguageTool',
             True),
            msg="Downloading LanguageTool")
    command_subclass.run = modified_run
    return command_subclass


@data_loader
class DevelopCommand(develop):
    pass


@data_loader
class InstallCommand(install):
    pass


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
      package_dir = {'': 'src'},
      packages=find_packages('src', exclude=('slidelint.tests', 'slidelint.tests.*')),
      # namespace_packages=['slidelint'],
      cmdclass={'install': InstallCommand,
                'develop': DevelopCommand},
      extras_require={
          'tests': ['testfixtures',
                    'nose',
                    'nose-selecttests',
                    'coverage',
                    'fabric']
      },
      package_data = {'':['default.cfg', 'logging.conf', 'checkers/regex_rules/gendered_pronouns']},
      zip_safe=False,
      install_requires=[
          'setuptools',
          'docopt',
          'configparser',
          'colorama',
          'pdfminer==20110515',
          'lxml',
          'tempdir',
          'pillow',
          'appdirs',
          'requests',
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
      Text.readability = slidelint.checkers.readability:main
      ContentQuality.language_tool_checker = slidelint.checkers.language_tool_checker:main
      ContentQuality.regex_grammar_checker = slidelint.checkers.regex_grammar_checker:main

      [slidelint.tests]
      TestGroupOne.test_cheker_1 = slidelint.tests.files.test_modules:group1_cheker1
      TestGroupOne.test_cheker_2 = slidelint.tests.files.test_modules:group1_cheker2
      TestGroupTwo.test_cheker_3 = slidelint.tests.files.test_modules:group2_cheker1
      """,
      )
