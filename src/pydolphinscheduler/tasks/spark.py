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

"""Task Spark."""

from __future__ import annotations

from pydolphinscheduler.constants import TaskType
from pydolphinscheduler.core.engine import Engine, ProgramType


class DeployMode(str):
    """SPARK deploy mode, for now it just contain `LOCAL`, `CLIENT` and `CLUSTER`."""

    LOCAL = "local"
    CLIENT = "client"
    CLUSTER = "cluster"


class Spark(Engine):
    """Task spark object, declare behavior for spark task to dolphinscheduler."""

    _task_custom_attr = {
        "deploy_mode",
        "driver_cores",
        "driver_memory",
        "num_executors",
        "executor_memory",
        "executor_cores",
        "app_name",
        "main_args",
        "others",
    }

    def __init__(
        self,
        name: str,
        main_class: str,
        main_package: str,
        program_type: ProgramType | None = ProgramType.SCALA,
        deploy_mode: DeployMode | None = DeployMode.CLUSTER,
        app_name: str | None = None,
        driver_cores: int | None = 1,
        driver_memory: str | None = "512M",
        num_executors: int | None = 2,
        executor_memory: str | None = "2G",
        executor_cores: int | None = 2,
        main_args: str | None = None,
        others: str | None = None,
        *args,
        **kwargs
    ):
        super().__init__(
            name,
            TaskType.SPARK,
            main_class,
            main_package,
            program_type,
            *args,
            **kwargs
        )
        self.deploy_mode = deploy_mode
        self.app_name = app_name
        self.driver_cores = driver_cores
        self.driver_memory = driver_memory
        self.num_executors = num_executors
        self.executor_memory = executor_memory
        self.executor_cores = executor_cores
        self.main_args = main_args
        self.others = others
