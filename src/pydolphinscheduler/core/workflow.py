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

"""Module workflow, core class for workflow define."""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from typing import Any

from pydolphinscheduler import configuration
from pydolphinscheduler.constants import Symbol, TaskType
from pydolphinscheduler.core.resource import Resource
from pydolphinscheduler.core.resource_plugin import ResourcePlugin
from pydolphinscheduler.exceptions import PyDSParamException, PyDSTaskNoFoundException
from pydolphinscheduler.java_gateway import gateway
from pydolphinscheduler.models import Base, Project, User
from pydolphinscheduler.utils.date import (
    MAX_DATETIME,
    conv_from_str,
    conv_to_schedule,
    timedelta2timeout,
)


class WorkflowContext:
    """Class workflow context, use when task get workflow from context expression."""

    _context_managed_workflow: Workflow | None = None

    @classmethod
    def set(cls, workflow: Workflow) -> None:
        """Set attribute self._context_managed_workflow."""
        cls._context_managed_workflow = workflow

    @classmethod
    def get(cls) -> Workflow | None:
        """Get attribute self._context_managed_workflow."""
        return cls._context_managed_workflow

    @classmethod
    def delete(cls) -> None:
        """Delete attribute self._context_managed_workflow."""
        cls._context_managed_workflow = None


class Workflow(Base):
    """Workflow object, will define workflow attribute, task, relation.

    TODO: maybe we should rename this class, currently use DS object name.

    :param online_schedule: Whether the online workflow is schedule. It will be automatically configured
        according to :param:``schedule`` configuration. If the :param:``schedule`` is assigned with valid
        value, :param:``online_schedule`` will be set to ``True``. But you can also manually specify
        :param:``online_schedule``. For example if you only want to set the workflow :param:``schedule`` but
        do not want to online the workflow schedule, you can set :param:``online_schedule`` to ``False``.
    :param execution_type: Decision which behavior to run when workflow have multiple instances.
        when workflow schedule interval is too short, it may cause multiple instances run at the
        same time. We can use this parameter to control the behavior about how to run those workflows
        instances. Currently we have four execution type:

          * ``PARALLEL``: Default value, all instances will allow to run even though the previous
            instance is not finished.
          * ``SERIAL_WAIT``: All instance will wait for the previous instance to finish, and all
            the waiting instances will be executed base on scheduling order.
          * ``SERIAL_DISCARD``: All instances will be discard(abandon) if the previous instance is not
            finished.
          * ``SERIAL_PRIORITY``: means the all instance will wait for the previous instance to finish, and
            all the waiting instances will be executed base on workflow priority order.
    :param timeout: Timeout attribute for task, in minutes. Task is consider as timed out task when the
        running time of a task exceeds than this value. when data type is :class:`datetime.timedelta` will
        be converted to int(in minutes). default ``0``
    :param user: The user for current workflow. Will create a new one if it do not exists. If your
        parameter ``project`` already exists but project's create do not belongs to ``user``, will grant
        ``project`` to ``user`` automatically.
    :param project: The project for current workflow. You could see the workflow in this project
        thought Web UI after it :func:`submit` or :func:`run`. It will create a new project belongs to
        ``user`` if it does not exists. And when ``project`` exists but project's create do not belongs
        to ``user``, will grant `project` to ``user`` automatically.
    :param resource_list: Resource files required by the current workflow.You can create and modify
        resource files from this field. When the workflow is submitted, these resource files are
        also submitted along with it.
    """

    # key attribute for identify Workflow object
    _KEY_ATTR = {
        "name",
        "project",
        "release_state",
        "param",
    }

    _DEFINE_ATTR = {
        "name",
        "description",
        "_project",
        "worker_group",
        "warning_type",
        "warning_group_id",
        "execution_type",
        "timeout",
        "release_state",
        "param",
        "tasks",
        "task_definition_json",
        "task_relation_json",
        "resource_list",
    }

    _EXPECT_SCHEDULE_CHAR_NUM = 7

    def __init__(
        self,
        name: str,
        description: str | None = None,
        schedule: str | None = None,
        online_schedule: bool | None = None,
        start_time: str | datetime | None = None,
        end_time: str | datetime | None = None,
        timezone: str | None = configuration.WORKFLOW_TIME_ZONE,
        user: str | None = configuration.WORKFLOW_USER,
        project: str | None = configuration.WORKFLOW_PROJECT,
        worker_group: str | None = configuration.WORKFLOW_WORKER_GROUP,
        warning_type: str | None = configuration.WORKFLOW_WARNING_TYPE,
        warning_group_id: int | None = 0,
        execution_type: str | None = configuration.WORKFLOW_EXECUTION_TYPE,
        timeout: timedelta | int | None = 0,
        release_state: str | None = configuration.WORKFLOW_RELEASE_STATE,
        param: dict | None = None,
        resource_plugin: ResourcePlugin | None = None,
        resource_list: list[Resource] | None = None,
        *args,
        **kwargs,
    ):
        super().__init__(name, description)
        self.schedule = schedule.strip() if schedule else schedule
        if (
            self.schedule
            and self.schedule.count(Symbol.BLANK) != self._EXPECT_SCHEDULE_CHAR_NUM - 1
        ):
            raise PyDSParamException(
                "Invlaid parameter schedule, expect crontab char is %d but get %s",
                self._EXPECT_SCHEDULE_CHAR_NUM,
                schedule,
            )

        #  handle workflow schedule state according to init value
        if self.schedule and online_schedule is None:
            self.online_schedule = True
        else:
            self.online_schedule = online_schedule or False
        self._start_time = start_time
        self._end_time = end_time
        self.timezone = timezone
        self._user = user
        self._project = project
        self.worker_group = worker_group
        self.warning_type = warning_type
        if warning_type.strip().upper() not in ("FAILURE", "SUCCESS", "ALL", "NONE"):
            raise PyDSParamException(
                "Parameter `warning_type` with unexpect value `%s`", warning_type
            )
        else:
            self.warning_type = warning_type.strip().upper()
        self.warning_group_id = warning_group_id
        if execution_type is None or execution_type.strip().upper() not in (
            "PARALLEL",
            "SERIAL_WAIT",
            "SERIAL_DISCARD",
            "SERIAL_PRIORITY",
        ):
            raise PyDSParamException(
                "Parameter `execution_type` with unexpect value `%s`", execution_type
            )
        else:
            self._execution_type = execution_type
        self._timeout: timedelta | int = timeout
        self._release_state = release_state
        self.param = param
        self.tasks: dict = {}
        self.resource_plugin = resource_plugin
        # TODO how to fix circle import
        self._task_relations: set[TaskRelation] = set()  # noqa: F821
        self._workflow_code = None
        self.resource_list = resource_list or []

    def __enter__(self) -> Workflow:
        WorkflowContext.set(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        WorkflowContext.delete()

    @property
    def project(self) -> Project:
        """Get attribute project."""
        return Project(self._project)

    @project.setter
    def project(self, project: Project) -> None:
        """Set attribute project."""
        self._project = project.name

    @property
    def user(self) -> User:
        """Get user object.

        For now we just get from python models but not from java gateway models, so it may not correct.
        """
        return User(name=self._user)

    @staticmethod
    def _parse_datetime(val: Any) -> Any:
        if val is None or isinstance(val, datetime):
            return val
        elif isinstance(val, str):
            return conv_from_str(val)
        else:
            raise PyDSParamException("Do not support value type %s for now", type(val))

    @property
    def start_time(self) -> Any:
        """Get attribute start_time."""
        return self._parse_datetime(self._start_time)

    @start_time.setter
    def start_time(self, val) -> None:
        """Set attribute start_time."""
        self._start_time = val

    @property
    def end_time(self) -> Any:
        """Get attribute end_time."""
        return self._parse_datetime(self._end_time)

    @end_time.setter
    def end_time(self, val) -> None:
        """Set attribute end_time."""
        self._end_time = val

    @property
    def release_state(self) -> int:
        """Get attribute release_state."""
        rs_ref = {
            "online": 1,
            "offline": 0,
        }
        if self._release_state not in rs_ref:
            raise PyDSParamException(
                "Parameter release_state only support `online` or `offline` but get %",
                self._release_state,
            )
        return rs_ref[self._release_state]

    @release_state.setter
    def release_state(self, val: str) -> None:
        """Set attribute release_state."""
        self._release_state = val.lower()

    @property
    def timeout(self) -> int:
        """Get attribute timeout."""
        if isinstance(self._timeout, int):
            if self._timeout < 0:
                raise PyDSParamException("The timeout value must be greater than 0")
            return self._timeout
        return timedelta2timeout(self._timeout) if self._timeout else 0

    @property
    def execution_type(self) -> str:
        """Get attribute execution_type."""
        return self._execution_type.upper()

    @execution_type.setter
    def execution_type(self, val: str) -> None:
        """Set attribute execution_type."""
        self._execution_type = val

    @property
    def param_json(self) -> list[dict] | None:
        """Return param json base on self.param."""
        # Handle empty dict and None value
        if not self.param:
            return []
        return [
            {
                "prop": k,
                "direct": "IN",
                "type": "VARCHAR",
                "value": v,
            }
            for k, v in self.param.items()
        ]

    @property
    def task_definition_json(self) -> list[dict]:
        """Return all tasks definition in list of dict."""
        if not self.tasks:
            return [self.tasks]
        else:
            return [task.get_define() for task in self.tasks.values()]

    @property
    def task_relation_json(self) -> list[dict]:
        """Return all relation between tasks pair in list of dict."""
        if not self.tasks:
            return [self.tasks]
        else:
            self._handle_root_relation()
            return [tr.get_define() for tr in self._task_relations]

    @property
    def schedule_json(self) -> dict | None:
        """Get schedule parameter json object. This is requests from java gateway interface."""
        if not self.schedule:
            return None
        else:
            start_time = conv_to_schedule(
                self.start_time if self.start_time else datetime.now()
            )
            end_time = conv_to_schedule(
                self.end_time if self.end_time else MAX_DATETIME
            )
            return {
                "startTime": start_time,
                "endTime": end_time,
                "crontab": self.schedule,
                "timezoneId": self.timezone,
            }

    @property
    def task_list(self) -> list[Task]:  # noqa: F821
        """Return list of tasks objects."""
        return list(self.tasks.values())

    def _handle_root_relation(self):
        """Handle root task property :class:`pydolphinscheduler.core.task.TaskRelation`.

        Root task in DAG do not have dominant upstream node, but we have to add an exactly default
        upstream task with task_code equal to `0`. This is requests from java gateway interface.
        """
        from pydolphinscheduler.core.task import TaskRelation

        post_relation_code = set()
        for relation in self._task_relations:
            post_relation_code.add(relation.post_task_code)
        for task in self.task_list:
            if task.code not in post_relation_code:
                root_relation = TaskRelation(pre_task_code=0, post_task_code=task.code)
                self._task_relations.add(root_relation)

    def add_task(self, task: Task) -> None:  # noqa: F821
        """Add a single task to workflow."""
        self.tasks[task.code] = task
        task._workflow = self

    def add_tasks(self, tasks: list[Task]) -> None:  # noqa: F821
        """Add task sequence to workflow, it a wrapper of :func:`add_task`."""
        for task in tasks:
            self.add_task(task)

    def get_task(self, code: str) -> Task:  # noqa: F821
        """Get task object from workflow by given code."""
        if code not in self.tasks:
            raise PyDSTaskNoFoundException(
                "Task with code %s can not found in workflow %",
                (code, self.name),
            )
        return self.tasks[code]

    # TODO which tying should return in this case
    def get_tasks_by_name(self, name: str) -> set[Task]:  # noqa: F821
        """Get tasks object by given name, if will return all tasks with this name."""
        find = set()
        for task in self.tasks.values():
            if task.name == name:
                find.add(task)
        return find

    def get_one_task_by_name(self, name: str) -> Task:  # noqa: F821
        """Get exact one task from workflow by given name.

        Function always return one task even though this workflow have more than one task with
        this name.
        """
        tasks = self.get_tasks_by_name(name)
        if not tasks:
            raise PyDSTaskNoFoundException(f"Can not find task with name {name}.")
        return tasks.pop()

    def run(self):
        """Submit and Start Workflow instance.

        Shortcut for function :func:`submit` and function :func:`start`. Only support manual start workflow
        for now, and schedule run will coming soon.
        :return:
        """
        self.submit()
        self.start()

    def _ensure_side_model_exists(self):
        """Ensure workflow models model exists.

        For now, models object including :class:`pydolphinscheduler.models.project.Project`,
        :class:`pydolphinscheduler.models.tenant.Tenant`, :class:`pydolphinscheduler.models.user.User`.
        If these model not exists, would create default value according to
        :class:`pydolphinscheduler.configuration`.
        """
        # TODO used metaclass for more pythonic
        self.user.create_if_not_exists()
        # Project model need User object exists
        self.project.create_if_not_exists(self._user)

    def _pre_submit_check(self):
        """Check specific condition satisfy before.

        This method should be called before workflow submit to java gateway
        For now, we have below checker:
        * `self.param` or at least one local param of task should be set if task `switch` in this workflow.
        """
        if (
            any([task.task_type == TaskType.SWITCH for task in self.tasks.values()])
            and self.param is None
            and all([len(task.local_params) == 0 for task in self.tasks.values()])
        ):
            raise PyDSParamException(
                "Parameter param or at least one local_param of task must "
                "be provider if task Switch in workflow."
            )

    def submit(self) -> int:
        """Submit Workflow instance to java gateway."""
        self._ensure_side_model_exists()
        self._pre_submit_check()

        # resource should be created before workflow
        if len(self.resource_list) > 0:
            for res in self.resource_list:
                res.user_name = self._user
                res.create_or_update_resource()

        self._workflow_code = gateway.create_or_update_workflow(
            self._user,
            self._project,
            self.name,
            str(self.description) if self.description else "",
            json.dumps(self.param_json),
            self.warning_type,
            self.warning_group_id,
            self.execution_type,
            self.timeout,
            self.worker_group,
            self.release_state,
            # TODO add serialization function
            json.dumps(self.task_relation_json),
            json.dumps(self.task_definition_json),
            json.dumps(self.schedule_json) if self.schedule_json else None,
            self.online_schedule,
            None,
        )
        return self._workflow_code

    def start(self) -> None:
        """Create and start Workflow instance.

        which post to `start-process-instance` to java gateway
        """
        gateway.exec_workflow_instance(
            self._user,
            self._project,
            self.name,
            self.worker_group,
            self.warning_type,
            self.warning_group_id,
        )
