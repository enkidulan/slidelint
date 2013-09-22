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
      description="",
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
      license='gpl',
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
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      slidelint = slidelint.pipeline_runner:main

      [slidelint.pluggins]
      Text.contents = slidelint.pipes.contents:main
      Text.contrast = slidelint.pipes.text_contrast:main
      Text.size = slidelint.pipes.text_size:main
      Text.edges = slidelint.pipes.edges:main
      Text.outline = slidelint.pipes.text_outline:main
      ContentQuality.grammar = slidelint.pipes.grammar:main
      ContentQuality.gender_pronouns = slidelint.pipes.gender_pronouns:main
      """,
      )
