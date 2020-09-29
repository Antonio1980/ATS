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

* $ git pull --allow-unrelated-histories

Git Initialization:
------------------------------------------------
git init
git status
git add app.py
git add -u -except app.py  
git commit -m "Created a simple Flask app."  
git remote add origin https://gitlab.com/cx_group/qa/platform-server_qa.git
git push -u origin --all 
git push --set-upstream origin master
git remote -v  

GitLab Hash Key:
ssh-keygen -t rsa -C "coins.exchange@example.com" -b 4096

git remote show origin
git remote rename <remote_from> <remote_to>
git remote remove <remote>
git clone https://gitlab.com/cx_group/cam/crm_bo.git    
git clone git@gitlab.com:cx_group/cam/crm_bo.git
git checkout -b qa origin/qa
git checkout -b dev origin/dev
git checkout qa
git checkout dev
git merge  origin/dev
git fetch <remote>
git pull <remote>


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

BASH
----

To split large file: $ split ****-b 50m dialogues.txt

main.exe -clientId 5bd96c4ce349400016db6d37 -tokenDuration 20h

python -m pytest project/tests/tools/market_makers/market_maker.py

--trusted-host pypi.org --trusted-host files.pythonhosted.org

curl -s --user '7170fc398741927137f304e49a97d071-985b58f4-1e0d06a7' -G https://api.mailgun.net/v3/domains/YOUR_DOMAIN_NAME/credentials

java -Dwebdriver.chrome.driver=D:\GitLab\platform-server_qa\src\drivers\win\chromedriver.exe -jar "D:\GitLab\platform-server_qa\src\repository\selenium-server-standalone-3.14.0.jar"

java --Dwebdriver.chrome.driver=-jar src/selenium-server-standalone-3.14.0.jar

newman run ./testData/testFiles/CarDC.collection.json -e  ./testData/testFiles/CarDC.environment.json -r cli,json --reporter-json-export ./testData/testFiles/outputfile.json

newman run RegistrationWithCustomEmail.postman_collection.json -e DX.postman_environment.json -r cli,html --reporter-html-export ./reports/output.html

newman run SignUpPreconditions.postman_collection.json -e DX.postman_environment.json -r cli,html --reporter-html-export ./reports/output.html     

newman run SignUpPreconditions.postman_collection.json -e DX.postman_environment.json -d /nodeJS/lib/currentUrl.csv -r cli,html --reporter-html-export ./reports/output.html

newman run SignUpPreconditions.postman_collection.json -e DX.postman_environment.json -g globals.postman_globals.json -r cli,html --reporter-html-export ./reports/output.html

newman run RegistrationWithCustomEmail.postman_collection.json --delay-request 30000 -e DX.postman_environment.json -r cli,html --reporter-html-export ./reports/output.html 

ps -p $(lsof  tcp:3000) o comm=,pid= -> ./src/scripts/output/process_id.txt

newman run ./2FA_Test/2FA_Test.postman.collection.json -e QA.postman_environment.json -r cli,html --reporter-html-export ./report_2fa.html 

python -m pytest tests_runner.py  --alluredir=./output/reports/my_allure_resultsmy --group=e2e_tests

python -m pytest tests/web_platform_tests/api_tests/authorization_tests/sign_up/sign_up_test.py  --alluredir=src/repository/allure_results

D:\allure\allure-commandline-2.9.0\allure-2.9.0\bin\allure.bat serve D:\GitLab\platform_server_qa\src\repository\allure_results

D:\allure\allure-commandline-2.9.0\allure-2.9.0\bin\allure.bat open src/repository/allure_report

D:\allure\allure-commandline-2.9.0\allure-2.9.0\bin\allure.bat generate src/repository/allure_results -o src/repository/allure_report --clean

protoc -I=. --mypy_out=../mypy_out --python_out=../python_out ClientData.proto

rotoc -I=. --plugin=protoc-gen-mypy=../mypy-protobuf-master/python/protoc-gen-mypy --mypy_out=../mypy_out  --python_out=../python_out ClientData.proto

PYTHON
------

usage: python [option] ... [-c cmd | -m mod | file | -] [arg] ...
Options and arguments (and corresponding environment variables):
-b     : issue warnings about str(bytes_instance), str(bytearray_instance)
         and comparing bytes/bytearray with str. (-bb: issue errors)
-B     : don't write .pyc files on import; also PYTHONDONTWRITEBYTECODE=x
-c cmd : program passed in as string (terminates option list)
-d     : debug output from parser; also PYTHONDEBUG=x
-E     : ignore PYTHON* environment variables (such as PYTHONPATH)
-h     : print this help message and exit (also --help)
-i     : inspect interactively after running script; forces a prompt even
         if stdin does not appear to be a terminal; also PYTHONINSPECT=x
-I     : isolate Python from the user's environment (implies -E and -s)
-m mod : run library module as a script (terminates option list)
-O     : remove assert and __debug__-dependent statements; add .opt-1 before
         .pyc extension; also PYTHONOPTIMIZE=x
-OO    : do -O changes and also discard docstrings; add .opt-2 before
         .pyc extension
-q     : don't print version and copyright messages on interactive startup
-s     : don't add user site directory to sys.path; also PYTHONNOUSERSITE
-S     : don't imply 'import site' on initialization
-u     : force the binary I/O layers of stdout and stderr to be unbuffered;
         stdin is always buffered; text I/O layer will be line-buffered;
         also PYTHONUNBUFFERED=x
-v     : verbose (trace import statements); also PYTHONVERBOSE=x
         can be supplied multiple times to increase verbosity
-V     : print the Python version number and exit (also --version)
         when given twice, print more information about the build
-W arg : warning control; arg is action:message:category:module:lineno
         also PYTHONWARNINGS=arg
-x     : skip first line of source, allowing use of non-Unix forms of #!cmd
-X opt : set implementation-specific option
file   : program read from script file
-      : program read from stdin (default; interactive mode if a tty)
arg ...: arguments passed to program in sys.argv[1:]

Other environment variables:
PYTHONSTARTUP: file executed on interactive startup (no default)
PYTHONPATH   : ';'-separated list of directories prefixed to the
               default module search path.  The result is sys.path.
PYTHONHOME   : alternate <prefix> directory (or <prefix>;<exec_prefix>).
               The default module search path uses <prefix>\python{major}{minor}.
PYTHONCASEOK : ignore case in 'import' statements (Windows).
PYTHONIOENCODING: Encoding[:errors] used for stdin/stdout/stderr.
PYTHONFAULTHANDLER: dump the Python traceback on fatal errors.
PYTHONHASHSEED: if this variable is set to 'random', a random value is used
   to seed the hashes of str, bytes and datetime objects.  It can also be
   set to an integer in the range [0,4294967295] to get hash values with a
   predictable seed.
PYTHONMALLOC: set the Python memory allocators and/or install debug hooks
   on Python memory allocators. Use PYTHONMALLOC=debug to install debug
   hooks.

PYTEST
------

usage: pytest [options] [file_or_dir] [file_or_dir] [...]

positional arguments:
  file_or_dir

general:
  -k EXPRESSION         only run tests which match the given substring
                        expression. An expression is a python evaluatable
                        expression where all names are substring-matched
                        against test names and their parent classes. Example:
                        -k 'test_method or test_other' matches all test
                        functions and classes whose name contains
                        'test_method' or 'test_other', while -k 'not
                        test_method' matches those that don't contain
                        'test_method' in their names. Additionally keywords
                        are matched to classes and functions containing extra
                        names in their 'extra_keyword_matches' set, as well as
                        functions which have names assigned directly to them.
  -m MARKEXPR           only run tests matching given mark expression.
                        example: -m 'mark1 and not mark2'.
  --markers             show markers (builtin, plugin and per-project ones).
  -x, --exitfirst       exit instantly on first error or failed test.
  --maxfail=num         exit after first num failures or errors.
  --strict              marks not registered in configuration file raise
                        errors.
  -c file               load configuration from `file` instead of trying to
                        locate one of the implicit configuration files.
  --continue-on-collection-errors
                        Force test execution even if collection errors occur.
  --rootdir=ROOTDIR     Define root directory for tests. Can be relative path:
                        'root_dir', './root_dir', 'root_dir/another_dir/';
                        absolute path: '/home/user/root_dir'; path with
                        variables: '$HOME/root_dir'.
  --fixtures, --funcargs
                        show available fixtures, sorted by plugin appearance
                        (fixtures with leading '_' are only shown with '-v')
  --fixtures-per-test   show fixtures per test
  --import-mode={prepend,append}
                        prepend/append to sys.path when importing test
                        modules, default is to prepend.
  --pdb                 start the interactive Python debugger on errors or
                        KeyboardInterrupt.
  --pdbcls=modulename:classname
                        start a custom interactive Python debugger on errors.
                        For example:
                        --pdbcls=IPython.terminal.debugger:TerminalPdb
  --capture=method      per-test capturing method: one of fd|sys|no.
  -s                    shortcut for --capture=no.
  --runxfail            run tests even if they are marked xfail
  --lf, --last-failed   rerun only the tests that failed at the last run (or
                        all if none failed)
  --ff, --failed-first  run all tests but run the last failures first. This
                        may re-order tests and thus lead to repeated fixture
                        setup/teardown
  --nf, --new-first     run tests from new files first, then the rest of the
                        tests sorted by file mtime
  --cache-show          show cache contents, don't perform collection or tests
  --cache-clear         remove all cache contents at start of test run.
  --lfnf={all,none}, --last-failed-no-failures={all,none}
                        change the behavior when no test failed in the last
                        run or no information about the last failures was
                        found in the cache
  --allure-severities=SEVERITIES_SET
                        Comma-separated list of severity names. Tests only
                        with these severities will be run. Possible values
                        are: blocker, critical, normal, minor, trivial.
  --allure-epics=EPICS_SET
                        Comma-separated list of epic names. Run tests that
                        have at least one of the specified feature labels.
  --allure-features=FEATURES_SET
                        Comma-separated list of feature names. Run tests that
                        have at least one of the specified feature labels.
  --allure-stories=STORIES_SET
                        Comma-separated list of story names. Run tests that
                        have at least one of the specified story labels.
  --allure-link-pattern=LINK_TYPE:LINK_PATTERN
                        Url pattern for link type. Allows short links in test,
                        like 'issue-1'. Text will be formatted to full url
                        with python str.format().

reporting:
  -v, --verbose         increase verbosity.
  -q, --quiet           decrease verbosity.
  --verbosity=VERBOSE   set verbosity
  -r chars              show extra test summary info as specified by chars
                        (f)ailed, (E)error, (s)skipped, (x)failed, (X)passed,
                        (p)passed, (P)passed with output, (a)all except pP.
                        Warnings are displayed at all times except when
                        --disable-warnings is set
  --disable-warnings, --disable-pytest-warnings
                        disable warnings summary
  -l, --showlocals      show locals in tracebacks (disabled by default).
  --tb=style            traceback print mode (auto/long/short/line/native/no).
  --show-capture={no,stdout,stderr,log,all}
                        Controls how captured stdout/stderr/log is shown on
                        failed tests. Default is 'all'.
  --full-trace          don't cut any tracebacks (default is to cut).
  --color=color         color terminal output (yes/no/auto).
  --durations=N         show N slowest setup/test durations (N=0 for all).
  --pastebin=mode       send failed|all info to bpaste.net pastebin service.
  --junit-xml=path      create junit-xml style report file at given path.
  --junit-prefix=str    prepend prefix to classnames in junit-xml output
  --result-log=path     DEPRECATED path for machine-readable result log.

collection:
  --collect-only        only collect tests, don't execute them.
  --pyargs              try to interpret all arguments as python packages.
  --ignore=path         ignore path during collection (multi-allowed).
  --deselect=nodeid_prefix
                        deselect item during collection (multi-allowed).
  --confcutdir=dir      only load conftest.py's relative to specified dir.
  --noconftest          Don't load any conftest.py files.
  --keep-duplicates     Keep duplicate tests.
  --collect-in-virtualenv
                        Don't ignore tests in a local virtualenv directory
  --doctest-modules     run doctests in all .py modules
  --doctest-report={none,cdiff,ndiff,udiff,only_first_failure}
                        choose another output format for diffs on doctest
                        failure
  --doctest-glob=pat    doctests file matching pattern, default: test*.txt
  --doctest-ignore-import-errors
                        ignore doctest ImportErrors
  --doctest-continue-on-failure
                        for a given doctest, continue to run after the first
                        failure

test session debugging and configuration:
  --basetemp=dir        base temporary directory for this test run.
  --version             display pytest lib version and import information.
  -h, --help            show help message and configuration info
  -p name               early-load given plugin (multi-allowed). To avoid
                        loading of plugins, use the `no:` prefix, e.g.
                        `no:doctest`.
  --trace-config        trace considerations of conftest.py files.
  --debug               store internal tracing debug information in
                        'pytestdebug.log'.
  -o OVERRIDE_INI, --override-ini=OVERRIDE_INI
                        override ini option with "option=value" style, e.g.
                        `-o xfail_strict=True -o cache_dir=cache`.
  --assert=MODE         Control assertion debugging tools. 'plain' performs no
                        assertion debugging. 'rewrite' (the default) rewrites
                        assert statements in test modules on import to provide
                        assert expression information.
  --setup-only          only setup fixtures, do not execute tests.
  --setup-show          show setup of fixtures while executing tests.
  --setup-plan          show what fixtures and tests would be executed but
                        don't execute anything.

pytest-warnings:
  -W PYTHONWARNINGS, --pythonwarnings=PYTHONWARNINGS
                        set which warnings to report, see -W option of python
                        itself.

logging:
  --no-print-logs       disable printing caught logs on failed tests.
  --log-level=LOG_LEVEL
                        logging level used by the logging module
  --log-format=LOG_FORMAT
                        log format as used by the logging module.
  --log-date-format=LOG_DATE_FORMAT
                        log date format as used by the logging module.
  --log-cli-level=LOG_CLI_LEVEL
                        cli logging level.
  --log-cli-format=LOG_CLI_FORMAT
                        log format as used by the logging module.
  --log-cli-date-format=LOG_CLI_DATE_FORMAT
                        log date format as used by the logging module.
  --log-file=LOG_FILE   path to a file when logging will be written to.
  --log-file-level=LOG_FILE_LEVEL
                        log file logging level.
  --log-file-format=LOG_FILE_FORMAT
                        log format as used by the logging module.
  --log-file-date-format=LOG_FILE_DATE_FORMAT
                        log date format as used by the logging module.

reporting:
  --alluredir=DIR       Generate Allure report in the specified directory (may
                        not exist)
  --clean-alluredir     Clean alluredir folder if it exists
  --allure-no-capture   Do not attach pytest captured logging/stdout/stderr to
                        report


[pytest] ini-options in the first pytest.ini|tox.ini|setup.cfg file found:

  markers (linelist)       markers for test functions
  empty_parameter_set_mark (string) default marker for empty parametersets
  norecursedirs (args)     directory patterns to avoid for recursion
  testpaths (args)         directories to search for tests when no files or dire
  console_output_style (string) console output: classic or with additional progr
  usefixtures (args)       list of default fixtures to be used with this project
  python_files (args)      glob-style file patterns for Python test module disco
  python_classes (args)    prefixes or glob names for Python test class discover
  python_functions (args)  prefixes or glob names for Python test function and m
  xfail_strict (bool)      default for the strict parameter of xfail markers whe
  junit_suite_name (string) Test suite name for JUnit report
  junit_logging (string)   Write captured log messages to JUnit report: one of n
  doctest_optionflags (args) option flags for doctests
  doctest_encoding (string) encoding used for doctest files
  cache_dir (string)       cache directory path.
  filterwarnings (linelist) Each line specifies a pattern for warnings.filterwar
  log_print (bool)         default value for --no-print-logs
  log_level (string)       default value for --log-level
  log_format (string)      default value for --log-format
  log_date_format (string) default value for --log-date-format
  log_cli (bool)           enable log display during test run (also known as "li
  log_cli_level (string)   default value for --log-cli-level
  log_cli_format (string)  default value for --log-cli-format
  log_cli_date_format (string) default value for --log-cli-date-format
  log_file (string)        default value for --log-file
  log_file_level (string)  default value for --log-file-level
  log_file_format (string) default value for --log-file-format
  log_file_date_format (string) default value for --log-file-date-format
  addopts (args)           extra command line options
  minversion (string)      minimally required pytest version

environment variables:
  PYTEST_ADDOPTS           extra command line options
  PYTEST_PLUGINS           comma-separated plugins to load during startup
  PYTEST_DEBUG             set to enable debug tracing of pytest's internals


to see available markers type: pytest --markers
to see available fixtures type: pytest --fixtures
(shown according to specified file_or_dir or current dir if not specified; fixtures with leading '_' are only shown with the '-v' option

DOCKER
-------

Usage: newman [options] [command]

Options:
  -v, --version               output the version number
  -h, --help                  output usage information

Commands:
  run [options] <collection>  URL or path to a Postman Collection.

To get available options for a command:
  newman [command] -h
antons@Antons-MacBook-Pro ~ % docker --help

Usage:	docker [OPTIONS] COMMAND

A self-sufficient runtime for containers

Options:
      --config string      Location of client config files (default "/Users/antons/.docker")
  -c, --context string     Name of the context to use to connect to the daemon (overrides DOCKER_HOST env var and default context set with
                           "docker context use")
  -D, --debug              Enable debug mode
  -H, --host list          Daemon socket(s) to connect to
  -l, --log-level string   Set the logging level ("debug"|"info"|"warn"|"error"|"fatal") (default "info")
      --tls                Use TLS; implied by --tlsverify
      --tlscacert string   Trust certs signed only by this CA (default "/Users/antons/.docker/ca.pem")
      --tlscert string     Path to TLS certificate file (default "/Users/antons/.docker/cert.pem")
      --tlskey string      Path to TLS key file (default "/Users/antons/.docker/key.pem")
      --tlsverify          Use TLS and verify the remote
  -v, --version            Print version information and quit

Management Commands:
  builder     Manage builds
  config      Manage Docker configs
  container   Manage containers
  context     Manage contexts
  image       Manage images
  network     Manage networks
  node        Manage Swarm nodes
  plugin      Manage plugins
  secret      Manage Docker secrets
  service     Manage services
  stack       Manage Docker stacks
  swarm       Manage Swarm
  system      Manage Docker
  trust       Manage trust on Docker images
  volume      Manage volumes

Commands:
  attach      Attach local standard input, output, and error streams to a running container
  build       Build an image from a Dockerfile
  commit      Create a new image from a container's changes
  cp          Copy files/folders between a container and the local filesystem
  create      Create a new container
  diff        Inspect changes to files or directories on a container's filesystem
  events      Get real time events from the server
  exec        Run a command in a running container
  export      Export a container's filesystem as a tar archive
  history     Show the history of an image
  images      List images
  import      Import the contents from a tarball to create a filesystem image
  info        Display system-wide information
  inspect     Return low-level information on Docker objects
  kill        Kill one or more running containers
  load        Load an image from a tar archive or STDIN
  login       Log in to a Docker registry
  logout      Log out from a Docker registry
  logs        Fetch the logs of a container
  pause       Pause all processes within one or more containers
  port        List port mappings or a specific mapping for the container
  ps          List containers
  pull        Pull an image or a repository from a registry
  push        Push an image or a repository to a registry
  rename      Rename a container
  restart     Restart one or more containers
  rm          Remove one or more containers
  rmi         Remove one or more images
  run         Run a command in a new container
  save        Save one or more images to a tar archive (streamed to STDOUT by default)
  search      Search the Docker Hub for images
  start       Start one or more stopped containers
  stats       Display a live stream of container(s) resource usage statistics
  stop        Stop one or more running containers
  tag         Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE
  top         Display the running processes of a container
  unpause     Unpause all processes within one or more containers
  update      Update configuration of one or more containers
  version     Show the Docker version information
  wait        Block until one or more containers stop, then print their exit codes


NEWMAN
------

Usage: newman [options] [command]

Options:
  -v, --version               output the version number
  -h, --help                  output usage information

Commands:
  run [options] <collection>  URL or path to a Postman Collection.

To get available options for a command:
  newman [command] -h
  
GIT
---

usage: git [--version] [--help] [-C <path>] [-c <name>=<value>]
           [--exec-path[=<path>]] [--html-path] [--man-path] [--info-path]
           [-p | --paginate | -P | --no-pager] [--no-replace-objects] [--bare]
           [--git-dir=<path>] [--work-tree=<path>] [--namespace=<name>]
           <command> [<args>]

These are common Git commands used in various situations:

start a working area (see also: git help tutorial)
   clone      Clone a repository into a new directory
   init       Create an empty Git repository or reinitialize an existing one

work on the current change (see also: git help everyday)
   add        Add file contents to the index
   mv         Move or rename a file, a directory, or a symlink
   reset      Reset current HEAD to the specified state
   rm         Remove files from the working tree and from the index

examine the history and state (see also: git help revisions)
   bisect     Use binary search to find the commit that introduced a bug
   grep       Print lines matching a pattern
   log        Show commit logs
   show       Show various types of objects
   status     Show the working tree status

grow, mark and tweak your common history
   branch     List, create, or delete branches
   checkout   Switch branches or restore working tree files
   commit     Record changes to the repository
   diff       Show changes between commits, commit and working tree, etc
   merge      Join two or more development histories together
   rebase     Reapply commits on top of another base tip
   tag        Create, list, delete or verify a tag object signed with GPG

collaborate (see also: git help workflows)
   fetch      Download objects and refs from another repository
   pull       Fetch from and integrate with another repository or a local branch
   push       Update remote refs along with associated objects
   
JIRA
----

*Issue:*

*Reproducibility:*

*Preconditions:*

*STR:*

*Expected Result:*

*Actual Result:*

*Note:*