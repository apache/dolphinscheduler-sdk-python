# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""Test utils.versions module."""

from unittest import mock

import pytest

from pydolphinscheduler.utils.versions import version_match


@pytest.mark.parametrize(
    "content, name, version, expect",
    [
        ("dolphinscheduler>=3.0.0", "dolphinscheduler", "3.0.0", True),
        ("dolphinscheduler>=3.0.0", "dolphinscheduler", "2.1.9", False),
        ("dolphinscheduler>=3.0.0", "dolphinscheduler", "3.1.0", True),
        ("dolphinscheduler~=3.0.0", "dolphinscheduler", "3.0.0", True),
        ("dolphinscheduler~=3.0.0", "dolphinscheduler", "3.0.9", True),
        ("dolphinscheduler~=3.0.0", "dolphinscheduler", "3.1.0", False),
        ("dolphinscheduler>=3.0.0, <3.1.0", "dolphinscheduler", "3.0.9", True),
        ("dolphinscheduler>=3.0.0, <3.1.0", "dolphinscheduler", "3.1.0", False),
        ("dolphinscheduler~=3.0.0, !=3.0.5", "dolphinscheduler", "3.0.9", True),
        ("dolphinscheduler~=3.0.0, !=3.0.5", "dolphinscheduler", "3.0.5", False),
    ],
)
@mock.patch("pathlib.Path.open")
def test_version_match(mock_open, content: str, name: str, version: str, expect: str):
    """Test function version_match."""
    mock_open.return_value.__enter__.return_value.read.return_value = content
    assert version_match(name, version) == expect
    assert mock_open.call_count == 1


def test_version_match_error():
    """Test function version_match error when external system name not in file ``Version.FILE_NAME``."""
    with pytest.raises(
        ValueError,
        match=".*?is not in.*",
    ):
        version_match("dolphinschedulerError", "1.0.0")
