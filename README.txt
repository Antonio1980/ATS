---------------------------------------------------
The "crm"- test project for the CRM coins.exchange.
---------------------------------------------------

Project structure consists from two parts:
------------------------------------------

1. The "tests" package:
 1.1 Test runner file 'tests_container' to run all tests devided by suites.
 1.2 The "test" package is devided by test suites according to presentation in TastRail.
     Test case name convension:
     - every test case must have prefix equals to TC ID in TestRail, for example C2590_login
 1.3 The "pages" package contains crm web pages implented as Selenium classes.
 1.4 The "locators" package contains classes (per page) with HTML locators.


2. The "tests_sources" package:
 2.1 The "drivers" package it's controllable repository to hold a browser executable files.
     The package devided by Unix/Windows artifacts.
     The 'WebDriverFactory' class for creation browser per test request.
 2.2 The "test_data" directory it's static repository to hold test data (csv files).
 2.3 The "test_utils" package as helpers container to extend project abilities.

Configuration:
--------------

- Project configuration stores in base_config.cfg that processes by test_definitions.py class.
- All imports specified in the requirements.txt file.

Technologies:
-------------

- 'unittest' standard Python3.6 library
- 'selenium' 3.12.0 test framework
- 'behave' 1.2.6 framework for Gherkin scenarios.
- 'ddt' framework for data driven tests.
- 'proboscis' framework for tests scheduling.

Preconditions:
--------------

1 PyCharm IDEA installed.
2 Python 3.6 installed.
3 Python virtualenvironment installed out of the project and activated.
4 Python interpreter configured.
5 Project requirements installed.
