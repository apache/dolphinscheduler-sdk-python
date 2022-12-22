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

"""Task function wrapper allows using decorator to create a task."""

import functools
import inspect
import types
from pathlib import Path

from stmdency.extractor import Extractor

from pydolphinscheduler.exceptions import PyDSParamException
from pydolphinscheduler.tasks.python import Python


def _exists_other_decorator(func: types.FunctionType) -> None:
    """Check if the function has other decorators except @task.

    :param func: The function which wraps by decorator ``@task``.
    """
    lines = inspect.getsourcelines(func)[0]

    for line in lines:
        strip_line = line.strip()
        if strip_line.startswith("@") and not strip_line == "@task":
            raise PyDSParamException(
                "Do no support other decorators for function ``task`` decorator."
            )


def task(func: types.FunctionType):
    """Decorate which covert Python functions into pydolphinscheduler task.

    :param func: The function which wraps by decorator ``@task``.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        _exists_other_decorator(func)
        loc = func.__code__.co_filename
        extractor = Extractor(Path(loc).open("r").read())
        stm = extractor.get_code(func.__name__)
        return Python(
            name=kwargs.get("name", func.__name__),
            definition=f"{stm}{func.__name__}()",
            *args,
            **kwargs,
        )

    return wrapper
