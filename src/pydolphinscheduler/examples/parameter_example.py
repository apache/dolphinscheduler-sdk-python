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

from pprint import pprint

from pydolphinscheduler.core.parameter import ParameterType

# [start tutorial]
# [start package_import]
# Import Workflow object to define your workflow attributes
from pydolphinscheduler.core.workflow import Workflow

# Import task Shell object cause we would create some shell tasks later
from pydolphinscheduler.tasks.shell import Shell

# [end package_import]

# [start workflow_declare]
with Workflow(
    name="tutorial",
) as workflow:
    task = Shell(
        name="task_parent",
        command="echo hello pydolphinscheduler",
        input_params={
            "value_VARCHAR": "abc",
            "value_LONG": ParameterType.LONG("1000000"),
            "value_INTEGER": 123,
            "value_FLOAT": 0.1,
            "value_DATE": ParameterType.DATE("2022-01-02"),
            "value_TIME": ParameterType.TIME("2022-01-01"),
            "value_TIMESTAMP": ParameterType.TIMESTAMP(123123124125),
            "value_BOOLEAN": True,
            "value_LIST": ParameterType.LIST("123123"),
        },
        output_params={
            "output_INTEGER": ParameterType.INTEGER(100),
            "output_LIST": ParameterType.LIST(),
        },
    )
    pprint(task.local_params)

    workflow.submit()
    # VARCHAR = create_data_type("VARCHAR", str)
    # LONG = create_data_type("LONG")
    # INTEGER = create_data_type("INTERGER", int)
    # FLOAT = create_data_type("FLOAT", float)
    # DOUBLE = create_data_type("DOUBLE")
    # DATE = create_data_type("DATE")
    # TIME = create_data_type("TIME")
    # TIMESTAMP = create_data_type("TIMESTAMP")
    # BOOLEAN = create_data_type("BOOLEAN")
    # LIST = create_data_type("LIST")
    # FILE = create_data_type("FILE")
