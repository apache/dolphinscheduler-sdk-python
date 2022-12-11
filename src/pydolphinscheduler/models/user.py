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

"""DolphinScheduler User models."""

from typing import Optional

from py4j.java_gateway import JavaObject

from pydolphinscheduler import configuration
from pydolphinscheduler.java_gateway import gateway
from pydolphinscheduler.models import BaseSide
from pydolphinscheduler.models.meta import ModelMeta


class User(metaclass=ModelMeta):
    """Model User, communicate with DolphinScheduler API server and convert Java Object into Python.

    We use metaclass :class:`pydolphinscheduler.models.meta.ModelMeta` to convert Java Object into Python.
    And code in this class just call Java API method.

    :param id_: user id, the primary key of tenant table
    :param user_name: username, unique key, used to identify user like get, update, delete
    :param user_password: user password for login
    :param user_type: user type, 0: admin user, 1: general user
    :param email: user email
    :param phone: user phone
    :param tenant_id: the id of tenant who the user belongs to
    :param queue: the queue of user to use
    :param state: user state, 0: inactive, 1: active
    :param time_zone: user time zone, default is UTC, and can be configured with string like `Europe/Amsterdam`.
    """

    def __init__(
        self,
        id_: int,
        user_name: str,
        user_password: str,
        user_type: int,
        email: str,
        phone: str,
        tenant_id: int,
        queue: str,
        state: int,
        time_zone: Optional[str] = None,
    ):
        self.id = id_
        self.user_name = user_name
        self.user_password = user_password
        self._user_type = user_type
        self.email = email
        self.phone = phone
        self.tenant_id = tenant_id
        self.queue = queue
        self._state = state
        self.time_zone = time_zone

    @property
    def user_type(self) -> int:
        """Return user_type with simple Python type."""
        assert isinstance(self._user_type, JavaObject), "user_type must be JavaObject"
        return self._user_type.getCode()

    @user_type.setter
    def user_type(self, user_type: JavaObject) -> None:
        """Set user_type."""
        assert isinstance(user_type, JavaObject), "user_type must be JavaObject"
        self._user_type = user_type

    @property
    def is_admin(self) -> bool:
        """Return True if user is admin."""
        return self._user_type == 0

    @property
    def is_active(self) -> bool:
        """Return True if user is active."""
        return self._state == 1

    @property
    def state(self) -> bool:
        """Return user state, we want to make it more readable."""
        return self.is_active

    @state.setter
    def state(self, state: int) -> None:
        """Set user state."""
        self._state = state

    @staticmethod
    def state_p2j(state: bool) -> int:
        """Convert Python state to Java state."""
        return 1 if state else 0

    @classmethod
    def create(cls, user_name: str, user_password: str, email: str, phone: str, tenant_code: str, queue: str, state: bool) -> "User":
        """Create User.

        Will always create user in admin type in pydolphinscheduler, for operate as much resource as possible.

        :param user_name: username, unique key, used to identify user like get, update, delete
        :param user_password: user password for login
        :param email: user email
        :param phone: user phone
        :param tenant_code: the code of tenant who the user belongs to
        :param queue: the queue of user to use
        :param state: user state, False: inactive, True: active
        """
        state_j = cls.state_p2j(state)
        return gateway.create_user(
            name=user_name,
            password=user_password,
            email=email,
            phone=phone,
            tenant_code=tenant_code,
            queue=queue,
            state=state_j,
        )

    @classmethod
    def get(cls, user_name: str) -> "User":
        """Get User.
        
        :param user_name: username, unique key, used to identify user like get, update, delete
        """
        user = gateway.query_user(user_name)
        if user is None:
            raise ValueError(f"User {user_name} not found.")
        return user

    @classmethod
    def update(cls, user_name: str, user_password: Optional[str] = None, email: Optional[str] = None, phone: Optional[str] = None, tenant_code: Optional[int] = None, queue: Optional[str] = None, state: Optional[bool] = None) -> "User":
        """Update User.

        :param user_name: username, unique key, used to identify user like get, update, delete
        :param user_password: user password for login
        :param email: user email
        :param phone: user phone
        :param tenant_code: the id of tenant who the user belongs to
        :param queue: the queue of user to use
        :param state: user state, False: inactive, True: active
        """
        original_user = cls.get(user_name)
        if user_password:
            original_user.user_password = user_password
        if email:
            original_user.email = email
        if phone:
            original_user.phone = phone
        if tenant_code:
            original_user.tenant_id = tenant_code
        if queue:
            original_user.queue = queue
        if state:
            state_j = cls.state_p2j(state)
            original_user.state = state_j
        return gateway.update_user(
            user_name=user_name,
            user_password=original_user.user_password,
            email=original_user.email,
            phone=original_user.phone,
            tenant_id=original_user.tenant_id,
            queue=original_user.queue,
            state=original_user.state,
        )

    @classmethod
    def delete(cls, user_name) -> "User":
        """Delete User.
        
        :param user_name: username, unique key, used to identify user like get, update, delete
        """
        user = cls.get(user_name)
        gateway.delete_user(user_name)
        return user
