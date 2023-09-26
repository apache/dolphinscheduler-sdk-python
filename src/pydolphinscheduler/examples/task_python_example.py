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
"""An example workflow for task python."""

from pydolphinscheduler.core.workflow import Workflow
from pydolphinscheduler.tasks.python import Python

with Workflow(
    name="task_python_example",
) as workflow:
    task_python = Python(
        name="task", 
        definition="print('hello world.')",
    )
    workflow.submit()
# [end workflow_declare]