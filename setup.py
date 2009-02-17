from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='PyoC',
      version=version,
      description="PyoC is an IoC container for Python projects",
      long_description="""\
To be determined.""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='IoC Dependency Injection',
      author='Bernardo Heynemann',
      author_email='heynemann@gmail.com',
      url='http://www.pyoc.org',
      license='OSI',
      packages=["pyoc",],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
