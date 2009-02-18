from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='PyoC',
      version=version,
      description="PyoC is an IoC container for Python projects",
      long_description="""\
============
Introduction
============
PyoC is an IoC container for Python. It's purpose is to make it even easier (it's easy already in Python) to manage dependencies between components. 

It's heavily oriented towards a Convention-over-Configuration approach.

===================
Project Cheat Sheet
===================

Project Google Groups Page - http://groups.google.com/group/pythonioc

Project Conventions: http://groups.google.com/group/pythonioc/web/conventions

Links and Blog Posts: http://groups.google.com/group/pythonioc/web/Links%20and%20Blog%20Posts

Project JIRA (Issue and Version Management) - 
http://jira.stormwindproject.org:8080/browse/PYOC

Project Subversion Server: http://svn.stormwindproject.org/svn/PyoC/Trunk/ (``svn 
co http://svn.stormwindproject.org/svn/PyoC/Trunk/ PyoC``)

**PyPI Page**: -

**Docs for current version**: -""",
      classifiers=["Development Status :: 2 - Pre-Alpha",
				   "Intended Audience :: Developers",
				   "License :: OSI Approved",
				   "Natural Language :: English",
				   "Programming Language :: Python :: 2.5",], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
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
