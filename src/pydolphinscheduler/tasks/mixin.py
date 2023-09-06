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

    :param min_cpu_cores: min CPU requirement for running Kubernetes task.
    :param min_memory_space: min memory requirement for running Kubernetes task.
    """

    _mixin_attr = {
        "min_cpu_cores",
        "min_memory_space",
    }

    def add_attr(
        self, 
        min_cpu_cores: float, 
        min_memory_space: float
    ):
        self.min_cpu_cores = min_cpu_cores
        self.min_memory_space = min_memory_space