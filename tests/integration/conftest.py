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

"""py.test conftest.py file for package integration test."""

import logging
import os

import pytest

from tests.testing.docker_wrapper import DockerWrapper

logger = logging.getLogger(__name__)


@pytest.fixture(scope="package", autouse=True)
def docker_setup_teardown():
    """Fixture for whole package tests, Set up and teardown docker env.

    Fixture in file named ``conftest.py`` with ``scope=package`` could be auto import in the
    whole package, and with attribute ``autouse=True`` will be auto-use for each test cases.

    .. seealso::
        For more information about conftest.py see:
        https://docs.pytest.org/en/latest/example/simple.html#package-directory-level-fixtures-setups
    """
    if os.environ.get("skip_launch_docker") == "true":
        yield True
    else:
        docker_wrapper = DockerWrapper(
            image="apache/dolphinscheduler-standalone-server:ci",
            container_name="ci-dolphinscheduler-standalone-server",
            environment={
                "API_PYTHON_GATEWAY_ENABLED": "true",
                "MASTER_SERVER_LOAD_PROTECTION_ENABLED": "false",
                "WORKER_SERVER_LOAD_PROTECTION_ENABLED": "false",
            },
        )
        ports = {"25333/tcp": 25333, "12345/tcp": 12345}
        container = docker_wrapper.run_until_log(
            log="Started ServerConnector", tty=True, ports=ports
        )
        assert container is not None
        yield
        container_logs = container.logs()
        logger.info(
            "Finished integration tests run, Container logs: %s",
            container_logs.decode("utf-8"),
        )
        docker_wrapper.remove_container()
