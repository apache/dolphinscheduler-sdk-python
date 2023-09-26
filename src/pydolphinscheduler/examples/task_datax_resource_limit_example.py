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
"""An example workflow for task datax with resource limit."""


from pydolphinscheduler.core.workflow import Workflow
from pydolphinscheduler.tasks.datax import CustomDataX, DataX

with Workflow(
    name="task_datax_with_resource_limit_example",
) as workflow:
    # This task synchronizes the data in `t_ds_project`
    # of `first_mysql` database to `target_project` of `second_mysql` database.
    # You have to make sure data source named `first_mysql` and `second_mysql` exists
    # in your environment.
    task1 = DataX(
        name="task_datax",
        datasource_name="first_mysql",
        datatarget_name="second_mysql",
        sql="select id, name, code, description from source_table",
        target_table="target_table",
        cpu_quota=1,
        memory_max=100,
    )

    # You can custom json_template of datax to sync data. This task create a new
    # datax job same as task1, transfer record from `first_mysql` to `second_mysql`
    task2 = CustomDataX(name="task_custom_datax", json="json", cpu_quota=1, memory_max=100)
    workflow.run()
# [end workflow_declare]
