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

"""Test pydolphinscheduler models tenant."""

from typing import Dict

import pytest

from pydolphinscheduler.models import Tenant, User

tenant_code = "tenant-code"
queue_name = "tenant-name"
description = "description-of-this-tenant"


def test_create():
    """Test create tenant."""
    tenant = Tenant.create(tenant_code, queue_name, description)
    assert tenant is not None
    assert tenant.id is not None and tenant.tenant_code == tenant_code and tenant.queue_name == queue_name and tenant.description == description


def test_get():
    """Test get tenant."""
    tenant = Tenant.get(tenant_code)
    assert tenant is not None
    assert tenant.id is not None and tenant.tenant_code == tenant_code and tenant.queue_name == queue_name and tenant.description == description


def test_get_error():
    """Test get tenant error."""
    with pytest.raises(ValueError, match="Tenant.*not found."):
        Tenant.get(tenant_code="not-exists-tenant")


@pytest.mark.parametrize(
    "update_params, expected",
    [
        ({"queue_name": "new_queue_name"}, {"queue_name": "new_queue_name"}),
        ({"description": "new_description"}, {"description": "new_description"}),
        ({"queue_name": "new_queue_name", "description": "new_description"}, {"queue_name": "new_queue_name", "description": "new_description"}),
    ]
)
def test_update(update_params: Dict, expected: Dict):
    """Test update tenant."""
    # previous user attributes not equal to expected
    original_tenant = Tenant.get(tenant_code=tenant_code)
    assert all([getattr(original_tenant, exp) != expected.get(exp) for exp in expected])

    # post user attributes equal to expected
    update_tenant = Tenant.update(tenant_code, **update_params)
    assert update_tenant is not None and update_tenant.id is not None and update_tenant.id == original_tenant.id and update_tenant.tenant_code == original_tenant.tenant_code
    assert update_tenant.id is not None and update_tenant.tenant_code == tenant_code and update_tenant.queue_name == queue_name and update_tenant.description == description


def test_delete():
    """Test delete tenant."""
    tenant = Tenant.update(tenant_code)
    assert tenant is not None
    assert tenant.id is not None and tenant.tenant_code == tenant_code and tenant.queue_name == queue_name and tenant.description == description
