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

"""The script for setting up pydolphinscheduler."""
import logging
import os
import sys
from distutils.command.sdist import sdist
from distutils.dir_util import remove_tree
from distutils.errors import DistutilsExecError
from typing import List

from setuptools import Command, setup

if sys.version_info[0] < 3:
    raise Exception(
        "pydolphinscheduler does not support Python 2. Please upgrade to Python 3."
    )

logger = logging.getLogger(__name__)


class CleanCommand(Command):
    """Command to clean up python api before setup by running `python setup.py clean`."""

    description = "Clean up project root"
    user_options: List[str] = []
    clean_list = [
        "build",
        "htmlcov",
        "dist",
        ".pytest_cache",
        ".coverage",
    ]

    def initialize_options(self) -> None:
        """Set default values for options."""

    def finalize_options(self) -> None:
        """Set final values for options."""

    def run(self) -> None:
        """Run and remove temporary files."""
        for cl in self.clean_list:
            if not os.path.exists(cl):
                logger.info("Path %s do not exists.", cl)
            elif os.path.isdir(cl):
                remove_tree(cl)
            else:
                os.remove(cl)
        logger.info("Finish clean process.")


class ApacheRelease(sdist):
    """Command to make Apache release by running `python setup.py sdist`.

    This command will make a tarball and also sign the tarball with gpg and sha512.
    """

    def run(self):
        """Run and build tarball and sign."""
        super().run()
        version = self.distribution.metadata.get_version()
        target_name = f"dolphinscheduler-python-src-{version}.tar.gz"
        try:
            os.system(
                f"cd dist && "
                f"mv apache-dolphinscheduler-{version}.tar.gz {target_name} && "
                f"gpg --batch --yes --armor --detach-sig {target_name} && "
                f"shasum -a 512 {target_name} > {target_name}.sha512"
            )
        except DistutilsExecError as e:
            self.warn("Make dist and sign failed: %s" % e)


setup(
    cmdclass={
        "clean": CleanCommand,
        "asdist": ApacheRelease,
    },
)
