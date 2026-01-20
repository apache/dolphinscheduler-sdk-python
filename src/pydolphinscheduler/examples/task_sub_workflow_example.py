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

"""A example workflow for task sub workflow."""

# [start tutorial]
# [start package_import]
# Import Workflow object to define your workflow attributes
from pydolphinscheduler.core.workflow import Workflow

# Import task Shell object cause we would create some shell tasks later
from pydolphinscheduler.tasks.sub_workflow import SubWorkflow
from pydolphinscheduler.tasks.shell import Shell

# [start workflow_declare]
# [start sub_workflow_declare]
with Workflow(name="sub_workflow_downstream") as wf_downstream, Workflow(
    name="task_sub_workflow_example"
) as wf_upstream:
    sub_workflow_ds_task = Shell(
        name="task_sub_workflow",
        command="echo 'call sub workflow success!'",
        workflow=wf_downstream,
    )
    wf_downstream.submit()
    # [end sub_workflow_declare]

    sub_workflow_pre = Shell(
        name="pre-task",
        command="echo 'prefix task for sub workflow'",
        workflow=wf_upstream,
    )
    # [start sub_workflow_task_declare]
    sw_task = SubWorkflow(
        name="sub_workflow",
        workflow_name=wf_downstream.name,
        workflow=wf_upstream,
    )
    # [end sub_workflow_task_declare]
    sub_workflow_pre >> sw_task
    # Please make sure workflow with name `wf_downstream.name` exists when we submit or run sub workflow task
    wf_upstream.run()
# [end workflow_declare]
