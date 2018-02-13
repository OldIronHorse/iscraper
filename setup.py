from setuptools import setup

setup(name='iscraper',
      version='0.1',
      description='',
      url='http://github.com/oldironhorse/iscraper',
      license='GPL 3.0',
      packages=['iscraper'],
      install_requires=[
        'bs4',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
