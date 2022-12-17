<!--
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
-->

# UPDATING

Updating is try to document non-backward compatible updates which notice users the detail changes about pydolphinscheduler.
It started after version 2.0.5 released

## Main

* Remove attribute tenant from pydolphinscheduler.core.workflow.workflow ([#54](https://github.com/apache/dolphinscheduler-sdk-python/pull/54))
  and please change tenant name in ``config.yaml`` in ``PYDS_HOME``

## 4.0.0

* Change Task attr ``timeout`` type from int to timedelta and use timeout determine attr ``timeout_flag`` value ([#41](https://github.com/apache/dolphinscheduler-sdk-python/pull/41)) 
* Remove the spark version of spark task ([#11860](https://github.com/apache/dolphinscheduler/pull/11860)).
* Change class name from process definition to workflow ([#26](https://github.com/apache/dolphinscheduler-sdk-python/pull/26))
  * Deprecated class `ProcessDefinition` to `Workflow`
  * Deprecated class `SubProcess` to `SubWorkflow`, and change parameter name from `process_definition_name` to `workflow_name`
  * Deprecated class `Dependent` parameter from `process_definition_name` to `workflow_name`
  * And all above deprecated will be remove in version 4.1.0

## 3.1.0

* Remove parameter ``task_location`` in process definition and Java Gateway service ([#11681](https://github.com/apache/dolphinscheduler/pull/11681))

## 3.0.0

* Integrate Python gateway server into Dolphinscheduler API server, and you could start Python gateway service by command
  `./bin/dolphinscheduler-daemon.sh start api-server` instead of independent command
  `./bin/dolphinscheduler-daemon.sh start python-gateway-server`.
* Remove parameter `queue` from class `ProcessDefinition` to avoid confuse user when it change but not work
* Change `yaml_parser.py` method `to_string` to magic method `__str__` make it more pythonic.
* Use package ``ruamel.yaml`` replace ``pyyaml`` for write yaml file with comment.
* Change variable about where to keep pydolphinscheduler configuration from ``PYDOLPHINSCHEDULER_HOME`` to
  ``PYDS_HOME`` which is same as other environment variable name.

