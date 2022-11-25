<!--
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
-->

# Contributing

pydolphinscheduler is python API for Apache DolphinScheduler, it just defines what workflow look like instead of
store or execute it. We here use [py4j][py4j] to dynamically access Java Virtual Machine.

## Setup Develop Environment

**PyDolphinScheduler** use GitHub to hold all source code, you should clone the code before you do same change.

```shell
git clone git@github.com:apache/dolphinscheduler-sdk-python.git
```

Now, we should install all dependence to make sure we could run test or check code style locally

```shell
python -m pip install -e '.[dev]'
```

Next, we have to open pydolphinscheduler project in you editor. We recommend you use [pycharm][pycharm]
instead of [IntelliJ IDEA][idea] to open it.

## Brief Concept

Apache DolphinScheduler is design to define workflow by UI, and pydolphinscheduler try to define it by code. When
define by code, user usually do not care user, tenant, or queue exists or not. All user care about is created
a new workflow according the code definition. So we have some **models object** in `pydolphinscheduler/models`
directory, their only check object exists or not, and create them if not exists.

More detail about core concept, please read [concept](https://dolphinscheduler.apache.org/python/main/concept.html)
in our documentation.

## Syntax To Trigger Specific CI During Pull Request

We use [GitHub Actions][github-actions] to run CI, and it will run automatically when you push code to GitHub.
But some CI we do not need to run them every time, or we have special rule to change our CI behavior.

* `[run-it]`: By default, we will skip all integration test in pull requests, if you want to run them, you should add this
  syntax to your Git commit message. The common reason to run integration test is you change some code related to python gateway
  service in repository [apache/dolphinscheduler](https://github.com/apache/dolphinscheduler). 

## Test Your Code

Linting and tests is very important for open source project, so we pay more attention to it. We have continuous
integration service run by GitHub Action to test whether the patch is good or not, which you could jump to
section [With GitHub Action](#with-github-action) see more detail.

And to make more convenience to local tests, we also have the way to run your [test automated with tox](#automated-testing-with-tox)
locally(*run all tests except integrate test with need docker environment*). It is helpful when your try to find out the
detail when continuous integration in GitHub Action failed, or you have a great patch and want to test local first.

Besides [automated testing with tox](#automated-testing-with-tox) locally, we also have a [manual way](#manually)
run tests. And it is scattered commands to reproduce each step of the integration test we told about.

* Remote
  * [With GitHub Action](#with-github-action)
* Local
  * [Automated Testing With tox](#automated-testing-with-tox)(including all but integrate test)
  * [Manually](#manually)(with integrate test)

### With GitHub Action

GitHub Action test in various environment for pydolphinscheduler, including different python version in
`3.6|3.7|3.8|3.9|3.10|3.11` and operating system `linux|macOS|windows`. It will trigger and run automatically when you
submit pull requests to repository `apache/dolphinscheduler-sdk-python`.

### Automated Testing With tox

[tox](https://tox.wiki) is a package aims to automate and standardize testing in Python, both our continuous
integration and local test use it to run actual task. To use it, you should install it first

```shell
python -m pip install --upgrade tox
```

After installation, you could run a single command to run all the tests, it is almost like test in GitHub Action
but not so much different environment.

```shell
tox -e local-ci
```

It will take a while when you run it the first time, because it has to install dependencies and make some prepare,
and the next time you run it will be faster.

The command `tox -e local-ci` will run all tests including code-style test, unit test, docs build test, which excepting
integrate test, because it needs to run dolphinscheduler before the test, for more detail, please read [Integrate Test](#integrate-test).

If you failed section `lint` when you run command `tox -e local-ci`, you could try to run command `tox -e auto-lint`
which we provider fix as many lints as possible. When I finish, you could run command `tox -e local-ci` to see
whether the linter pass or not, you have to fix it by yourself if linter still fail.

> NOTE: You can add `-r` or `--recreate` to recreate the virtual environment of tox, it is useful when you change
> our dependencies in `setup.py` or `tox.ini`, or some odd things happen.

### Manually

* For code style lint, see [Code Style Using pre-commit](#code-style-using-pre-commit)
* For unit test, see [Unit Test Manually](#unit-test-manually)
* For document build, see [Build Document Manually](#build-document-manually)
* For integrate test, see [Integrate Test](#integrate-test)

## Code Style

We use [isort][isort] to automatically keep Python imports alphabetically, and use [Black][black] for code
formatter and [Flake8][flake8] for pep8 checker. If you use [pycharm][pycharm]or [IntelliJ IDEA][idea],
maybe you could follow [Black-integration][black-editor] to configure them in your environment.

Our Python API CI would automatically run code style checker and unittest when you submit pull request in
GitHub, you could also run static check locally.

### Code Style Using tox

The command `tox -e auto-lint` will run code style checker and formatter, and fix as many lints as possible(some
flake8 linter can not auto fix). When it finishes, you could run command `tox -e local-ci` to see whether have
some flake8 linter still fail, you have to fix it by yourself.

### Code Style Using pre-commit

We recommend [pre-commit](https://pre-commit.com/) to do the checker mentioned above before you develop locally.
You should install `pre-commit` by running

```shell
python -m pip install pre-commit 
```

in your development environment and then run `pre-commit install` to set up the git hooks scripts. After finish
above steps, each time you run `git commit` or `git push` would run pre-commit check to make basic check before
you create pull requests in GitHub.

### Code Style Manually

If you do not want to use `tox` and `pre-commit`, you can run these lints command manually. First we should install
dependencies for lints

```shell
python -m pip install '.[style]'
```

```shell
# We recommend you run isort and Black before Flake8, because Black could auto fix some code style issue
# but Flake8 just hint when code style not match pep8

# Run Isort
python -m isort .

# Run Black
python -m black .

# Run Flake8
python -m flake8
```

## Build Document

We use [sphinx][sphinx] to build docs. Dolphinscheduler Python API CI would automatically build docs when you submit pull request in
GitHub. You may locally ensure docs could be built successfully in case the failure blocks CI, you can build by tox or manual.

### Build Document Automatically with tox

We integrated document build process into tox, you can build the latest document and all document(including history documents) via
single command

```shell
# Build the latest document in dev branch
tox -e doc-build
# Build all documents, which including the latest and all history documents
tox -e doc-build-multi
```

### Build Document Manually

You can also build docs manually instead of using tox, in this case you should install dependencies first

```shell
python -m pip install '.[doc]'
```

Then go to document directory and execute the build command

```shell
cd pydolphinscheduler/docs/
make clean && make html
```

or if you want to build history documents, you should execute the command below

```shell
# Fetch all history tags because we use tag to build history documents via [sphinx-multiversion](https://holzhaus.github.io/sphinx-multiversion/master/index.html)
git fetch --tags
cd pydolphinscheduler/docs/
make clean && make multiversion
```

## Unit Test

pydolphinscheduler using [pytest][pytest] to test our codebase. GitHub Action will run our test when you create
pull request or commit to dev branch, with python version `3.6|3.7|3.8|3.9|3.10|3.11` and operating system `linux|macOS|windows`.

### Unit Test Using tox

We integrated unit test into tox, you can run all unit tests and check the code coverage via single command

```shell
# Run unit test base on current python version
tox -e code-test
```

Besides run tests, it will also check the unit test [coverage][coverage] threshold, for now when test cover less than 90%
will fail the coverage, as well as our GitHub Action.

### Unit Test Manually

pydolphinscheduler using [pytest][pytest] to run all tests in directory `tests`. You could run tests by the commands

```shell
python -m pytest --cov=pydolphinscheduler --cov-config=.coveragerc tests/
```

The command above will check test coverage automatically, and you could also test the coverage by command.

```shell
python -m coverage run && python -m  coverage report
```

It would not only run unit test but also show each file coverage which cover rate less than 100%, and `TOTAL`
line show you total coverage of you code. If your CI failed with coverage you could go and find some reason by
this command output.

## Integrate Test

Integrate Test can not run when you execute command `tox -e local-ci` because it needs external environment
including [Docker](https://docs.docker.com/get-docker/) and specific image build by [maven](https://maven.apache.org/install.html).
Here we would show you the step to run integrate test in directory `tests/integration`. There are two ways to run integrate tests.

### Launch Docker Container Locally

```shell
# Clone apache/dolphinscheduler repository
cd <SOMEWHERE-PUT-CODE>
git clone git@github.com:apache/dolphinscheduler.git

# Build apache/dolphinscheduler-standalone-server docker image
./mvnw -B clean install \
    -Dmaven.test.skip \
    -Dmaven.javadoc.skip \
    -Dmaven.checkstyle.skip \
    -Pdocker,release -Ddocker.tag=ci \
    -pl dolphinscheduler-standalone-server -am

# Go to dolphinscheduler-sdk/python root directory and run integrate tests via tox
cd dolphinscheduler-sdk/python
tox -e integrate-test
```

### Start Standalone Server in IntelliJ IDEA

```shell
# Clone apache/dolphinscheduler repository
cd <SOMEWHERE-PUT-CODE>
git clone git@github.com:apache/dolphinscheduler.git

# Run apache/dolphinscheduler's Standalone Server in IntelliJ IDEA according to
# https://dolphinscheduler.apache.org/en-us/docs/dev/user_doc/contribute/development-environment-setup.html

# Go to dolphinscheduler-sdk/python root directory and run integrate tests via tox
tox -e local-integrate-test
```

> NOTE: You can also run integrate test via command `python -m pytest tests/integration/` or run them in Pycharm,
> after you start Standalone Server above.

## Add LICENSE When New Dependencies Adding

When you add a new package in pydolphinscheduler, you should also add the package's LICENSE to directory
`licenses`, and also add a short description to `LICENSE` file.

## Update `UPDATING.md` when public class, method or interface is being changed

When you change public class, method or interface, you should change the [UPDATING.md](./UPDATING.md) to notice
users who may use it in other way.

## Reference

[py4j]: https://www.py4j.org/index.html
[pycharm]: https://www.jetbrains.com/pycharm
[idea]: https://www.jetbrains.com/idea/
[all-task]: https://dolphinscheduler.apache.org/en-us/docs/dev/user_doc/guide/task/shell.html
[pytest]: https://docs.pytest.org/en/latest/
[black]: https://black.readthedocs.io/en/stable/index.html
[flake8]: https://flake8.pycqa.org/en/latest/index.html
[black-editor]: https://black.readthedocs.io/en/stable/integrations/editors.html#pycharm-intellij-idea
[coverage]: https://coverage.readthedocs.io/en/stable/
[isort]: https://pycqa.github.io/isort/index.html
[sphinx]: https://www.sphinx-doc.org/en/master
