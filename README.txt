--------------------------------------------------------------------------------------------
The "ATS"- "automation test solution" test project for the BackEnd/FrontEnd @coins.exchange.
--------------------------------------------------------------------------------------------

Project structure:
------------------

1. "ATS"  - root, project directory.

1.1 READ.ME.txt - project description.

1.2 requirements.txt - external packages dependencies.

1.3 .gitignore - to prevent upload redundant data as cache, builds etc.

1.4 base_config.cfg - configuration file (URL's, credentials, Data etc.).

1.5 setup.py - build script of the project.

1.6 test_definitions.py - python converter for the configuration data.


2. "src" package:

2.1 "base" package contains core modules: base_exception, browser, enums, http_client, instruments, terminal.
- Browser class (selenium methods implementation).
- HTTPClient class (used to send requests via HTTP or HTTPS).
- Instruments class (provides set of utilities for different needs).
- Terminal class (ability to execute any terminal or cmd command).

2.2 "drivers" package it's controllable repository to hold a browser executable files.
      - The package divided by Unix/Windows artifacts.
      - "WebDriverFactory" class for creation browser per test request.

2.3 "repository" directory it's static repository to hold any kind of files needed for testing.

2.4 "scripts" directory stores any kind of JavaScript, Shell/Bash etc.


3. "tests" package home directory for all apps under test.

3.1 "tests_api" package contains test for the  ACL API.

3.2 "tests_crm_bo" package contains test context for crm-bo apps.

      - internally the same schema as crm_bo_qa project.

3.3 "tests_end2end".

3.4 "tests_me_admin".

      - internally the same schema as me project.

3.5  "tests_web_platform".

      - internally the same schema as platform-server_qa project.

3.6 Test container file 'crm_tests_container' to group all tests into test suites for execution.

3.7 Test runner file 'crm_tests_runner' to execute suites from container (ordered execution).


Location:
---------

- SSH: git@gitlab.com:AShipulin/crm.git
- HTTPS: https://gitlab.com/AShipulin/crm.git

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
