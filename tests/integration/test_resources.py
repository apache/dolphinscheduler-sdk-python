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

"""Test pydolphinscheduler resources."""

import pytest
from py4j.java_gateway import JavaObject

from pydolphinscheduler.core.resource import Resource
from pydolphinscheduler.models.user import User
from tests.testing.constants import UNIT_TEST_TENANT, UNIT_TEST_USER_NAME

name = "unittest_resource.txt"
content = "unittest_resource_content"


@pytest.fixture(scope="module")
def tmp_user():
    """Get a temporary user."""
    user = User(
        name=UNIT_TEST_USER_NAME,
        password="unittest-password",
        email="test-email@abc.com",
        phone="17366637777",
        tenant=UNIT_TEST_TENANT,
        queue="test-queue",
        status=1,
    )
    user.create_if_not_exists()
    yield
    user.delete()


@pytest.mark.skip("activate it when dolphinscheduler default resource center is local file")
def test_create_or_update(tmp_user):
    """Test create or update resource to java gateway."""
    resource = Resource(name=name, content=content, user_name=UNIT_TEST_USER_NAME)
    result = resource.create_or_update_resource()
    assert result is not None and isinstance(result, JavaObject)
    assert result.getAlias() == name


@pytest.mark.skip("activate it when dolphinscheduler default resource center is local file")
def test_get_resource_info(tmp_user):
    """Test get resource info from java gateway."""
    resource = Resource(name=name, user_name=UNIT_TEST_USER_NAME)
    result = resource.get_info_from_database()
    assert result is not None and isinstance(result, JavaObject)
    assert result.getAlias() == name
