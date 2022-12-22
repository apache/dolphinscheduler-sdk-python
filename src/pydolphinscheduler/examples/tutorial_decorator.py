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

import time

# [start tutorial]
# [start package_import]
# Import Workflow object to define your workflow attributes
from pydolphinscheduler.core.workflow import Workflow

# Import task Shell object cause we would create some shell tasks later
from pydolphinscheduler.tasks.func_wrap import task

# [end package_import]

scope_global = "global-var"


# [start task_declare]
@task
def print_something():
    """First task in this workflow."""
    print("hello python function wrap task")


@task
def depend_import():
    """Depend on import module."""
    time.sleep(2)


@task
def depend_global_var():
    """Depend on global var."""
    print(f"Use global variable {scope_global}")


@task
def depend_local_var():
    """Depend on local variable."""
    scope_global = "local"
    print(f"Use local variable overwrite global {scope_global}")


def foo():
    """Call in other task."""
    print("this is a global function")


@task
def depend_func():
    """Depend on global function."""
    foo()


# [end task_declare]


# [start workflow_declare]
with Workflow(
    name="tutorial_decorator",
    schedule="0 0 0 * * ? *",
    start_time="2021-01-01",
) as workflow:
    # [end workflow_declare]

    # [start task_relation_declare]
    task_group = [depend_import(), depend_global_var()]
    print_something().set_downstream(task_group)

    task_group >> depend_local_var() >> depend_func()
    # [end task_relation_declare]

    # [start submit_or_run]
    workflow.submit()
    # [end submit_or_run]
# [end tutorial]
