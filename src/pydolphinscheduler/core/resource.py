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

"""Module resource."""

from __future__ import annotations

from pydolphinscheduler.exceptions import PyDSParamException
from pydolphinscheduler.java_gateway import gateway
from pydolphinscheduler.models import Base


class Resource(Base):
    """resource object, will define the resources that you want to create or update.

    :param name: The fullname of resource.Includes path and suffix.
    :param content: The description of resource.
    :param description: The description of resource.
    :param user_name: The user name of resource.
    """

    _DEFINE_ATTR = {"name", "content", "description", "user_name"}

    def __init__(
        self,
        name: str,
        content: str | None = None,
        description: str | None = None,
        user_name: str | None = None,
    ):
        super().__init__(name, description)
        self.content = content
        self.user_name = user_name
        self._resource_code = None

    def get_info_from_database(self):
        """Get resource info from java gateway, contains resource id, name."""
        if not self.user_name:
            raise PyDSParamException(
                "`user_name` is required when querying resources from python gate."
            )
        return gateway.query_resources_file_info(self.user_name, self.name)

    def get_fullname_from_database(self):
        """Get resource fullname from java gateway."""
        return self.get_info_from_database().getFullName()

    def create_or_update_resource(self):
        """Create or update resource via java gateway."""
        if not self.content or not self.user_name:
            raise PyDSParamException(
                "`user_name` and `content` are required when create or update resource from python gate."
            )
        return gateway.create_or_update_resource(
            self.user_name,
            self.name,
            self.content,
        )
