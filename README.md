
CONTENTS OF THIS FILE
---------------------

 * Introduction
 * Location
 * Technologies
 * Recommended plugins
 * Requirements
 * Tests
 * Configuration
 * Troubleshooting
 * Maintainers

INTRODUCTION
------------

The "A.T.S."- automation test framework covers backend and frontend, provides functionality testing:
- Unit
- API
- UI
- Integration
- EndToEnd
- Load/Performance

LOCATION
---------

- https://github.com/Antonio1980/ATS.git

TECHNOLOGIES
-------------

- pytest - advanced test framework.
- allure-pytest - reporting.
- selenium - test framework.
- ddt - framework for data driven tests.
- redis - access to Redis DB.
- requests - HTTP/S requests.
- PyMySQL - access to SQL DB.
- beautifulsoup4 - work with HTML.

RECOMMENDED PLUGINS
-------------------
- bashsupport - ability to execute shell/bash scripts.
- multirun - ability to run several configurations.
- .gitignore - prevents redundant uploads.
- GitLab - projects integration with remote repo.
- CSV - plugin to support csv files.
- Docker - for docker integration.
- CMD support.

REQUIREMENTS
------------

1. PyCharm IDEA installed.
2. Python 3.6 or later installed.
3. Python virtualenvironment installed out of the project and activated.
4. Python interpreter configured.
5. Project requirements installed.
6. Project plugins installed.

TESTS
-----

1 Run all tests:
* $ pytest -v tests/platform_tests --alluredir=src/repository/allure_results

2 Run tests as a package:
* $ pytest -v tests/platform_tests/trading_sanity_tests --alluredir=src/repository/allure_results

3 Run specific test:
* $ pytest -v tests/platform_tests/api_tests/authorization_service_tests/sign_up_test.py  --alluredir=src/repository/allure_results

4 Run per test group (public_api group as example):
* $ pytest -v tests/platform_tests/api_tests -m public_api --alluredir=src/repository/allure_results

5 Generate temporary allure report:
* $ allure.bat serve src/repository/allure_results
  
6 Generate report:
* $ allure.bat generate src/repository/allure_results -o src/repository/allure_report --clean
  
7 Open allure report:
* $ allure.bat open src/repository/allure_report

8 Show pytest fixtures and execution plan:
* $ pytest --collect-only

9 Ignore Not Finished tests (cross project)
* $ pytest -v tests/platform_tests --ignore-glob='NF*.py'

10 Run tests under tox and pass environment variable:
* $ ENV=int tox -- -m [GROUP_NAME] --alluredir=../src/allure_results

11 Run tests under tox:
* $ tox -- -m [GROUP_NAME] --alluredir=../src/allure_results

* Test Groups:

1. smoke - ui smoke tests includes signup, signin, forgot, etc.
2. ui - ui tests except smoke
3. trading_sanity - sanity for trading
4. payment_sanity - sanity for payment
5. e2e - end to end tests
6. balance - as feature across project
7. withdrawal - as feature across project
8. deposit - as feature across project
9. redis - tests related to redis
10. home_page - tests that covering related page
11. sign_up_page - tests that covering related page
12. add_phone_page - tests that covering related page
13. forgot_password_page - tests that covering related page
14. negative - negative tests include ddt (currently ddt tests are skipped)
15. sign_in_page - tests that covering related page
16. order_book - ui tests for order book
17. maintenance_time - traktor
18. upper_ruler - ui upper ruler
19. order_management - as feature across project
20. market_order - only market orders
21. limit_order - only limit orders
22. hurl - tests for hurl
23. payment - as feature across project
24. public_api - only that opened for public
25. regression - all api tests
26. authorization - as feature across project
27. authorization_service - tests only for desired service


CONFIGURATION
--------------

- Project base configuration stores in config.cfg that processes by config_definitions.py class.

- All imports specified in the requirements.txt file.

* To install all project dependencies run command:
* $ pip install -r requirements.txt

- All base constants initialized in src.base.__init__:

* from src.base import test_token, base_url, crm_base_url, api_base_url, file_svc_url, balance_svc_url

To change URL or test_token of the environment just change value of needed key in config.cfg

- Configuration map:

* test_token = BaseConfig.TEST_TOKEN
* base_url = BaseConfig.WTP_BASE_URL
* crm_base_url = BaseConfig.CRM_BASE_URL
* api_base_url = BaseConfig.API_BASE_URL
* file_svc_url = BaseConfig.FILE_SERVICE_HOST
* balance_svc_url = BaseConfig.BALANCE_SERVICE_IP

- Build file setup.py.

* To check if build success run command:
* $ python setup.py install --root=build --install-purelib=INFO --install-data=data --record=install.log --force

- Setup configuration stores in setup.sfg that actually contains definitions for Pytest.


TROUBLESHOOTING
---------------

Docker:
-------
1 Remove containers: 
* $ docker container prune -f

2 Remove images: 
* $ docker image prune -a -f

3 Build image: 
* $ docker build . --rm -f "Dockerfile" -t [project_name]:latest 

4 Get Docker logs:
* $ docker info

5 Get list of used IP's:
* $ docker network ls

6 Inspect Docker connection:
* $ docker network inspect <contiv-srv-net>

7 Log In to GitLab Registry:
* $ docker login registry.gitlab.com

* Remove by ID:
$ docker network rm

* Docker processes:
$ docker ps

* Docker run container:
$ docker exec -it #containername# bash

* Logs dir:
$ cd /usr/local/zend/var/log

* View logs:
$ tail -f | grep *.log

* Kill all UDP connections (Docker included):
$ lsof -P | grep 'UDP' | awk '{print $2}' | xargs kill -9 

Kafka:
------
1 Installation guide:

https://kafka.apache.org/quickstart
-------------------------------------
https://medium.com/@shaaslam/installing-apache-kafka-on-windows-495f6f2fd3c8
----------------------------------------------------------------------------

2 Running Apache Kafka:
* $ .\bin\windows\kafka-server-start.bat .\config\server.properties

3 Start a producer:
* $ kafka-console-producer.bat — broker-list localhost:9092 — topic sql-insert

Solving Network conflict:
-------------------------
* If your docker build fails such as:
"ERROR: cannot create network",
(br-c868a505e7d9): "conflicts with network",
(br-992ca1654879): "networks have overlapping IPv4"

* Look on docker network processes:
$ docker network ls

* Find from returned list conflicted ID:
NETWORK ID          NAME                        DRIVER              SCOPE
10060c77e51a        bridge                      bridge              local
992ca1654879        crm_bo-master_crm-network   bridge              local
82c2f8dcfa10        host                        host                local
64d5c2636300        none                        null                local

* Remove by ID:
$ docker network rm

Solving DB conflict (site not responding):
------------------------------------------
* Docker processes:
$ docker ps

* Docker run container:
$ docker exec -it #containername# bash

* Logs dir:
$ cd /usr/local/zend/var/log

* View logs:
$ tail -f | grep *.log

* Inspect DB network:
$ telnet hostname 3306

Git Configuration:
------------------
* $ git init

* $ git status

* $ git config --global --list

* $ git config --global user.name ""

* $ git config --global user.email ""

* $ cat ~/.gitconfig

* $ git config --global help.autocorrect 1

* $ git config core.autorlf true/false


Python Installation:  
--------------------
https://www.python.org/downloads/windows/
-----------------------------------------

* install pip:
$ python get-pip.py

* install virtual environment:
$ pip install virtualenv

* create virtual environment:
$ virtualenv venv --python=python3.7

* activate environment for Windows:
$ venv\Scripts\activate

* activate environment for Unix:
$ source venv/bin/activate

* list all packages installed in the environment:
$ pip freeze

* upgrade pip:  
$ python -m pip install --upgrade pip

PROTOBUF
-------- 

- Download and Installation:

https://github.com/protocolbuffers/protobuf/releases/tag/v3.6.1

$ brew install libtool, automake
$ pip3 install --no-binary=protobuf protobuf
$ python3 ./setup.py build  
$ python3 ./setup.py -v install  

- Plugin:
https://github.com/dropbox/mypy-protobuf

* Generate python proto:
$ GitLab\protoc-3.6.1-win32\bin\protoc -I=GitLab\proto_contracts\src --python_out=GitLab\proto_contracts\gen   

* Generate mypy proto (with autocomplete and keywords):
$ protoc -I=. --mypy_out=../mypy_out --python_out=../python_out LocationServiceResponse.proto   

Protobuf installation:
pip install --no-binary=protobuf protobuf
I guess that before it you need pip uninstall protobuf


MAINTAINERS
-----------

* Anton Shipulin <antishipul@gmail.com> 
