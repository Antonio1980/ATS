-----------------------------------------------------------
The "ats"- automation test solution for CRM coins.exchange.
-----------------------------------------------------------

Project structure:
------------------

1. "ATS"  - root directory.

1.1 READ.ME.txt - short description.

1.2 requirements.txt - external packages installation.

2. "src" package:

2.1 "base" package contains core modules: browser, db, me_client, terminal.
2.2 "drivers" package it's controllable repository to hold a browser executable files.
      - The package divided by Unix/Windows artifacts.
      - "WebDriverFactory" class for creation browser per test request.
2.3 "test_data" directory it's static repository to hold any kind of files needed for tests.

2.3.1 "logs" directory to contain log file separately. 
2.4 "test_utils" package as helpers container to extend project abilities.

3. "tests" package home directory for all apps under test.

3.1 "crm" package contains tests cases for crm content for it execution.

      - "test" package is divided by test suites according to TastRail.

      Test case name convension:
      - every test case must have prefix equals to TC ID in TestRail, for example C2590_login

3.1.1 "pages" package contains crm web pages implented as Selenium classes.
3.1.2 "locators" package contains classes (per page) with HTML locators.

3.2 Test runner file 'tests_container' to run all tests divided by suites. 

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
