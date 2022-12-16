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

# Release

**PyDolphinScheduler** office release is in [ASF Distribution Directory](https://downloads.apache.org/dolphinscheduler/),
and it should be released together with [apache-dolphinscheduler](https://github.com/apache/dolphinscheduler).

<!--
## To ASF Distribution Directory

You could release to [ASF Distribution Directory](https://downloads.apache.org/dolphinscheduler/) according to
[release guide](../../docs/docs/en/contribute/release/release-prepare.md) in DolphinScheduler
website.
-->

## Create Tag

We should create a tag and push it to GitHub for each release, You could create a tag by:

```shell
export TAG=<YOUR-VERSION>  # setting your version here, like 1.0.1 or others
export REMOTE=<YOUR-REMOTE-NAME>  # setting your remote name here, like origin or upstream
git tag -a "${TAG}" -m "Release v${TAG}"
git push "${REMOTE}" --tags
```

## Release to Apache Distribution



## Release to PyPi

[PyPI](https://pypi.org), Python Package Index, is a repository of software for the Python programming language.

### Install or Upgrade package

We use [build](https://pypi.org/project/build/) to build package, and [twine](https://pypi.org/project/twine/) to
upload package to PyPi. You could first install and upgrade them by:

```bash
python3 -m pip install --upgrade pip build twine
```

It is highly recommended [releasing package to TestPyPi](#release-to-testpypi) first, to check whether the
package is correct, and then [release to PyPi](#release-to-pypi).

### Release to TestPyPi

TestPyPi is a test environment of PyPi, you could release to it to test whether the package is work or not.

1. Create an account in [TestPyPi](https://test.pypi.org/account/register/).
2. Clean unrelated files in `dist` directory, and build package `python3 setup.py pre_clean`.
3. Build package `python3 -m build`, and you will see two new files in `dist` directory, with extension
   `.tar.gz` and `.whl`.
4. Upload to TestPyPi `python3 -m twine upload --repository testpypi dist/*`.
5. Check the package in [TestPyPi](https://test.pypi.org/project/apache-dolphinscheduler/) and install it
   by `python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps apache-dolphinscheduler` to
   test whether it is work or not.

### Release to PyPi

PyPi is the official repository of Python packages, it is highly recommended [releasing package to TestPyPi](#release-to-testpypi)
first to test whether the package is correct.

1. Create an account in [PyPI](https://pypi.org/account/register/).
2. Clean unrelated files in `dist` directory, and build package `python3 setup.py pre_clean`.
3. Build package `python3 -m build`, and you will see two new files in `dist` directory, with extension
   `.tar.gz` and `.whl`.
4. Upload to TestPyPi `python3 -m twine upload dist/*`.
5. Check the package in [PyPi](https://pypi.org/project/apache-dolphinscheduler/) and install it
   by `python3 -m pip install apache-dolphinscheduler` to install it.
