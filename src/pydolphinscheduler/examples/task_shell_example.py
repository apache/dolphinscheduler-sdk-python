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

r"""
A tutorial example take you to experience pydolphinscheduler.

After tutorial.py file submit to Apache DolphinScheduler server a DAG would be create,
and workflow DAG graph as below:

                  --> task_child_one
                /                    \
task_parent -->                        -->  task_union
                \                    /
                  --> task_child_two

it will instantiate and run all the task it have.
"""

# [start tutorial]
# [start package_import]
# Import Workflow object to define your workflow attributes
from pydolphinscheduler.core.workflow import Workflow

# Import task Shell object cause we would create some shell tasks later
from pydolphinscheduler.tasks.shell import Shell

# [start workflow_declare]
with Workflow(
    name="task_shell",
    schedule="0 0 0 * * ? *",
    start_time="2021-01-01",
) as workflow:
    # [end workflow_declare]
    simple = Shell(name="simple", command="echo simple")

    datasource_source = Shell(
        name="datasource_source",
        command="""
        echo "${getConnectionHost('mysql-meta')}"
        echo "${getConnectionUsername('mysql-target')}"
        """,
        datasource_name=[
            "mysql-meta",
            "mysql-target",
        ],
    )

    remote_connection = Shell(
        name="remote_connection",
        command="ls /tmp",
        remote_connection="remote-ssh-ws3",
    )

    mixin = Shell(
        name="mixin",
        command="""
            echo "${getConnectionHost('mysql-meta')}"
            echo "${getConnectionUsername('mysql-target')}"
            """,
        remote_connection="remote-ssh-ws3",
        datasource_name=[
            "mysql-meta",
            "mysql-target",
        ],
    )

    simple >> datasource_source >> remote_connection >> mixin

    # [start submit_or_run]
    workflow.submit()
