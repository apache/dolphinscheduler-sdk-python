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

"""Test pydolphinscheduler model user."""

from typing import Dict

import pytest

from pydolphinscheduler.models import User
from pydolphinscheduler.utils import encode


tenant_code = "tenant-code"
queue_name = "tenant-name"
description = "description-of-this-tenant"


user_name = "test-name"
user_password = "test-password"
email = "dolphinscheduler@apache.org"
phone = "12345678912"
tenant_code = "tenant-code"
queue = "test-queue"
state = True


def test_create():
    """Test create user."""
    user = User.create(user_name=user_name, user_password=user_password, email=email, phone=phone, tenant_code=tenant_code, queue=queue, state=state)
    assert user is not None
    assert user.id is not None and user.tenant_id is not None and user.user_name == user_name and user.user_password == encode.md5(user_password) and user.email == email and user.phone == phone and user.queue == queue and user.state == state


def test_get():
    """Test get a single user."""
    user = User.get(user_name=user_name)
    assert user is not None
    assert user.id is not None and user.tenant_id is not None and user.user_name == user_name and user.user_password == encode.md5(user_password) and user.email == email and user.phone == phone and user.queue == queue and user.state == state


def test_get_error():
    """Test get user error."""
    with pytest.raises(ValueError, match="User.*not found."):
        User.get(user_name="not-exists-user")


@pytest.mark.parametrize(
    "update_params, expected",
    [
        ({"password": "new-password"}, {"user_password": encode.md5("new-password")}),
        ({"email": "test-dolphinscheduler@apache.org"}, {"email": "test-dolphinscheduler@apache.org"}),
        ({"phone": reversed(phone)}, {"phone": reversed(phone)}),
        ({"state": False}, {"state": False}),
        ({"email": "test-dolphinscheduler@apache.org", "phone": reversed(phone)}, {"email": "test-dolphinscheduler@apache.org", "phone": reversed(phone)}),
    ]
)
def test_update(update_params: Dict, expected: Dict):
    """Test update a single user."""
    # previous user attributes not equal to expected
    original_user = User.get(user_name=user_name)
    assert all([getattr(original_user, exp) != expected.get(exp) for exp in expected])

    # post user attributes equal to expected
    update_user = User.update(user_name=user_name, **update_params)
    assert update_user is not None and update_user.id is not None and update_user.id == original_user.id and update_user.user_name == original_user.user_name
    assert all([getattr(update_user, exp) == expected.get(exp) for exp in expected])


def test_delete():
    """Test delete a single user."""
    exists_user = User.get(user_name)
    assert exists_user is not None

    User.delete(user_name=user_name)
    user = User.get(user_name)
    assert user is None
