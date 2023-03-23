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

"""Test workflow."""
import warnings
from datetime import datetime
from typing import Any, List
from unittest.mock import patch

import pytest
from freezegun import freeze_time

from pydolphinscheduler import configuration
from pydolphinscheduler.core.resource import Resource
from pydolphinscheduler.core.workflow import Workflow
from pydolphinscheduler.exceptions import PyDSParamException
from pydolphinscheduler.models import Project, User
from pydolphinscheduler.tasks.switch import Branch, Default, Switch, SwitchCondition
from pydolphinscheduler.utils.date import conv_to_schedule
from tests.testing.task import Task

TEST_WORKFLOW_NAME = "simple-test-workflow"
TEST_TASK_TYPE = "test-task-type"


@pytest.mark.parametrize("func", ["run", "submit", "start"])
def test_workflow_key_attr(func):
    """Test workflow have specific functions or attributes."""
    with Workflow(TEST_WORKFLOW_NAME) as workflow:
        assert hasattr(
            workflow, func
        ), f"Workflow instance don't have attribute `{func}`"


@pytest.mark.parametrize(
    "name,value",
    [
        ("timezone", configuration.WORKFLOW_TIME_ZONE),
        ("project", Project(configuration.WORKFLOW_PROJECT)),
        (
            "user",
            User(
                configuration.USER_NAME,
                configuration.USER_PASSWORD,
                configuration.USER_EMAIL,
                configuration.USER_PHONE,
                configuration.USER_TENANT,
                configuration.WORKFLOW_QUEUE,
                configuration.USER_STATE,
            ),
        ),
        ("worker_group", configuration.WORKFLOW_WORKER_GROUP),
        ("warning_type", configuration.WORKFLOW_WARNING_TYPE),
        ("warning_group_id", 0),
        ("execution_type", configuration.WORKFLOW_EXECUTION_TYPE.upper()),
        ("release_state", 1),
    ],
)
def test_workflow_default_value(name, value):
    """Test workflow default attributes."""
    with Workflow(TEST_WORKFLOW_NAME) as workflow:
        assert getattr(workflow, name) == value, (
            f"Workflow instance attribute `{name}` not with "
            f"except default value `{getattr(workflow, name)}`"
        )


@pytest.mark.parametrize(
    "name,cls,expect",
    [
        ("name", str, "name"),
        ("description", str, "description"),
        ("schedule", str, "schedule"),
        ("timezone", str, "timezone"),
        ("worker_group", str, "worker_group"),
        ("warning_type", str, "FAILURE"),
        ("warning_group_id", int, 1),
        ("execution_type", str, "PARALLEL"),
        ("timeout", int, 1),
        ("param", dict, {"key": "value"}),
        (
            "resource_list",
            List,
            [Resource(name="/dev/test.py", content="hello world", description="desc")],
        ),
    ],
)
def test_set_attr(name, cls, expect):
    """Test workflow set attributes which get with same type."""
    with Workflow(TEST_WORKFLOW_NAME) as workflow:
        setattr(workflow, name, expect)
        assert (
            getattr(workflow, name) == expect
        ), f"Workflow set attribute `{name}` do not work expect"


@pytest.mark.parametrize(
    "value,expect",
    [
        ("online", 1),
        ("offline", 0),
    ],
)
def test_set_release_state(value, expect):
    """Test workflow set release_state attributes."""
    with Workflow(TEST_WORKFLOW_NAME, release_state=value) as workflow:
        assert (
            getattr(workflow, "release_state") == expect
        ), "Workflow set attribute release_state do not return expect value."


@pytest.mark.parametrize(
    "value",
    [
        "oneline",
        "offeline",
        1,
        0,
        None,
    ],
)
def test_set_release_state_error(value):
    """Test workflow set release_state attributes with error."""
    workflow = Workflow(TEST_WORKFLOW_NAME, release_state=value)
    with pytest.raises(
        PyDSParamException,
        match="Parameter release_state only support `online` or `offline` but get.*",
    ):
        workflow.release_state


@pytest.mark.parametrize(
    "set_attr,set_val,get_attr,get_val",
    [
        ("_project", "project", "project", Project("project")),
        ("_start_time", "2021-01-01", "start_time", datetime(2021, 1, 1)),
        ("_end_time", "2021-01-01", "end_time", datetime(2021, 1, 1)),
    ],
)
def test_set_attr_return_special_object(set_attr, set_val, get_attr, get_val):
    """Test workflow set attributes which get with different type."""
    with Workflow(TEST_WORKFLOW_NAME) as workflow:
        setattr(workflow, set_attr, set_val)
        assert get_val == getattr(
            workflow, get_attr
        ), f"Set attribute {set_attr} can not get back with {get_val}."


@pytest.mark.parametrize(
    "val,expect",
    [
        (datetime(2021, 1, 1), datetime(2021, 1, 1)),
        (None, None),
        ("2021-01-01", datetime(2021, 1, 1)),
        ("2021-01-01 01:01:01", datetime(2021, 1, 1, 1, 1, 1)),
    ],
)
def test__parse_datetime(val, expect):
    """Test workflow function _parse_datetime.

    Only two datetime test cases here because we have more test cases in tests/utils/test_date.py file.
    """
    with Workflow(TEST_WORKFLOW_NAME) as workflow:
        assert expect == workflow._parse_datetime(
            val
        ), f"Function _parse_datetime with unexpect value by {val}."


@pytest.mark.parametrize(
    "val",
    [
        20210101,
        (2021, 1, 1),
        {"year": "2021", "month": "1", "day": 1},
    ],
)
def test__parse_datetime_not_support_type(val: Any):
    """Test workflow function _parse_datetime not support type error."""
    with Workflow(TEST_WORKFLOW_NAME) as workflow:
        with pytest.raises(PyDSParamException, match="Do not support value type.*?"):
            workflow._parse_datetime(val)


@pytest.mark.parametrize(
    "val",
    [
        "ALLL",
        "nonee",
    ],
)
def test_warn_type_not_support_type(val: str):
    """Test workflow param warning_type not support type error."""
    with pytest.raises(
        PyDSParamException, match="Parameter `warning_type` with unexpect value.*?"
    ):
        Workflow(TEST_WORKFLOW_NAME, warning_type=val)


@pytest.mark.parametrize(
    "val",
    [
        "ALLL",
        "",
        None,
    ],
)
def test_execute_type_not_support_type(val: str):
    """Test workflow param execute_type not support type error."""
    with pytest.raises(
        PyDSParamException, match="Parameter `execution_type` with unexpect value.*?"
    ):
        Workflow(TEST_WORKFLOW_NAME, execution_type=val)


@pytest.mark.parametrize(
    "param, expect",
    [
        (
            None,
            [],
        ),
        (
            {},
            [],
        ),
        (
            {"key1": "val1"},
            [
                {
                    "prop": "key1",
                    "direct": "IN",
                    "type": "VARCHAR",
                    "value": "val1",
                }
            ],
        ),
        (
            {
                "key1": "val1",
                "key2": "val2",
            },
            [
                {
                    "prop": "key1",
                    "direct": "IN",
                    "type": "VARCHAR",
                    "value": "val1",
                },
                {
                    "prop": "key2",
                    "direct": "IN",
                    "type": "VARCHAR",
                    "value": "val2",
                },
            ],
        ),
    ],
)
def test_property_param_json(param, expect):
    """Test Workflow's property param_json."""
    workflow = Workflow(TEST_WORKFLOW_NAME, param=param)
    assert workflow.param_json == expect


@patch(
    "pydolphinscheduler.core.task.Task.gen_code_and_version",
    return_value=(123, 1),
)
def test__pre_submit_check_switch_without_param(mock_code_version):
    """Test :func:`_pre_submit_check` if workflow with switch but without attribute param."""
    with Workflow(TEST_WORKFLOW_NAME) as workflow:
        parent = Task(name="parent", task_type=TEST_TASK_TYPE)
        switch_child_1 = Task(name="switch_child_1", task_type=TEST_TASK_TYPE)
        switch_child_2 = Task(name="switch_child_2", task_type=TEST_TASK_TYPE)
        switch_condition = SwitchCondition(
            Branch(condition="${var} > 1", task=switch_child_1),
            Default(task=switch_child_2),
        )

        switch = Switch(name="switch", condition=switch_condition)
        parent >> switch
        with pytest.raises(
            PyDSParamException,
            match="Parameter param or at least one local_param of task must "
            "be provider if task Switch in workflow.",
        ):
            workflow._pre_submit_check()


@patch(
    "pydolphinscheduler.core.task.Task.gen_code_and_version",
    return_value=(123, 1),
)
def test__pre_submit_check_switch_with_local_params(mock_code_version):
    """Test :func:`_pre_submit_check` if workflow with switch with local params of task."""
    with Workflow(TEST_WORKFLOW_NAME) as workflow:
        parent = Task(
            name="parent",
            task_type=TEST_TASK_TYPE,
            local_params=[
                {"prop": "var", "direct": "OUT", "type": "VARCHAR", "value": ""}
            ],
        )
        switch_child_1 = Task(name="switch_child_1", task_type=TEST_TASK_TYPE)
        switch_child_2 = Task(name="switch_child_2", task_type=TEST_TASK_TYPE)
        switch_condition = SwitchCondition(
            Branch(condition="${var} > 1", task=switch_child_1),
            Default(task=switch_child_2),
        )

        switch = Switch(name="switch", condition=switch_condition)
        parent >> switch
        workflow._pre_submit_check()


def test_workflow_get_define_without_task():
    """Test workflow function get_define without task."""
    expect = {
        "name": TEST_WORKFLOW_NAME,
        "description": None,
        "project": configuration.WORKFLOW_PROJECT,
        "workerGroup": configuration.WORKFLOW_WORKER_GROUP,
        "warningType": configuration.WORKFLOW_WARNING_TYPE,
        "warningGroupId": 0,
        "executionType": "PARALLEL",
        "timeout": 0,
        "releaseState": 1,
        "param": None,
        "tasks": {},
        "taskDefinitionJson": [{}],
        "taskRelationJson": [{}],
        "resourceList": [],
    }
    with Workflow(TEST_WORKFLOW_NAME) as workflow:
        assert workflow.get_define() == expect


def test_workflow_simple_context_manager():
    """Test simple create workflow in workflow context manager mode."""
    expect_tasks_num = 5
    with Workflow(TEST_WORKFLOW_NAME) as workflow:
        for i in range(expect_tasks_num):
            curr_task = Task(name=f"task-{i}", task_type=f"type-{i}")
            # Set deps task i as i-1 parent
            if i > 0:
                pre_task = workflow.get_one_task_by_name(f"task-{i - 1}")
                curr_task.set_upstream(pre_task)
        assert len(workflow.tasks) == expect_tasks_num

        # Test if task workflow same as origin one
        task: Task = workflow.get_one_task_by_name("task-0")
        assert workflow is task.workflow

        # Test if all tasks with expect deps
        for i in range(expect_tasks_num):
            task: Task = workflow.get_one_task_by_name(f"task-{i}")
            if i == 0:
                assert task._upstream_task_codes == set()
                assert task._downstream_task_codes == {
                    workflow.get_one_task_by_name("task-1").code
                }
            elif i == expect_tasks_num - 1:
                assert task._upstream_task_codes == {
                    workflow.get_one_task_by_name(f"task-{i - 1}").code
                }
                assert task._downstream_task_codes == set()
            else:
                assert task._upstream_task_codes == {
                    workflow.get_one_task_by_name(f"task-{i - 1}").code
                }
                assert task._downstream_task_codes == {
                    workflow.get_one_task_by_name(f"task-{i + 1}").code
                }


def test_deprecated_workflow_simple_context_manager():
    """Test deprecated class ProcessDefinition still work and will raise warning."""
    expect_tasks_num = 5

    with warnings.catch_warnings(record=True) as w:
        from pydolphinscheduler.core.process_definition import ProcessDefinition

        assert len(w) == 1
        assert issubclass(w[-1].category, DeprecationWarning)
        assert "deprecated" in str(w[-1].message)

        with ProcessDefinition(TEST_WORKFLOW_NAME) as workflow:
            for i in range(expect_tasks_num):
                curr_task = Task(name=f"task-{i}", task_type=f"type-{i}")
                # Set deps task i as i-1 parent
                if i > 0:
                    pre_task = workflow.get_one_task_by_name(f"task-{i - 1}")
                    curr_task.set_upstream(pre_task)
            assert len(workflow.tasks) == expect_tasks_num

            # Test if task workflow same as origin one
            task: Task = workflow.get_one_task_by_name("task-0")
            assert workflow is task.workflow

            # Test if all tasks with expect deps
            for i in range(expect_tasks_num):
                task: Task = workflow.get_one_task_by_name(f"task-{i}")
                if i == 0:
                    assert task._upstream_task_codes == set()
                    assert task._downstream_task_codes == {
                        workflow.get_one_task_by_name("task-1").code
                    }
                elif i == expect_tasks_num - 1:
                    assert task._upstream_task_codes == {
                        workflow.get_one_task_by_name(f"task-{i - 1}").code
                    }
                    assert task._downstream_task_codes == set()
                else:
                    assert task._upstream_task_codes == {
                        workflow.get_one_task_by_name(f"task-{i - 1}").code
                    }
                    assert task._downstream_task_codes == {
                        workflow.get_one_task_by_name(f"task-{i + 1}").code
                    }


def test_workflow_simple_separate():
    """Test workflow simple create workflow in separate mode.

    This test just test basic information, cause most of test case is duplicate to
    test_workflow_simple_context_manager.
    """
    expect_tasks_num = 5
    workflow = Workflow(TEST_WORKFLOW_NAME)
    for i in range(expect_tasks_num):
        curr_task = Task(
            name=f"task-{i}",
            task_type=f"type-{i}",
            workflow=workflow,
        )
        # Set deps task i as i-1 parent
        if i > 0:
            pre_task = workflow.get_one_task_by_name(f"task-{i - 1}")
            curr_task.set_upstream(pre_task)
    assert len(workflow.tasks) == expect_tasks_num
    assert all(["task-" in task.name for task in workflow.task_list])


def test_schedule_json_none_schedule():
    """Test function schedule_json with None as schedule."""
    with Workflow(
        TEST_WORKFLOW_NAME,
        schedule=None,
    ) as workflow:
        assert workflow.schedule_json is None


# We freeze time here, because we test start_time with None, and if will get datetime.datetime.now. If we do
# not freeze time, it will cause flaky test here.
@freeze_time("2021-01-01")
@pytest.mark.parametrize(
    "start_time,end_time,expect_date",
    [
        (
            "20210101",
            "20210201",
            {"start_time": "2021-01-01 00:00:00", "end_time": "2021-02-01 00:00:00"},
        ),
        (
            "2021-01-01",
            "2021-02-01",
            {"start_time": "2021-01-01 00:00:00", "end_time": "2021-02-01 00:00:00"},
        ),
        (
            "2021/01/01",
            "2021/02/01",
            {"start_time": "2021-01-01 00:00:00", "end_time": "2021-02-01 00:00:00"},
        ),
        # Test mix pattern
        (
            "2021/01/01 01:01:01",
            "2021-02-02 02:02:02",
            {"start_time": "2021-01-01 01:01:01", "end_time": "2021-02-02 02:02:02"},
        ),
        (
            "2021/01/01 01:01:01",
            "20210202 020202",
            {"start_time": "2021-01-01 01:01:01", "end_time": "2021-02-02 02:02:02"},
        ),
        (
            "20210101 010101",
            "2021-02-02 02:02:02",
            {"start_time": "2021-01-01 01:01:01", "end_time": "2021-02-02 02:02:02"},
        ),
        # Test None value
        (
            "2021/01/01 01:02:03",
            None,
            {"start_time": "2021-01-01 01:02:03", "end_time": "9999-12-31 23:59:59"},
        ),
        (
            None,
            None,
            {
                "start_time": conv_to_schedule(datetime(2021, 1, 1)),
                "end_time": "9999-12-31 23:59:59",
            },
        ),
    ],
)
def test_schedule_json_start_and_end_time(start_time, end_time, expect_date):
    """Test function schedule_json about handle start_time and end_time.

    Only two datetime test cases here because we have more test cases in tests/utils/test_date.py file.
    """
    schedule = "0 0 0 * * ? *"
    expect = {
        "crontab": schedule,
        "startTime": expect_date["start_time"],
        "endTime": expect_date["end_time"],
        "timezoneId": configuration.WORKFLOW_TIME_ZONE,
    }
    with Workflow(
        TEST_WORKFLOW_NAME,
        schedule=schedule,
        start_time=start_time,
        end_time=end_time,
        timezone=configuration.WORKFLOW_TIME_ZONE,
    ) as workflow:
        assert workflow.schedule_json == expect
