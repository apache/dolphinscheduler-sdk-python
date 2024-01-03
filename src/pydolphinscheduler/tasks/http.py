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

"""Task shell."""

from __future__ import annotations

from pydolphinscheduler.constants import TaskType
from pydolphinscheduler.core.task import Task
from pydolphinscheduler.exceptions import PyDSParamException
from pydolphinscheduler.core.parameter import ParameterHelper
import warnings


class HttpMethod:
    """Constant of HTTP method."""

    GET = "GET"
    POST = "POST"
    HEAD = "HEAD"
    PUT = "PUT"
    DELETE = "DELETE"


class HttpCheckCondition:
    """Constant of HTTP check condition.

    For now it contain four value:
    - STATUS_CODE_DEFAULT: when http response code equal to 200, mark as success.
    - STATUS_CODE_CUSTOM: when http response code equal to the code user define, mark as success.
    - BODY_CONTAINS: when http response body contain text user define, mark as success.
    - BODY_NOT_CONTAINS: when http response body do not contain text user define, mark as success.
    """

    STATUS_CODE_DEFAULT = "STATUS_CODE_DEFAULT"
    STATUS_CODE_CUSTOM = "STATUS_CODE_CUSTOM"
    BODY_CONTAINS = "BODY_CONTAINS"
    BODY_NOT_CONTAINS = "BODY_NOT_CONTAINS"


class Http(Task):
    """Task HTTP object, declare behavior for HTTP task to dolphinscheduler.
    Attributes:
        _task_custom_attr (set): A set containing custom attributes specific to the Http task, 
                                including 'url', 'http_method', 'http_params', and more.
    Args:                            
        :param str name: The name or identifier for the HTTP task.
        :param str url: The URL endpoint for the HTTP request.
        :param str http_method: The HTTP method for the request (GET, POST, etc.). Defaults to HttpMethod.GET.
        :param dict http_params: Parameters for the HTTP request. Defaults to None.
        :param str http_check_condition: Condition for checking the HTTP response status. 
                                        Defaults to HttpCheckCondition.STATUS_CODE_DEFAULT.
        :param str condition: Additional condition to evaluate if `http_check_condition` is not STATUS_CODE_DEFAULT.
        :param int connect_timeout: Connection timeout for the HTTP request in milliseconds. Defaults to 60000.
        :param int socket_timeout: Socket timeout for the HTTP request in milliseconds. Defaults to 60000.

        
    Raises:
        PyDSParamException: Exception raised for invalid parameters, such as unsupported HTTP methods or conditions.

    Example:
        Usage example for creating an HTTP task:
        http_task = Http(name="http_task", url="https://api.example.com", http_method="POST", http_params={"key": "value"})
    """

    _task_custom_attr = {
        "url",
        "http_method",
        "http_params",
        "http_check_condition",
        "condition",
        "connect_timeout",
        "socket_timeout",
    }

    def __init__(
        self,
        name: str,
        url: str,
        http_method: str | None = HttpMethod.GET,
        http_params: dict | None = None,
        http_check_condition: str | None = HttpCheckCondition.STATUS_CODE_DEFAULT,
        condition: str | None = None,
        connect_timeout: int | None = 60000,
        socket_timeout: int | None = 60000,
        *args,
        **kwargs,
    ):
        super().__init__(name, TaskType.HTTP, *args, **kwargs)
        self.url = url
        if not hasattr(HttpMethod, http_method):
            raise PyDSParamException(
                "Parameter http_method %s not support.", http_method
            )
        
        if isinstance(http_params, list):
            warnings.warn(
                "The `http_params` parameter currently accepts a dictionary instead of a list. Your parameter is being ignored.",
                DeprecationWarning,
            )
            
        self.http_method = http_method
        self._http_params = http_params

    @property
    def http_params(self):
        """Property to convert http_params using ParameterHelper when accessed."""
        return ParameterHelper.convert_params(self._http_params, direction=Direction.IN) if self._http_params else []

    


    if not hasattr(HttpCheckCondition, http_check_condition):
        raise PyDSParamException(
                "Parameter http_check_condition %s not support.", http_check_condition
            )
    self.http_check_condition = http_check_condition
    if (
        http_check_condition != HttpCheckCondition.STATUS_CODE_DEFAULT
            and condition is None
        ):
        raise PyDSParamException(
            "Parameter condition must provider if http_check_condition not equal to STATUS_CODE_DEFAULT"
            )
    self.condition = condition
    self.connect_timeout = connect_timeout
    self.socket_timeout = socket_timeout
