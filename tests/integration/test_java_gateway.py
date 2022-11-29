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

"""Test pydolphinscheduler java gateway."""
import importlib
import warnings
from unittest.mock import PropertyMock, patch

import pytest
from py4j.java_gateway import GatewayParameters, JavaGateway, java_import

from pydolphinscheduler import java_gateway
from tests.testing.constants import TOKEN

gateway_parameters = GatewayParameters(auth_token=TOKEN)
gateway = JavaGateway(gateway_parameters=gateway_parameters)


@pytest.fixture(scope="module")
def class_tear_down():
    """Tear down java gateway by close it."""
    yield
    gateway.close()


def test_gateway_connect():
    """Test weather client could connect java gate way or not."""
    app = gateway.entry_point
    assert app.ping() == "PONG"


def test_jvm_simple():
    """Test use JVM build-in object and operator from java gateway."""
    smallest = gateway.jvm.java.lang.Integer.MIN_VALUE
    biggest = gateway.jvm.java.lang.Integer.MAX_VALUE
    assert smallest is not None and biggest is not None
    assert biggest > smallest


def test_python_client_java_import_single():
    """Test import single class from java gateway."""
    java_import(gateway.jvm, "org.apache.dolphinscheduler.common.utils.FileUtils")
    assert hasattr(gateway.jvm, "FileUtils")


def test_python_client_java_import_package():
    """Test import package contain multiple class from java gateway."""
    java_import(gateway.jvm, "org.apache.dolphinscheduler.common.utils.*")
    # test if jvm view have some common utils
    for util in ("FileUtils", "OSUtils", "DateUtils"):
        assert hasattr(gateway.jvm, util)


@pytest.mark.parametrize(
    "version, is_warning",
    [
        ("dev", False),
        ("1.0.0-dev", False),
        ("1.0.0", True),
    ],
)
@patch("pydolphinscheduler.__version__", new_callable=PropertyMock)
def test_gateway_entry_point_version_warning(
    mock_version, version: str, is_warning: bool
):
    """Test whether gateway entry point will raise version warning or not."""
    mock_version.return_value = version
    mock_version.endswith.return_value = version.endswith("dev")

    importlib.reload(java_gateway)
    with warnings.catch_warnings(record=True) as w:
        _ = java_gateway.GatewayEntryPoint()
        if is_warning:
            assert len(w) == 1
            assert issubclass(w[-1].category, UserWarning)
            assert "Using unmatched version of pydolphinscheduler" in str(w[-1].message)
        else:
            assert len(w) == 0
