The "crm"- test project for the CRM coins.exchange.
---------------------------------------------------

Project structure consists from two parts:

1. The "tests" package:
 1.1 The "test" package is devided by test suites according to presentation in TastRail.
 1.2 The "pages" package contains crm web pages implented as Selenium classes.
 1.3 The "locators" package contains classes (per page) with HTML locators.

2. The "tests_sources" package:
 2.1 The "drivers" package it's controllable repository to hold a browser executable files.
     The package devided by Unix/Windows artifacts.
     The 'WebDriverFactory' class for creation browser per test request.
 2.2 The "test_data" directory it's static repository to hold test data (csv files).
 2.3 The "test_utils" package as helpers container to extend project abilities.

Configuration:

- Project configuration stores in base_config.cfg that processes by test_definitions.py class.
- All imports specified in the requirements.txt file.

Technologies:

- 'unittest' standard Python3.6 library
- 'selenium' test framework v. 3.12.0
- 'behave' v. 1.2.6 for Gherkin scenarios.
- 'ddt' framework for data driven tests.
- 'proboscis' framework for tests scheduling.
