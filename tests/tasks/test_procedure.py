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

"""Test Task Procedure."""

from unittest.mock import patch

import pytest

from pydolphinscheduler.models.datasource import TaskUsage
from pydolphinscheduler.tasks.procedure import Procedure

TEST_PROCEDURE_SQL = (
    'create procedure HelloWorld() selece "hello world"; call HelloWorld();'
)
TEST_PROCEDURE_DATASOURCE_NAME = "test_datasource"


@pytest.mark.parametrize(
    "attr, expect",
    [
        (
            {
                "name": "test-procedure-task-params",
                "datasource_name": TEST_PROCEDURE_DATASOURCE_NAME,
                "method": TEST_PROCEDURE_SQL,
            },
            {
                "method": TEST_PROCEDURE_SQL,
                "type": "MYSQL",
                "datasource": "1",
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
@patch(
    "pydolphinscheduler.models.datasource.Datasource.get_task_usage_4j",
    return_value=TaskUsage(id="1", type="MYSQL", name="test"),
)
def test_property_task_params(mock_datasource, mock_code_version, attr, expect):
    """Test task sql task property."""
    task = Procedure(**attr)
    assert expect == task.task_params


@patch(
    "pydolphinscheduler.core.task.Task.gen_code_and_version",
    return_value=(123, 1),
)
@patch(
    "pydolphinscheduler.models.datasource.Datasource.get_task_usage_4j",
    return_value=TaskUsage(id="1", type="MYSQL", name="test"),
)
def test_sql_get_define(mock_datasource, mock_code_version):
    """Test task procedure function get_define."""
    name = "test_procedure_get_define"
    expect_task_params = {
        "type": "MYSQL",
        "datasource": "1",
        "method": TEST_PROCEDURE_SQL,
        "localParams": [],
        "resourceList": [],
        "dependence": {},
        "conditionResult": {"successNode": [""], "failedNode": [""]},
        "waitStartTimeout": {},
    }
    task = Procedure(name, TEST_PROCEDURE_DATASOURCE_NAME, TEST_PROCEDURE_SQL)
    assert task.task_params == expect_task_params
