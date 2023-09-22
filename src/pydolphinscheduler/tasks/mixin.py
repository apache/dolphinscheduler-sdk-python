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

"""Task Kubernetes Mixin"""
class KubernetesMixin():
    """KubernetesMixin object, declare some attributes for Kubernetes task.
    """

    def add_attr(
        self, 
        **kwargs
    ):
        self.min_cpu_cores = kwargs.get("min_cpu_cores", None) 
        self.min_memory_space = kwargs.get("min_memory_space", None) 
        if hasattr(self, "_task_custom_attr"): 
            self._task_custom_attr |= { "min_cpu_cores", "min_memory_space"}

"""Task Shell Mixin"""
class ShellMixin():
    """ShellMixin object, declare some attributes for Shell task.
    """

    def add_attr(
        self, 
        **kwargs
    ):
        self._raw_script = kwargs.get("command", None) 
        assert self._raw_script != None
        if hasattr(self, "_task_custom_attr"): 
            self._task_custom_attr |= { "_raw_script"}