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
r"""
A tutorial example set local parameter in pydolphinscheduler.

Method 1:
    task = Shell(..., input_params={"input":"a"}, output_params={"output": "b"})

Method 2:
    task = Shell(...)
    task.add_in("input", "a")
    task.add_out("output", "b")
"""

from pydolphinscheduler.core.parameter import ParameterType
from pydolphinscheduler.core.workflow import Workflow
from pydolphinscheduler.tasks.shell import Shell

with Workflow(name="local_parameter_example", release_state="offline") as workflow:
    # [start parameter example]
    # define a parameter "a", and use it in Shell task
    example1_input_params = Shell(
        name="example1_input_params",
        command="echo ${a}",
        input_params={
            "a": "123",
        },
    )

    # define a parameter "random_value", and pass it to the downstream tasks
    example2_output_params = Shell(
        name="example2_output_params",
        command="""
        val=$(echo $RANDOM)
        echo "#{setValue(random_value=${val})}"
        echo $val
        """,
        output_params={
            "random_value": "",
        },
    )

    # use the parameter "random_value", from upstream tasks
    # we don't need to define input_params again if the parameter is from upstram tasks
    example2_input_params = Shell(
        name="example2_input_params", command="""echo ${random_value}"""
    )

    example2_output_params >> example2_input_params
    # [end parameter example]

    # [start parameter define]
    # Add parameter via task arguments
    task_1 = Shell(
        name="task_1",
        command="echo hello pydolphinscheduler",
        input_params={
            "value_VARCHAR": "abc",
            "value_INTEGER": 123,
            "value_FLOAT": 0.1,
            "value_BOOLEAN": True,
        },
        output_params={
            "value_EMPTY": None,
        },
    )

    # Add parameter via task instance's method
    task_2 = Shell(name="task_2", command="echo hello pydolphinscheduler")

    task_2.add_in("value_VARCHAR", "abc")
    task_2.add_in("value_INTEGER", 123)
    task_2.add_in("value_FLOAT", 0.1)
    task_2.add_in("value_BOOLEAN", True)
    task_2.add_out("value_EMPTY")

    # Task 1 is the same as task 2

    # Others parameter types which cannot be converted automatically, must declare type explicitly
    task_3 = Shell(
        name="task_3",
        command="echo '123' >> test.txt",
        input_params={
            "value_LONG": ParameterType.LONG("1000000"),
            "value_DATE": ParameterType.DATE("2022-01-02"),
            "value_TIME": ParameterType.TIME("2022-01-01"),
            "value_TIMESTAMP": ParameterType.TIMESTAMP(123123124125),
            "value_LIST": ParameterType.LIST("123123"),
        },
        output_params={
            "output_INTEGER": ParameterType.INTEGER(100),
            "output_LIST": ParameterType.LIST(),
            "output_FILE": ParameterType.FILE("test.txt"),
        },
    )

    workflow.submit()
    # [end parameter define]
# [end workflow_declare]
