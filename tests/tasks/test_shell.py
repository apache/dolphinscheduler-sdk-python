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

"""Test Task shell."""

from pathlib import Path
from unittest.mock import patch

import pytest

from pydolphinscheduler.resources_plugin import Local
from pydolphinscheduler.tasks.shell import Shell
from pydolphinscheduler.utils import file
from tests.testing.file import delete_file

file_name = "local_res.sh"
file_content = 'echo "test res_local"'
res_plugin_prefix = Path(__file__).parent
file_path = res_plugin_prefix.joinpath(file_name)


@pytest.fixture
def setup_crt_first():
    """Set up and teardown about create file first and then delete it."""
    file.write(content=file_content, to_path=file_path)
    yield
    delete_file(file_path)


@pytest.mark.parametrize(
    "attr, expect",
    [
        (
            {"command": "test script"},
            {
                "rawScript": "test script",
                "localParams": [],
                "resourceList": [],
                "dependence": {},
                "waitStartTimeout": {},
                "conditionResult": {"successNode": [""], "failedNode": [""]},
            },
        )
    ],
)
@patch(
    "pydolphinscheduler.core.task.Task.gen_code_and_version",
    return_value=(123, 1),
)
def test_property_task_params(mock_code_version, attr, expect):
    """Test task shell task property."""
    task = Shell("test-shell-task-params", **attr)
    assert expect == task.task_params


def test_shell_get_define():
    """Test task shell function get_define."""
    code = 123
    version = 1
    name = "test_shell_get_define"
    command = "echo test shell"
    expect_task_params = {
        "resourceList": [],
        "localParams": [],
        "rawScript": command,
        "dependence": {},
        "conditionResult": {"successNode": [""], "failedNode": [""]},
        "waitStartTimeout": {},
    }
    with patch(
        "pydolphinscheduler.core.task.Task.gen_code_and_version",
        return_value=(code, version),
    ):
        shell = Shell(name, command)
        assert shell.task_params == expect_task_params


@pytest.mark.parametrize(
    "attr, expect",
    [
        (
            {
                "name": "test-local-res-command-content",
                "command": file_name,
                "resource_plugin": Local(str(res_plugin_prefix)),
            },
            file_content,
        )
    ],
)
@patch(
    "pydolphinscheduler.core.task.Task.gen_code_and_version",
    return_value=(123, 1),
)
def test_resources_local_shell_command_content(
    mock_code_version, attr, expect, setup_crt_first
):
    """Test task shell task command content through the local resource plug-in."""
    task = Shell(**attr)
    assert expect == getattr(task, "raw_script")


@pytest.mark.parametrize(
    "resource_limit",
    [
        {"cpu_quota": 1, "memory_max": 10},
        {"memory_max": 15},
        {},
    ],
)
def test_shell_get_define_cpu_and_memory(resource_limit):
    """Test task shell function get_define with resource limit."""
    code = 123
    version = 1
    name = "test_shell_get_define_cpu_and_memory"
    command = "echo test shell with resource limit"

    with patch(
        "pydolphinscheduler.core.task.Task.gen_code_and_version",
        return_value=(code, version),
    ):
        shell = Shell(name, command, **resource_limit)
        assert "cpuQuota" in shell.get_define()
        assert "memoryMax" in shell.get_define()

        if "cpuQuota" in resource_limit:
            assert shell.get_define()["cpuQuota"] == resource_limit.get("cpu_quota")

        if "memoryMax" in resource_limit:
            assert shell.get_define()["memoryMax"] == resource_limit.get("memory_max")
