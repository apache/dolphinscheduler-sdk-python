.. Licensed to the Apache Software Foundation (ASF) under one
   or more contributor license agreements.  See the NOTICE file
   distributed with this work for additional information
   regarding copyright ownership.  The ASF licenses this file
   to you under the Apache License, Version 2.0 (the
   "License"); you may not use this file except in compliance
   with the License.  You may obtain a copy of the License at

..   http://www.apache.org/licenses/LICENSE-2.0

.. Unless required by applicable law or agreed to in writing,
   software distributed under the License is distributed on an
   "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
   KIND, either express or implied.  See the License for the
   specific language governing permissions and limitations
   under the License.

Shell
=====

A shell task type's example and dive into information of **PyDolphinScheduler**.

Example
-------

.. literalinclude:: ../../../src/pydolphinscheduler/examples/tutorial.py
   :start-after: [start workflow_declare]
   :end-before: [end task_relation_declare]

Resource Limit Example
----------------------

We can add resource limit like CPU quota and max memory by passing parameters when declaring tasks.

.. literalinclude:: ../../../src/pydolphinscheduler/examples/tutorial.py
   :start-after: [start resource_limit]
   :end-before: [end resource_limit]

Dive Into
---------

.. automodule:: pydolphinscheduler.tasks.shell


YAML file example
-----------------

.. literalinclude:: ../../../examples/yaml_define/Shell.yaml
   :start-after: # under the License.
   :language: yaml
