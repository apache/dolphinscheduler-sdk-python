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

# PyDolphinScheduler

[![PyPi Version](https://img.shields.io/pypi/v/apache-dolphinscheduler.svg?style=flat-square&logo=PyPi)](https://pypi.org/project/apache-dolphinscheduler/)
[![PyPi Python Versions](https://img.shields.io/pypi/pyversions/apache-dolphinscheduler.svg?style=flat-square&logo=python)](https://pypi.org/project/apache-dolphinscheduler/)
[![PyPi License](https://img.shields.io/:license-Apache%202-blue.svg?style=flat-square)](https://raw.githubusercontent.com/apache/dolphinscheduler-sdk-python/main/LICENSE)
[![PyPi Status](https://img.shields.io/pypi/status/apache-dolphinscheduler.svg?style=flat-square)](https://pypi.org/project/apache-dolphinscheduler/)
[![Downloads](https://static.pepy.tech/badge/apache-dolphinscheduler/month)](https://pepy.tech/project/apache-dolphinscheduler)
![Coverage Status](https://img.shields.io/codecov/c/github/apache/dolphinscheduler-sdk-python/main.svg?style=flat-square)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat-square&labelColor=ef8336)](https://pycqa.github.io/isort)
[![CI](https://github.com/apache/dolphinscheduler-sdk-python/actions/workflows/ci.yaml/badge.svg)](https://github.com/apache/dolphinscheduler-sdk-python/actions/workflows/ci.yaml)
[![Twitter Follow](https://img.shields.io/twitter/follow/dolphinschedule.svg?style=social&label=Follow)](https://twitter.com/dolphinschedule)
[![Slack Status](https://img.shields.io/badge/slack-join_chat-white.svg?logo=slack&style=social)](https://s.apache.org/dolphinscheduler-slack)

**PyDolphinScheduler** is python API for [Apache DolphinScheduler](https://dolphinscheduler.apache.org),
which allow you definition your workflow by python code, aka workflow-as-codes.

## Quick Start

### Version Compatibility

At Nov 7, 2022 we seperated PyDolphinScheduler from DolphinScheduler, and the version of PyDolphinScheduler 4.0.0
can match multiple versions of DolphinScheduler, for more details, please refer to [version](https://dolphinscheduler.apache.org/python/main/index.html#version)

### Installation

```shell
# Install
python -m pip install apache-dolphinscheduler

# Verify installation is successful, it will show the version of apache-dolphinscheduler, here we use 0.1.0 as example
pydolphinscheduler version
# 0.1.0
```

> NOTE: package apache-dolphinscheduler not work on above Python version 3.10(including itself) in Window operating system
> due to dependence [py4j](https://pypi.org/project/py4j/) not work on those environments.

Here we show you how to install and run a simple example of PyDolphinScheduler

### Start DolphinScheduler

There are many ways to start DolphinScheduler, here we use docker to start and run it as a standalone server.

```shell
# Change the version of dolphinscheduler to the version you want to use, here we use 3.1.1 as example
DOLPHINSCHEDULER_VERSION=3.1.1
docker run --name dolphinscheduler-standalone-server -p 12345:12345 -p 25333:25333 -d apache/dolphinscheduler-standalone-server:"${DOLPHINSCHEDULER_VERSION}"
```

After the container is started, you can access the DolphinScheduler UI via http://localhost:12345/dolphinscheduler.
For more way to start DolphinScheduler and the more detail about DolphinScheduler, please refer to
[DolphinScheduler](https://dolphinscheduler.apache.org/#/en-us/docs/3.1.2/guide/start/quick-start)

### Run a simple example

We have many examples in [examples](src/pydolphinscheduler/examples) directory, we here pick up a typical one
to show how to run it.

```shell
# Get the latest code of example from github 
curl https://raw.githubusercontent.com/apache/dolphinscheduler-sdk-python/main/src/pydolphinscheduler/examples/tutorial.py -o ./tutorial.py

# Change tenant to real exists tenant in the host your DolphinScheduler running, by any editor you like 

# Run the example
python ./tutorial.py
```

> NOTICE: Since Apache DolphinScheduler's tenant is requests while running command, you have to change
> tenant value in file tutorial.py. The default value is `tenant_exists`, change it to username exists your host.

After that, a new workflow will be created by PyDolphinScheduler, and you can see it in DolphinScheduler web
UI's Project Management page. It will trigger the workflow automatically, so you can see the workflow running
in DolphinScheduler web UI's Workflow Instance page too. For more detail about any function about DolphinScheduler
Project Management, please refer to [DolphinScheduler Workflow](https://dolphinscheduler.apache.org/#/en-us/docs/3.1.2/guide/project/workflow-definition)

## Documentation

For full documentation visit [document](https://dolphinscheduler.apache.org/python/main/index.html). This
documentation is generated from this repository so please raise issues or pull requests for any additions, corrections, or clarifications.

## Contributing

If you would like to contribute, check out the [open issues on GitHub](https://github.com/apache/dolphinscheduler-sdk-python/issues).
You can also see the guide to [contributing](./CONTRIBUTING.md).

## Release

Follow the [release](./RELEASE.md) guide to release a new version of PyDolphinScheduler.
