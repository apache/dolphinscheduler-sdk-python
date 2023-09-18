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

"""Test Database."""
import json
from unittest.mock import patch

import pytest

from pydolphinscheduler.models.connection import Connection
from pydolphinscheduler.models.datasource import Datasource

TEST_CONNECTION_PARAMS = {
    "user": "root",
    "password": "mysql",
    "database": "test",
    "jdbcUrl": "jdbc:mysql://127.0.0.1:3306/test",
    "driverClassName": "com.mysql.cj.jdbc.Driver",
    "validationQuery": "select 1",
}


datasource = Datasource(
    id_=1,
    datasource_name="test",
    plugin_name="mysql",
    plugin_version="1.0.0",
    description="test",
    datasource_config=json.dumps(TEST_CONNECTION_PARAMS),
)


@pytest.mark.skip("can not mock javaMap object")
@patch.object(Datasource, "get", return_value=datasource)
def test_get_datasource_attr(mock_datasource):
    """Test get datasource attr."""
    datasource_return = Datasource.get("test_datasource")
    assert (
        Connection(
            **{
                "host": "127.0.0.1",
                "port": "3306",
                "schema": "test",
                "username": "root",
                "password": "mysql",
            }
        )
        == datasource_return.connection
    )
