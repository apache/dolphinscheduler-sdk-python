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

"""Test Task sub workflow."""

import warnings
from unittest.mock import patch

import pytest

from pydolphinscheduler.core.workflow import Workflow
from pydolphinscheduler.tasks.sub_workflow import SubWorkflow

TEST_SUB_WORKFLOW_NAME = "sub-test-workflow"
TEST_SUB_WORKFLOW_CODE = "3643589832320"
TEST_WORKFLOW_NAME = "simple-test-workflow"


@pytest.mark.parametrize(
    "attr, expect",
    [
        (
            {"workflow_name": TEST_SUB_WORKFLOW_NAME},
            {
                "workflowDefinitionCode": TEST_SUB_WORKFLOW_CODE,
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
    "pydolphinscheduler.tasks.sub_workflow.SubWorkflow.get_workflow_info",
    return_value=(
        {
            "id": 1,
            "name": TEST_SUB_WORKFLOW_NAME,
            "code": TEST_SUB_WORKFLOW_CODE,
        }
    ),
)
@patch(
    "pydolphinscheduler.core.task.Task.gen_code_and_version",
    return_value=(123, 1),
)
def test_property_task_params(mock_code_version, mock_pd_info, attr, expect):
    """Test task sub workflow property."""
    task = SubWorkflow("test-sub-workflow-task-params", **attr)
    assert expect == task.task_params


@patch(
    "pydolphinscheduler.tasks.sub_workflow.SubWorkflow.get_workflow_info",
    return_value=(
        {
            "id": 1,
            "name": TEST_SUB_WORKFLOW_NAME,
            "code": TEST_SUB_WORKFLOW_CODE,
        }
    ),
)
def test_sub_workflow_get_define(mock_workflow_definition):
    """Test task sub_workflow function get_define."""
    code = 123
    version = 1
    name = "test_sub_workflow_get_define"
    expect_task_params = {
        "resourceList": [],
        "localParams": [],
        "workflowDefinitionCode": TEST_SUB_WORKFLOW_CODE,
        "dependence": {},
        "conditionResult": {"successNode": [""], "failedNode": [""]},
        "waitStartTimeout": {},
    }
    with patch(
        "pydolphinscheduler.core.task.Task.gen_code_and_version",
        return_value=(code, version),
    ):
        with Workflow(TEST_WORKFLOW_NAME):
            sub_workflow = SubWorkflow(name, TEST_SUB_WORKFLOW_NAME)
            assert sub_workflow.task_params == expect_task_params


@patch(
    "pydolphinscheduler.tasks.sub_workflow.SubWorkflow.get_workflow_info",
    return_value=(
        {
            "id": 1,
            "name": TEST_SUB_WORKFLOW_NAME,
            "code": TEST_SUB_WORKFLOW_CODE,
        }
    ),
)
def test_deprecated_sub_workflow_get_define(mock_workflow_definition):
    """Test deprecated task sub_process still work and raise warning."""
    code = 123
    version = 1
    name = "test_sub_workflow_get_define"
    expect_task_params = {
        "resourceList": [],
        "localParams": [],
        "workflowDefinitionCode": TEST_SUB_WORKFLOW_CODE,
        "dependence": {},
        "conditionResult": {"successNode": [""], "failedNode": [""]},
        "waitStartTimeout": {},
    }
    with patch(
        "pydolphinscheduler.core.task.Task.gen_code_and_version",
        return_value=(code, version),
    ):
        with warnings.catch_warnings(record=True) as w:
            from pydolphinscheduler.tasks.sub_process import SubProcess

            assert len(w) == 1
            assert issubclass(w[-1].category, DeprecationWarning)
            assert "deprecated" in str(w[-1].message)

            with Workflow(TEST_WORKFLOW_NAME):
                sub_workflow = SubProcess(name, TEST_SUB_WORKFLOW_NAME)
                assert sub_workflow.task_params == expect_task_params
