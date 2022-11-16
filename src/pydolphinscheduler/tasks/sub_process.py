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

"""This module is deprecated. Please use `pydolphinscheduler.tasks.sub_workflow.SubWorkflow`."""

import warnings

from pydolphinscheduler.tasks.sub_workflow import SubWorkflow

warnings.warn(
    "This module is deprecated and will be remove in 4.1.0. "
    "Please use `pydolphinscheduler.tasks.sub_workflow.SubWorkflow` instead.",
    DeprecationWarning,
    stacklevel=2,
)


class SubProcess(SubWorkflow):
    """Task SubProcess object, declare behavior for SubProcess task to dolphinscheduler.

    This module is deprecated and will be remove in 4.1.0. Please use
    `pydolphinscheduler.tasks.sub_workflow.SubWorkflow` instead.
    """

    def __init__(self, name: str, process_definition_name: str, *args, **kwargs):
        super().__init__(
            name=name, workflow_name=process_definition_name, *args, **kwargs
        )
