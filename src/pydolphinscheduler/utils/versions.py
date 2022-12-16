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

"""Util versions."""

from pathlib import Path

from packaging import requirements
from packaging.version import InvalidVersion
from pkg_resources import parse_requirements

from pydolphinscheduler.constants import Version


def version_match(name: str, version: str) -> bool:
    """Check if the version of external system matches current python sdk version.

    :param name: External system name in file ``Version.FILE_NAME``
    :param version: External system current version
    """
    path = Path(__file__).parent.parent.joinpath(Version.FILE_NAME)
    with path.open() as match:
        content = match.read()
        for reqs in parse_requirements(content):
            if reqs.name == name:
                try:
                    return requirements.Requirement(str(reqs)).specifier.contains(
                        version
                    )
                except InvalidVersion:
                    return False
        raise ValueError("%s is not in %s" % (name, Version.FILE_NAME))
