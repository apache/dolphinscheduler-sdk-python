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

"""DolphinScheduler Tenant model."""

from typing import Optional

from pydolphinscheduler.java_gateway import gateway
from pydolphinscheduler.models.meta import ModelMeta


class Tenant(metaclass=ModelMeta):
    """Model Tenant, communicate with DolphinScheduler API server and convert Java Object into Python.

    We use metaclass :class:`pydolphinscheduler.models.meta.ModelMeta` to convert Java Object into Python.
    And code in this class just call Java API method.

    :param id_: tenant id, the primary key of tenant table
    :param tenant_code: tenant code, unique key, used to identify tenant like get, update, delete
    :param queue_id: the queue id used by this tenant
    :param queue_name: the queue name used by this tenant
    :param queue: queue
    :param description: description of current tenant
    """

    def __init__(
        self,
        id_: int,
        tenant_code: str,
        queue_id: str,
        queue_name: str,
        queue: str,
        description: Optional[str] = None,
    ):
        self.id = id_
        self.tenant_code = tenant_code
        self.queue_id = queue_id
        self.queue_name = queue_name
        self.queue = queue
        self.description = description

    @classmethod
    def create(cls, tenant_code: str, queue_name: str, description: str) -> "Tenant":
        """Create tenant.

        :param tenant_code: tenant code
        :param queue_name: queue name
        :param description: description
        """
        try:
            cls.get(tenant_code)
            raise ValueError(f"Tenant {tenant_code} already exists")
        except ValueError:
            return gateway.create_tenant(tenant_code, queue_name, description)

    @classmethod
    def get(cls, tenant_code: str) -> "Tenant":
        """Get single Tenant.

        :param tenant_code: tenant code
        """
        tenant = gateway.query_tenant(tenant_code)
        if tenant is None:
            raise ValueError(f"Tenant {tenant_code} not found.")
        return tenant

    @classmethod
    def update(cls, tenant_code: str, queue_name: Optional[str], description: Optional[str]) -> "Tenant":
        """Update Tenant.

        :param tenant_code: tenant code, unique key.
        :param queue_name: new queue name you want to update
        :param description: new description you want to update
        """

        original_tenant = cls.get(tenant_code)
        if queue_name:
            original_tenant.queue_name = queue_name
        if description:
            original_tenant.description = description
        tenant = gateway.update_tenant(original_tenant.id, original_tenant.tenant_code, original_tenant.description)
        return tenant

    @classmethod
    def delete(cls, tenant_code) -> "Tenant":
        """Delete Tenant.

        :param tenant_code: tenant code you want to delete
        """
        tenant = cls.get(tenant_code)
        gateway.delete_tenant(tenant_code)
        return tenant
