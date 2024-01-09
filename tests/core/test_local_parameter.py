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

"""Test parameter."""


import pytest

from pydolphinscheduler.core.parameter import (
    BaseDataType,
    Direction,
    ParameterHelper,
    ParameterType,
)
from pydolphinscheduler.exceptions import PyDSParamException


@pytest.mark.parametrize(
    "value, expect",
    [
        (123456, ParameterType.INTEGER),
        (0.5, ParameterType.FLOAT),
        ("abc", ParameterType.VARCHAR),
        (None, ParameterType.VARCHAR),
        (True, ParameterType.BOOLEAN),
        (False, ParameterType.BOOLEAN),
    ],
)
def test_infer_type_of_parameters(value, expect):
    """Test the infer function."""
    cls = ParameterHelper.infer_parameter_type(value)
    assert cls == expect


@pytest.mark.parametrize(
    "value",
    [list(), dict(), set()],
)
def test_infer_type_of_parameters_error(value):
    """Test the infer function error."""
    with pytest.raises(
        PyDSParamException,
        match="Can not infer parameter type",
    ):
        ParameterHelper.infer_parameter_type(value)


@pytest.mark.parametrize(
    "value, expect_type, expect_value",
    [
        (ParameterType.VARCHAR("123"), "VARCHAR", "123"),
        (ParameterType.VARCHAR(123), "VARCHAR", "123"),
        (ParameterType.VARCHAR(), "VARCHAR", ""),
        (ParameterType.LONG(123), "LONG", "123"),
        (ParameterType.LONG(), "LONG", ""),
        (ParameterType.INTEGER(123), "INTEGER", 123),
        (ParameterType.INTEGER("123"), "INTEGER", 123),
        (ParameterType.INTEGER(), "INTEGER", ""),
        (ParameterType.FLOAT(123), "FLOAT", float(123)),
        (ParameterType.FLOAT("123"), "FLOAT", float(123)),
        (ParameterType.FLOAT(), "FLOAT", ""),
        (ParameterType.DOUBLE(123), "DOUBLE", "123"),
        (ParameterType.DOUBLE(), "DOUBLE", ""),
        (ParameterType.DATE("2022-01-01"), "DATE", "2022-01-01"),
        (ParameterType.DATE(), "DATE", ""),
        (ParameterType.TIME("2022-01-01"), "TIME", "2022-01-01"),
        (ParameterType.TIME(), "TIME", ""),
        (ParameterType.TIMESTAMP(123123123), "TIMESTAMP", "123123123"),
        (ParameterType.TIMESTAMP(), "TIMESTAMP", ""),
        (ParameterType.BOOLEAN(True), "BOOLEAN", True),
        (ParameterType.BOOLEAN(), "BOOLEAN", ""),
        (ParameterType.LIST("abc"), "LIST", "abc"),
        (ParameterType.LIST(), "LIST", ""),
        (ParameterType.FILE("task1.output"), "FILE", "task1.output"),
    ],
)
def test_parameter_define(value: BaseDataType, expect_type: str, expect_value):
    """Test the parameter define."""
    assert value.data_type == expect_type
    assert value.value == expect_value


def test_convert_params():
    """Test the ParameterHelper convert_params function."""
    params = {
        "value_INTEGER": 123,
        "value_LONG": ParameterType.LONG("1000000"),
    }
    results = ParameterHelper.convert_params(params, direction=Direction.IN)
    expect = [
        {"prop": "value_INTEGER", "direct": "IN", "type": "INTEGER", "value": 123},
        {"prop": "value_LONG", "direct": "IN", "type": "LONG", "value": "1000000"},
    ]
    assert results == expect

    results = ParameterHelper.convert_params(params, direction=Direction.OUT)
    expect = [
        {"prop": "value_INTEGER", "direct": "OUT", "type": "INTEGER", "value": 123},
        {"prop": "value_LONG", "direct": "OUT", "type": "LONG", "value": "1000000"},
    ]

    assert results == expect


def test_convert_params_error_type():
    """Test the ParameterHelper convert_params with wrong type raise error."""
    params = [
        {"prop": "value_INTEGER", "direct": "IN", "type": "INTEGER", "value": 123},
        {"prop": "value_LONG", "direct": "IN", "type": "LONG", "value": "1000000"},
    ]
    with pytest.raises(
        PyDSParamException,
        match="Parameter `params` must be a dict, but get",
    ):
        ParameterHelper.convert_params(params, direction=Direction.IN)
