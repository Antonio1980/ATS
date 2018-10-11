# !/usr/bin/env python
# -*- coding: utf8 -*-

import os
import sys
from setuptools import setup
from distutils.cmd import Command

name = "ats"
rootdir = os.path.abspath(os.path.dirname(__file__))

# Restructured text project description read from file
long_description = open(os.path.join(rootdir, 'README.txt')).read()

# Python 3.4 or later needed
if sys.version_info < (3, 4, 0, 'final', 0):
    raise SystemExit('Python 3.4 or later is required!')

# Build a list of all project modules
packages = []
for dirname, dirnames, filenames in os.walk(rootdir):
    if '__init__.py' in filenames:
        packages.append(dirname.replace('/', '.'))

package_dir = {name: name}

# Data files used e.g. in tests
package_data = {name: [os.path.join(rootdir, 'requirements.txt')]}

# Scripts
scripts = []
for dirname, dirnames, filenames in os.walk('./src/scripts'):
    for filename in filenames:
        if not filename.endswith('.bat'):
            scripts.append(os.path.join(dirname, filename))

# Provide bat executables in the tarball (always for Win)
# if 'sdist' in sys.argv or os.name in ['ce', 'nt']:
#     for s in scripts[:]:
#         scripts.append(s + '.bat')

# Data_files (e.g. doc) needs (directory, files-in-this-directory) tuples
data_files = []
for dirname, dirnames, filenames in os.walk('./src/repository'):
    fileslist = []
    for filename in filenames:
        fullname = os.path.join(dirname, filename)
        fileslist.append(fullname)
    data_files.append(('share/' + name + '/' + dirname, fileslist))


# python setup.py test with distutils
# https://justin.abrah.ms/python/setuppy_distutils_testing.html
class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys, subprocess
        if sys.version_info < (3, 4, 0, 'final', 0):
            raise SystemExit(subprocess.call(['unit2', 'discover', '-s', './tests', '-p', '*_test.py']))
        else:
            raise SystemExit(
                subprocess.call([sys.executable, '-m', 'unittest', 'discover', '-s', './tests', '-p', '*_test.py']))


setup(
    name='ATS',
    version='1.0',
    url='https://gitlab.com/AShipulin/crm.git',
    packages=packages,
    package_dir=package_dir,
    package_data=package_data,
    scripts=scripts,
    license='ASL',
    author='antons',
    author_email='antons@coins.exchange',
    data_files=data_files,
    cmdclass={'test': TestCommand},
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    keywords='argparse distutils selenium unittest',
    description='selenium tests - runs accross of all system.',
    long_description=long_description
)
