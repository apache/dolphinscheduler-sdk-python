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

# [start workflow_declare]
"""An example workflow for task pytorch with resource limit."""

from pydolphinscheduler.core.workflow import Workflow
from pydolphinscheduler.tasks.pytorch import Pytorch

with Workflow(
    name="task_pytorch_with_resource_limit_example",
) as workflow:
    # run project with existing environment
    task_existing_env = Pytorch(
        name="task_existing_env",
        script="main.py",
        script_params="--dry-run --no-cuda",
        project_path="https://github.com/pytorch/examples#mnist",
        python_command="/home/anaconda3/envs/pytorch/bin/python3",
        cpu_quota=1,
        memory_max=100,
    )

    workflow.submit()
# [end workflow_declare]
