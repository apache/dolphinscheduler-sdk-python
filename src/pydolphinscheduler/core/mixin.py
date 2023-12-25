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

"""WorkerResource Mixin."""


class WorkerResourceMixin:
    """Mixin object, declare some attributes for WorkerResource."""

    def add_attr(self, **kwargs):
        """Add attributes to WorkerResource, include cpu_quota and memory_max now."""
        self._cpu_quota = kwargs.get("cpu_quota", -1)
        self._memory_max = kwargs.get("memory_max", -1)
        if hasattr(self, "_DEFINE_ATTR"):
            self._DEFINE_ATTR |= {"cpu_quota", "memory_max"}

    @property
    def cpu_quota(self):
        """Get cpu_quota."""
        return self._cpu_quota

    @property
    def memory_max(self):
        """Get memory_max."""
        return self._memory_max
