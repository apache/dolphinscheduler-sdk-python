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

"""DolphinScheduler Task and TaskRelation object."""
import copy
import types
import warnings
from datetime import timedelta
from logging import getLogger
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union

from pydolphinscheduler import configuration
from pydolphinscheduler.constants import (
    Delimiter,
    IsCache,
    ResourceKey,
    Symbol,
    TaskFlag,
    TaskPriority,
    TaskTimeoutFlag,
)
from pydolphinscheduler.core.parameter import BaseDataType, Direction, ParameterHelper
from pydolphinscheduler.core.resource import Resource
from pydolphinscheduler.core.resource_plugin import ResourcePlugin
from pydolphinscheduler.core.workflow import Workflow, WorkflowContext
from pydolphinscheduler.exceptions import PyDSParamException, PyResPluginException
from pydolphinscheduler.java_gateway import gateway
from pydolphinscheduler.models import Base
from pydolphinscheduler.utils.date import timedelta2timeout

logger = getLogger(__name__)


class TaskRelation(Base):
    """TaskRelation object, describe the relation of exactly two tasks."""

    # Add attr `_KEY_ATTR` to overwrite :func:`__eq__`, it is make set
    # `Task.workflow._task_relations` work correctly.
    _KEY_ATTR = {
        "pre_task_code",
        "post_task_code",
    }

    _DEFINE_ATTR = {
        "pre_task_code",
        "post_task_code",
    }

    _DEFAULT_ATTR = {
        "name": "",
        "preTaskVersion": 1,
        "postTaskVersion": 1,
        "conditionType": 0,
        "conditionParams": {},
    }

    def __init__(
        self,
        pre_task_code: int,
        post_task_code: int,
        name: Optional[str] = None,
    ):
        super().__init__(name)
        self.pre_task_code = pre_task_code
        self.post_task_code = post_task_code

    def __hash__(self):
        return hash(f"{self.pre_task_code} {Delimiter.DIRECTION} {self.post_task_code}")


class Task(Base):
    """Task object, parent class for all exactly task type.

    :param name: The name of the task. Node names within the same workflow must be unique.
    :param task_type:
    :param description: default None
    :param flag: default TaskFlag.YES,
    :param task_priority: default TaskPriority.MEDIUM
    :param worker_group: default configuration.WORKFLOW_WORKER_GROUP
    :param environment_name: default None
    :param delay_time: deault 0
    :param fail_retry_times: default 0
    :param fail_retry_interval: default 1
    :param timeout_notify_strategy: default, None
    :param timeout: default None
    :param resource_list: default None
    :param wait_start_timeout: default None
    :param condition_result: default None,
    :param resource_plugin: default None
    :param is_cache: default False
    :param input_params: default None, input parameters, {param_name: param_value}
    :param output_params: default None, input parameters, {param_name: param_value}
    """

    _DEFINE_ATTR = {
        "name",
        "code",
        "version",
        "task_type",
        "task_params",
        "description",
        "flag",
        "task_priority",
        "worker_group",
        "environment_code",
        "delay_time",
        "fail_retry_times",
        "fail_retry_interval",
        "timeout_flag",
        "timeout_notify_strategy",
        "timeout",
        "is_cache",
    }

    # task default attribute will into `task_params` property
    _task_default_attr = {
        "local_params",
        "resource_list",
        "dependence",
        "wait_start_timeout",
        "condition_result",
    }
    # task attribute ignore from _task_default_attr and will not into `task_params` property
    _task_ignore_attr: set = set()
    # task custom attribute define in sub class and will append to `task_params` property
    _task_custom_attr: set = set()

    ext: set = None
    ext_attr: Union[str, types.FunctionType] = None

    DEFAULT_CONDITION_RESULT = {"successNode": [""], "failedNode": [""]}

    def __init__(
        self,
        name: str,
        task_type: str,
        description: Optional[str] = None,
        flag: Optional[str] = TaskFlag.YES,
        task_priority: Optional[str] = TaskPriority.MEDIUM,
        worker_group: Optional[str] = configuration.WORKFLOW_WORKER_GROUP,
        environment_name: Optional[str] = None,
        delay_time: Optional[int] = 0,
        fail_retry_times: Optional[int] = 0,
        fail_retry_interval: Optional[int] = 1,
        timeout_notify_strategy: Optional = None,
        timeout: Optional[timedelta] = None,
        workflow: Optional[Workflow] = None,
        resource_list: Optional[List] = None,
        dependence: Optional[Dict] = None,
        wait_start_timeout: Optional[Dict] = None,
        condition_result: Optional[Dict] = None,
        resource_plugin: Optional[ResourcePlugin] = None,
        is_cache: Optional[bool] = False,
        input_params: Optional[Dict] = None,
        output_params: Optional[Dict] = None,
        *args,
        **kwargs,
    ):
        super().__init__(name, description)
        self.task_type = task_type
        self.flag = flag
        self._is_cache = is_cache
        self.task_priority = task_priority
        self.worker_group = worker_group
        self._environment_name = environment_name
        self.fail_retry_times = fail_retry_times
        self.fail_retry_interval = fail_retry_interval
        self.delay_time = delay_time
        self.timeout_notify_strategy = timeout_notify_strategy
        self._timeout: timedelta = timeout
        self._workflow = None
        self._input_params = input_params or {}
        self._output_params = output_params or {}
        if "process_definition" in kwargs:
            warnings.warn(
                "The `process_definition` parameter is deprecated, please use `workflow` instead.",
                DeprecationWarning,
            )
            self.workflow = kwargs.pop("process_definition")
        else:
            self.workflow: Workflow = workflow or WorkflowContext.get()

        if "local_params" in kwargs:
            warnings.warn(
                """The `local_params` parameter is deprecated,
                please use `input_params` and `output_params` instead.
                """,
                DeprecationWarning,
            )
            self._local_params = kwargs.get("local_params")

        self._upstream_task_codes: Set[int] = set()
        self._downstream_task_codes: Set[int] = set()
        self._task_relation: Set[TaskRelation] = set()
        # move attribute code and version after _workflow and workflow declare
        self.code, self.version = self.gen_code_and_version()
        # Add task to workflow, maybe we could put into property workflow latter

        if self.workflow is not None and self.code not in self.workflow.tasks:
            self.workflow.add_task(self)
        else:
            logger.warning(
                "Task code %d already in workflow, prohibit re-add task.",
                self.code,
            )

        # Attribute for task param
        self._resource_list = resource_list or []
        self.dependence = dependence or {}
        self.wait_start_timeout = wait_start_timeout or {}
        self._condition_result = condition_result or self.DEFAULT_CONDITION_RESULT
        self.resource_plugin = resource_plugin
        self.get_content()

    @property
    def workflow(self) -> Optional[Workflow]:
        """Get attribute workflow."""
        return self._workflow

    @workflow.setter
    def workflow(self, workflow: Optional[Workflow]):
        """Set attribute workflow."""
        self._workflow = workflow

    @property
    def timeout(self) -> int:
        """Get attribute timeout."""
        return timedelta2timeout(self._timeout) if self._timeout else 0

    @timeout.setter
    def timeout(self, val: timedelta) -> None:
        """Set attribute timeout."""
        self._timeout = val

    @property
    def timeout_flag(self) -> str:
        """Whether the timeout attribute is being set or not."""
        return TaskTimeoutFlag.ON if self._timeout else TaskTimeoutFlag.OFF

    @property
    def is_cache(self) -> str:
        """Whether the cache is being set or not."""
        if isinstance(self._is_cache, bool):
            return IsCache.YES if self._is_cache else IsCache.NO
        else:
            raise PyDSParamException("is_cache must be a bool")

    @property
    def resource_list(self) -> List[Dict[str, Resource]]:
        """Get task define attribute `resource_list`."""
        resources = set()
        for res in self._resource_list:
            if type(res) == str:
                resources.add(
                    Resource(
                        name=res, user_name=self.user_name
                    ).get_fullname_from_database()
                )
            elif type(res) == dict and ResourceKey.NAME in res:
                warnings.warn(
                    """`resource_list` should be defined using List[str] with resource paths,
                       the use of ids to define resources will be remove in version 3.2.0.
                    """,
                    DeprecationWarning,
                    stacklevel=2,
                )
                resources.add(res.get(ResourceKey.NAME))
        return [{ResourceKey.NAME: r} for r in resources]

    @property
    def user_name(self) -> Optional[str]:
        """Return username of workflow."""
        if self.workflow:
            return self.workflow.user.name
        else:
            raise PyDSParamException("`user_name` cannot be empty.")

    @property
    def condition_result(self) -> Dict:
        """Get attribute condition_result."""
        return self._condition_result

    @condition_result.setter
    def condition_result(self, condition_result: Optional[Dict]):
        """Set attribute condition_result."""
        self._condition_result = condition_result

    def _get_attr(self) -> Set[str]:
        """Get final task task_params attribute.

        Base on `_task_default_attr`, append attribute from `_task_custom_attr` and subtract attribute from
        `_task_ignore_attr`.
        """
        attr = copy.deepcopy(self._task_default_attr)
        attr -= self._task_ignore_attr
        attr |= self._task_custom_attr
        return attr

    @property
    def task_params(self) -> Optional[Dict]:
        """Get task parameter object.

        Will get result to combine _task_custom_attr and custom_attr.
        """
        custom_attr = self._get_attr()
        return self.get_define_custom(custom_attr=custom_attr)

    def get_plugin(self):
        """Return the resource plug-in.

        according to parameter resource_plugin and parameter
        workflow.resource_plugin.
        """
        if self.resource_plugin is None:
            if self.workflow.resource_plugin is not None:
                return self.workflow.resource_plugin
            else:
                raise PyResPluginException(
                    "The execution command of this task is a file, but the resource plugin is empty"
                )
        else:
            return self.resource_plugin

    def get_content(self):
        """Get the file content according to the resource plugin."""
        if self.ext_attr is None and self.ext is None:
            return
        _ext_attr = getattr(self, self.ext_attr)
        if _ext_attr is not None:
            if isinstance(_ext_attr, str) and _ext_attr.endswith(tuple(self.ext)):
                res = self.get_plugin()
                content = res.read_file(_ext_attr)
                setattr(self, self.ext_attr.lstrip(Symbol.UNDERLINE), content)
            else:
                if self.resource_plugin is not None or (
                    self.workflow is not None
                    and self.workflow.resource_plugin is not None
                ):
                    index = _ext_attr.rfind(Symbol.POINT)
                    if index != -1:
                        raise ValueError(
                            "This task does not support files with suffix {}, only supports {}".format(
                                _ext_attr[index:],
                                Symbol.COMMA.join(str(suf) for suf in self.ext),
                            )
                        )
                setattr(self, self.ext_attr.lstrip(Symbol.UNDERLINE), _ext_attr)

    def __hash__(self):
        return hash(self.code)

    def __lshift__(self, other: Union["Task", Sequence["Task"]]):
        """Implement Task << Task."""
        self.set_upstream(other)
        return other

    def __rshift__(self, other: Union["Task", Sequence["Task"]]):
        """Implement Task >> Task."""
        self.set_downstream(other)
        return other

    def __rrshift__(self, other: Union["Task", Sequence["Task"]]):
        """Call for Task >> [Task] because list don't have __rshift__ operators."""
        self.__lshift__(other)
        return self

    def __rlshift__(self, other: Union["Task", Sequence["Task"]]):
        """Call for Task << [Task] because list don't have __lshift__ operators."""
        self.__rshift__(other)
        return self

    def _set_deps(
        self, tasks: Union["Task", Sequence["Task"]], upstream: bool = True
    ) -> None:
        """
        Set parameter tasks dependent to current task.

        it is a wrapper for :func:`set_upstream` and :func:`set_downstream`.
        """
        if not isinstance(tasks, Sequence):
            tasks = [tasks]

        for task in tasks:
            if upstream:
                self._upstream_task_codes.add(task.code)
                task._downstream_task_codes.add(self.code)

                if self._workflow:
                    task_relation = TaskRelation(
                        pre_task_code=task.code,
                        post_task_code=self.code,
                        name=f"{task.name} {Delimiter.DIRECTION} {self.name}",
                    )
                    self.workflow._task_relations.add(task_relation)
            else:
                self._downstream_task_codes.add(task.code)
                task._upstream_task_codes.add(self.code)

                if self._workflow:
                    task_relation = TaskRelation(
                        pre_task_code=self.code,
                        post_task_code=task.code,
                        name=f"{self.name} {Delimiter.DIRECTION} {task.name}",
                    )
                    self.workflow._task_relations.add(task_relation)

    def set_upstream(self, tasks: Union["Task", Sequence["Task"]]) -> None:
        """Set parameter tasks as upstream to current task."""
        self._set_deps(tasks, upstream=True)

    def set_downstream(self, tasks: Union["Task", Sequence["Task"]]) -> None:
        """Set parameter tasks as downstream to current task."""
        self._set_deps(tasks, upstream=False)

    # TODO code should better generate in bulk mode when :ref: workflow run submit or start
    def gen_code_and_version(self) -> Tuple:
        """
        Generate task code and version from java gateway.

        If task name do not exists in workflow before, if will generate new code and version id
        equal to 0 by java gateway, otherwise if will return the exists code and version.
        """
        # TODO get code from specific project workflow and task name
        result = gateway.get_code_and_version(
            self.workflow._project, self.workflow.name, self.name
        )
        # result = gateway.entry_point.genTaskCodeList(DefaultTaskCodeNum.DEFAULT)
        # gateway_result_checker(result)
        return result.get("code"), result.get("version")

    @property
    def environment_code(self) -> str:
        """Convert environment name to code."""
        if self._environment_name is None:
            return None
        return gateway.query_environment_info(self._environment_name)

    @property
    def local_params(self):
        """Convert local params."""
        local_params = (
            copy.deepcopy(self._local_params) if hasattr(self, "_local_params") else []
        )
        local_params.extend(
            ParameterHelper.convert_params(self._input_params, Direction.IN)
        )
        local_params.extend(
            ParameterHelper.convert_params(self._output_params, Direction.OUT)
        )
        return local_params

    def add_in(
        self,
        name: str,
        value: Optional[Union[int, str, float, bool, BaseDataType]] = None,
    ):
        """Add input parameters.

        :param name: name of the input parameter.
        :param value: value of the input parameter.

        It could be simply command::

            task.add_in("a")
            task.add_in("b", 123)
            task.add_in("c", bool)
            task.add_in("d", ParameterType.LONG(123))

        """
        self._input_params[name] = value

    def add_out(
        self,
        name: str,
        value: Optional[Union[int, str, float, bool, BaseDataType]] = None,
    ):
        """Add output parameters.

        :param name: name of the output parameter.
        :param value: value of the output parameter.

        It could be simply command::

            task.add_out("a")
            task.add_out("b", 123)
            task.add_out("c", bool)
            task.add_out("d", ParameterType.LONG(123))

        """
        self._output_params[name] = value
