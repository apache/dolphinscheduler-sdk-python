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
from typing import Dict, List, Optional

from pydolphinscheduler.constants import TaskType
from pydolphinscheduler.core.task import Task
from pydolphinscheduler.tasks.mixin.datasource_list_mixin import DatasourceListMixin
from pydolphinscheduler.tasks.mixin.remote_connection_mixin import RemoteConnectionMixin


class Shell(Task, DatasourceListMixin, RemoteConnectionMixin):
    """Task shell object, declare behavior for shell task to dolphinscheduler.

    :param name: A unique, meaningful string for the shell task.
    :param command: One or more command want to run in this task.

        It could be simply command::

            Shell(name=..., command="echo task shell")

        or maybe same commands trying to do complex task::

            command = '''echo task shell step 1;
            echo task shell step 2;
            echo task shell step 3
            '''

            Shell(name=..., command=command)

    """

    # TODO maybe we could use instance name to replace attribute `name`
    #  which is simplify as `task_shell = Shell(command = "echo 1")` and
    #  task.name assign to `task_shell`

    _task_custom_attr = {
        "raw_script",
    }

    ext: set = {".sh", ".zsh"}
    ext_attr: str = "_raw_script"

    def __init__(
        self,
        name: str,
        command: str,
        datasource_name: Optional[List[str]] = None,
        remote_connection: Optional[str] = None,
        *args,
        **kwargs
    ):
        self._raw_script = command
        self.datasource_name = datasource_name
        self.remote_connection = remote_connection
        super().__init__(name, TaskType.SHELL, *args, **kwargs)

    @property
    def task_params(self, camel_attr: bool = True, custom_attr: set = None) -> Dict:
        """Override Task.task_params for sql task.

        sql task have some specials attribute for task_params, and is odd if we
        directly set as python property, so we Override Task.task_params here.
        """
        params = super().task_params
        if self.datasource_name:
            params.update(self.get_datasource())
        if self.remote_connection:
            params.update(self.get_remote_connection())
        return params
