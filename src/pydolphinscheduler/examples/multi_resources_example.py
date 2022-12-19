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

"""
This example show how to upload file to dolphinscheduler resource center and use them in tasks.

When you want to create a new resource file in resource center, you can add them to ``workflow.resource_list``
use the following code:

.. code-block:: python

    with Workflow(
        name="use_resource_center",
        resource_list=[
            Resource(name="new-name.py", content="print('hello world from resource center')"),
        ],
        ) as workflow:

during the workflow running, the resource file will be created and uploaded to dolphinscheduler resource
center automatically.

If you want to use the resource file in tasks, you can also use ``resource_list`` parameter in task
constructor, just like the following code:

.. code-block:: python

    task_use_resource = Shell(
        name="run_resource",
        command="python new-name.py",
        resource_list=[
            "new-name.py",
        ],
    )

and the resource file will be downloaded to the task runtime working directory which mean you cna execute
them. In this example we run the file ``new-name.py`` like we execute python script in terminal. And we can
also use the resource file already in dolphinscheduler resource center, not only the new we created in
current workflow.
"""

# [start workflow]
from pydolphinscheduler.core import Workflow
from pydolphinscheduler.core.resource import Resource
from pydolphinscheduler.tasks import Shell

dependence = "dependence.py"
main = "main.py"

with Workflow(
    name="multi_resources_example",
    # [start create_new_resources]
    resource_list=[
        Resource(
            name=dependence,
            content="from datetime import datetime\nnow = datetime.now()",
        ),
        Resource(name=main, content="from dependence import now\nprint(now)"),
    ],
    # [end create_new_resources]
) as workflow:
    # [start use_exists_resources]
    task_use_resource = Shell(
        name="use-resource",
        command=f"python {main}",
        resource_list=[
            dependence,
            main,
        ],
    )
    # [end use_exists_resources]

    workflow.run()
# [end workflow]
