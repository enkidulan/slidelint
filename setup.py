from setuptools import setup, find_packages
import sys, os

version = '0.1dev'

setup(name='slidelint',
      version=version,
      description="Reads in PDF of presentation slides and checks common problems, outputs a summary report on the problems.",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='',
      author_email='supamaxy@gmail.com',
      url='',
      license='',
      packages=find_packages('src', exclude=['ez_setup', 'examples', 'tests']),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      tests_require = ['testfixtures'],
      install_requires=[
          'setuptools',
          'docopt',
          'configparser',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      [console_scripts]
      slidelint = slidelint.cli:main
      [slidelint.text]
      contents = slidelint.pipes.contents:main
      text_contrast = slidelint.pipes.text_contrast:main
      text_size = slidelint.pipes.text_size:main
      edges = slidelint.pipes.edges:main
      text_outline = slidelint.pipes.text_outline:main
      [slidelint.content_quality]
      grammar = slidelint.pipes.grammar:main
      gender_pronouns = slidelint.pipes.gender_pronouns:main
      # -*- Entry points: -*-
      """,
      )
