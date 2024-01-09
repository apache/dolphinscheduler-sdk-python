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

"""Test Task HTTP."""

import warnings
from unittest.mock import patch

import pytest

from pydolphinscheduler.exceptions import PyDSParamException
from pydolphinscheduler.tasks.http import Http, HttpCheckCondition, HttpMethod


@pytest.mark.parametrize(
    "class_name, attrs",
    [
        (HttpMethod, ("GET", "POST", "HEAD", "PUT", "DELETE")),
        (
            HttpCheckCondition,
            (
                "STATUS_CODE_DEFAULT",
                "STATUS_CODE_CUSTOM",
                "BODY_CONTAINS",
                "BODY_NOT_CONTAINS",
            ),
        ),
    ],
)
def test_attr_exists(class_name, attrs):
    """Test weather class HttpMethod and HttpCheckCondition contain specific attribute."""
    assert all(hasattr(class_name, attr) for attr in attrs)


@pytest.mark.parametrize(
    "attr, expect",
    [
        (
            {"url": "https://www.apache.org"},
            {
                "url": "https://www.apache.org",
                "httpMethod": "GET",
                "httpParams": [],
                "httpCheckCondition": "STATUS_CODE_DEFAULT",
                "condition": None,
                "connectTimeout": 60000,
                "socketTimeout": 60000,
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
    """Test task http property."""
    task = Http("test-http-task-params", **attr)
    assert expect == task.task_params


@pytest.mark.parametrize(
    "param",
    [
        {"http_method": "http_method"},
        {"http_check_condition": "http_check_condition"},
        {"http_check_condition": HttpCheckCondition.STATUS_CODE_CUSTOM},
        {
            "http_check_condition": HttpCheckCondition.STATUS_CODE_CUSTOM,
            "condition": None,
        },
    ],
)
@patch(
    "pydolphinscheduler.core.task.Task.gen_code_and_version",
    return_value=(123, 1),
)
def test_http_task_param_not_support_param(mock_code, param):
    """Test HttpTaskParams not support parameter."""
    url = "https://www.apache.org"
    with pytest.raises(PyDSParamException, match="Parameter .*?"):
        Http("test-no-supprot-param", url, **param)


def test_http_get_define():
    """Test task HTTP function get_define."""
    code = 123
    version = 1
    name = "test_http_get_define"
    url = "https://www.apache.org"
    expect_task_params = {
        "localParams": [],
        "httpParams": [],
        "url": url,
        "httpMethod": "GET",
        "httpCheckCondition": "STATUS_CODE_DEFAULT",
        "condition": None,
        "connectTimeout": 60000,
        "socketTimeout": 60000,
        "dependence": {},
        "resourceList": [],
        "conditionResult": {"successNode": [""], "failedNode": [""]},
        "waitStartTimeout": {},
    }
    with patch(
        "pydolphinscheduler.core.task.Task.gen_code_and_version",
        return_value=(code, version),
    ):
        http = Http(name, url)
        assert http.task_params == expect_task_params


@patch(
    "pydolphinscheduler.core.task.Task.gen_code_and_version",
    return_value=(123, 1),
)
def test_http_params(mock_code):
    """Test the transformation and conversion of http_params."""
    http_params_dict = {"prop1": "value1", "prop2": 135, "prop3": "value3"}

    http_instance = Http(
        name="test_http",
        url="http://www.example.com",
        http_method="GET",
        http_params=http_params_dict,
    )
    expect_transformation = [
        {"prop": "prop1", "direct": "IN", "type": "VARCHAR", "value": "value1"},
        {"prop": "prop2", "direct": "IN", "type": "INTEGER", "value": 135},
        {"prop": "prop3", "direct": "IN", "type": "VARCHAR", "value": "value3"},
    ]

    assert isinstance(http_instance.http_params, list)
    assert len(http_instance.http_params) == len(http_params_dict)
    assert http_instance.http_params == expect_transformation


def test_http_params_deprecation_warning():
    """Test deprecation warning when user passes list to http_params."""
    code = 123
    version = 1
    name = "test_http_params_deprecation_warning"
    http_params_list = [
        {"prop": "abc", "httpParametersType": "PARAMETER", "value": "def"}
    ]

    with patch(
        "pydolphinscheduler.core.task.Task.gen_code_and_version",
        return_value=(code, version),
    ):
        with warnings.catch_warnings(record=True) as w:
            Http(
                name=name,
                url="http://www.example.com",
                http_method="GET",
                http_params=http_params_list,
            )

            # Check if a deprecation warning is raised
            assert len(w) == 1
            assert issubclass(w[-1].category, DeprecationWarning)
            assert "The `http_params` parameter currently accepts a dictionary" in str(
                w[-1].message
            )
