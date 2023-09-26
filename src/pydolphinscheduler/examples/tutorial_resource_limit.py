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
"""An example workflow for task shell with resoure limit."""

from pydolphinscheduler.core.workflow import Workflow
from pydolphinscheduler.tasks.shell import Shell

with Workflow(
    name="task_shell_with_resourceexample",
) as workflow:
    task_shell = Shell(
        name="task", 
        command="echo resource limit",
        cpu_quota=1,
        memory_max=100,
    )
    workflow.submit()
# [end workflow_declare]