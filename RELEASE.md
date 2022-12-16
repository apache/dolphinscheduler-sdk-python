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

**PyDolphinScheduler** office release is in [ASF Distribution Directory](#release-to-apache-distribution),
but we also have a [PyPi](#release-to-pypi) repository for Python package distribution for convenience.

## Prepare

* Change `version` in `setup.py`.
* Remove `sphinx-multiversion` dependency in `setup.py`, we still can not fix this issue
  [Distribute tarball and wheel error with direct dependency](https://github.com/apache/dolphinscheduler/issues/12238)
* Run all test locally, `tox -e local-ci && tox -e local-integrate-test`, after you start dolphinscheduler to
  pass `local-integrate-test`

## Build and Sign Package

We use [build](https://pypi.org/project/build/) to build package, and [twine](https://pypi.org/project/twine/) to
upload package to PyPi. You could first install and upgrade them by:

```shell
# Install or upgrade dependencies
python3 -m pip install --upgrade pip build twine

# Add Tag
VERSION=<VERSION>  # The version of the package you want to release, e.g. 1.2.3
REMOTE=<REMOTE>  # The git remote name, we usually use `origin` or `remote`
git tag -a "${VERSION}" -m "Release v${VERSION}"
git push "${REMOTE}" --tags

# Build
python setup.py pre_clean && python -m build

# Sign
cd dist
gpg --batch --yes --armor --detach-sig apache-dolphinscheduler-"${VERSION}".tar.gz
gpg --batch --yes --armor --detach-sig apache_dolphinscheduler-"${VERSION}"-py3-none-any.whl
shasum -a 512 apache-dolphinscheduler-"${VERSION}".tar.gz > apache-dolphinscheduler-"${VERSION}".tar.gz.sha512
shasum -a 512 apache_dolphinscheduler-"${VERSION}"-py3-none-any.whl > apache_dolphinscheduler-"${VERSION}"-py3-none-any.whl.sha512
```

## Release to Apache Distribution

### To Apache SVN

```shell
svn co https://dist.apache.org/repos/dist/dev/dolphinscheduler/ release/dolphinscheduler
mkdir -p release/dolphinscheduler/python/"${VERSION}"
cp apache*dolphinscheduler-"${VERSION}"* release/dolphinscheduler/python/"${VERSION}"

cd release/dolphinscheduler && svn add python && svn commit python -m "Release Apache DolphinScheduler-SDK-Python version ${VERSION}"
```

### Vote Mail

```text
TITLE: [VOTE] Release Apache DolphinScheduler SDK Python <VERSION>

BODY:

Hello DolphinScheduler Community,

This is a call for vote to release Apache DolphinScheduler SDK Python version <VERSION>

Release notes: https://github.com/apache/dolphinscheduler-sdk-python/releases/tag/<VERSION>

The release candidates: https://dist.apache.org/repos/dist/dev/dolphinscheduler/python/<VERSION>/

Git tag for the release: https://github.com/apache/dolphinscheduler-sdk-python/tree/<VERSION>

Release Commit ID: https://github.com/apache/dolphinscheduler-sdk-python/commit/02bc4f44cdd136622e403506f6474da0c7fa36fb

Keys to verify the Release Candidate: https://dist.apache.org/repos/dist/dev/dolphinscheduler/KEYS

The vote will be open for at least 72 hours or until necessary number of votes are reached.

Please vote accordingly:

[ ] +1 approve
[ ] +0 no opinion
[ ] -1 disapprove with the reason

Checklist for reference:

[ ] Download links are valid.
[ ] Checksums and PGP signatures are valid.
[ ] Source code artifacts have correct names matching the current release.
[ ] LICENSE and NOTICE files are correct for each DolphinScheduler repo.
[ ] All files have license headers if necessary.
[ ] No compiled archives bundled in source archive.
```

## Release to PyPi

[PyPI](https://pypi.org), Python Package Index, is a repository of software for the Python programming language.

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
