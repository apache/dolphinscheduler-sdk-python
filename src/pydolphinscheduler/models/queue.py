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

"""DolphinScheduler User object."""

from typing import Optional

from pydolphinscheduler import configuration
from pydolphinscheduler.java_gateway import gateway
from pydolphinscheduler.models.meta import ModelMeta


class Queue(metaclass=ModelMeta):
    """Model Queue, communicate with DolphinScheduler API server and convert Java Object into Python.

    We use metaclass :class:`pydolphinscheduler.models.meta.ModelMeta` to convert Java Object into Python.
    And code in this class just call Java API method.

    :param id_: queue id, the primary key of queue table
    :param queue_name: queue name, unique key, used to identify queue like get, update, delete
    :param queue: Yarn queue name, deprecate after dolphinscheduler 2.0.0
    """

    def __init__(
        self,
        id_: int,
        queue_name: str,
        queue: str,
    ):
        self.id = id_
        self.queue_name = queue_name
        self.queue = queue

    @classmethod
    def create(cls, queue_name: str, queue: Optional[str] = None) -> "Queue":
        """Create queue.

        :param queue_name: queue name, unique key, used to identify queue like get, update, delete
        :param queue: Yarn queue name, deprecate after dolphinscheduler 2.0.0
        """
        try:
            cls.get(queue_name)
            raise ValueError(f"Tenant {queue_name} already exists")
        except ValueError:
            if queue is None:
                queue = queue_name
            return gateway.create_queue(queue_name, queue)

    @classmethod
    def get(cls, queue_name: str) -> "Queue":
        """Get single queue.

        :param queue_name: queue name, unique key, used to identify queue like get, update, delete
        """
        queue = gateway.get_queue(queue_name)
        if queue is None:
            raise ValueError(f"Tenant {queue_name} not found.")
        return queue

    @classmethod
    def update(cls, tenant_code: str, queue_name: Optional[str], description: Optional[str]) -> "Queue":
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
    def delete(cls, tenant_code) -> "Queue":
        """Delete Tenant.

        :param tenant_code: tenant code you want to delete
        """
        tenant = cls.get(tenant_code)
        gateway.delete_tenant(tenant_code)
        return tenant
    
