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

"""A example workflow for task SQL."""
from pathlib import Path

from pydolphinscheduler.core.workflow import Workflow
from pydolphinscheduler.resources_plugin import Local
from pydolphinscheduler.tasks.sql import Sql, SqlType

with Workflow(
    name="task_sql_example",
) as workflow:
    # [start bare_sql_desc]
    bare_sql = Sql(
        name="bare_sql",
        datasource_name="metadata",
        sql="select * from t_ds_version",
    )
    # [end bare_sql_desc]
    # [start sql_file_desc]
    sql_file = Sql(
        name="sql_file",
        datasource_name="metadata",
        sql="ext/example.sql",
        sql_type=SqlType.SELECT,
        resource_plugin=Local(prefix=str(Path(__file__).parent)),
    )
    # [end sql_file_desc]
    # [start sql_with_pre_post_desc]
    sql_with_pre_post = Sql(
        name="sql_with_pre_post",
        datasource_name="metadata",
        sql="select * from t_ds_version",
        pre_statements=[
            "update table_one set version = '1.3.6'",
            "delete from table_two where version = '1.3.6'",
        ],
        post_statements="update table_one set version = '3.0.0'",
    )
    # [end sql_with_pre_post_desc]

    bare_sql >> [
        sql_file,
        sql_with_pre_post,
    ]

    workflow.submit()

# [end workflow_declare]
