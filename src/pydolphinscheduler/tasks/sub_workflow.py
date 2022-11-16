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

"""Task sub workflow."""

from typing import Dict

from pydolphinscheduler.constants import TaskType
from pydolphinscheduler.core.task import Task
from pydolphinscheduler.exceptions import PyDSWorkflowNotAssignException
from pydolphinscheduler.java_gateway import gateway


class SubWorkflow(Task):
    """Task SubWorkflow object, declare behavior for SubWorkflow task to dolphinscheduler."""

    _task_custom_attr = {"process_definition_code"}

    def __init__(self, name: str, workflow_name: str, *args, **kwargs):
        super().__init__(name, TaskType.SUB_WORKFLOW, *args, **kwargs)
        self.workflow_name = workflow_name

    @property
    def process_definition_code(self) -> str:
        """Get workflow code, a wrapper for :func:`get_workflow_info`.

        We can not change this function name to workflow_code, because it is a keyword used in
        dolphinscheduler itself.
        """
        return self.get_workflow_info(self.workflow_name).get("code")

    def get_workflow_info(self, workflow_name: str) -> Dict:
        """Get workflow info from java gateway, contains workflow id, name, code."""
        if not self.workflow:
            raise PyDSWorkflowNotAssignException(
                "Workflow must be provider for task SubWorkflow."
            )
        return gateway.get_workflow_info(
            self.workflow.user.name,
            self.workflow.project.name,
            workflow_name,
        )
