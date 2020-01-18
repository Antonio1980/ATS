import io
import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

tests = "tests"

name_ = os.path.abspath(os.path.dirname(sys.argv[0]))

if "\\" in name_:
    name = name_.split("\\")[-1]
else:
    name = name_.split("/")[-1]

root_dir = os.path.abspath(os.path.dirname(__file__))

# Restructured text project description read from file
path = os.path.join(root_dir, 'README.md')
long_description_ = io.open(path, encoding="utf-8").read()

# Python 3.4 or later needed
if sys.version_info < (3, 4, 0, 'final', 0):
    raise SystemExit('Python 3.4 or later is required!')

# Build a list of all tests classes.
test_cases = []
for dirname, dir_names, filenames in os.walk(os.path.join(root_dir, tests)):
    if 'NF' or 'READY' in filenames:
        pass
    elif '__init__.py' in filenames:
        test_cases.append(dirname.replace('/', '.'))

package_dir = {name: name}

# Data files used e.g. in tests
drivers = {name: [os.path.join(name, 'src/drivers')]}

# Scripts- ./build/scripts
scripts = []
for dirname, dir_names, filenames in os.walk(os.path.join(root_dir, 'src/scripts')):
    for filename in filenames:
        if filename.endswith('.js') or filename.endswith('.sh'):
            scripts.append(os.path.join(dirname, filename))

# Data_files (e.g. doc) needs (directory, files-in-this-directory) tuples- ./build/data
data_files = []
for dirname, dir_names, filenames in os.walk(os.path.join(root_dir, 'src/repository')):
    files_list = []
    for filename in filenames:
        fullname = os.path.join(dirname, filename)
        files_list.append(fullname)
    data_files.append((dirname, files_list))


# python setup.py test with distutils- https://justin.abrah.ms/python/setuppy_distutils_testing.html

# python setup.py test with distutils- https://justin.abrah.ms/python/setuppy_distutils_testing.html
class PyTest(TestCommand):
    user_options = [("pytest-args=", "v", "--alluredir=src/allure_results", )]

    def __init__(self, dist, **kw):
        super().__init__(dist, **kw)
        self.pytest_args = ""

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import shlex
        import pytest

        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)

# python setup.py test
setup(
    name=name,
    version='2.0',
    url='https://gitlab.com/cx_group/qa/platform-server_qa.git',
    setup_requires=["pytest-runner", ],
    tests_require=["pytest", ],
    packages=test_cases,
    package_dir=package_dir,
    package_data=drivers,
    scripts=scripts,
    license='ASL',
    author='antons',
    author_email='antons@coins.exchange',
    data_files=data_files,
    cmdclass={'test': PyTest},
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
    keywords='argparse distutils selenium unittest pytest python',
    description='selenium tests - runs front of web platform.',
    long_description=long_description_
)
