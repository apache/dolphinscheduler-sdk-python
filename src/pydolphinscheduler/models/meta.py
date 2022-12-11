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

"""Metadata class for module models.

This module contains the ModelMeta class, which is used to convert ``py4j.java_gateway.JavaObject`` to
``pydolphinscheduler.models`` object. this is useful when you communicate with the DolphinScheduler
server to get some resource from database, but you want to make sure the return object is a in Python
object.
"""

from functools import wraps
from inspect import signature
from typing import Dict, Tuple

from py4j.java_gateway import JavaObject

from pydolphinscheduler.utils.string import snake2camel


class ModelMeta(type):
    """Mateclass convert ``py4j.java_gateway.JavaObject`` to python object more easily."""

    _FUNC_INIT = "__init__"
    _PARAM_SELF = "self"

    def __new__(mcs, name: str, bases: Tuple, attrs: Dict):
        """Create a new class."""
        if mcs._FUNC_INIT not in attrs:
            raise TypeError(
                "Class with mateclass %s must have %s method",
                (mcs.__name__, mcs._FUNC_INIT),
            )

        sig = signature(attrs.get(mcs._FUNC_INIT))
        param = [
            param.name
            for name, param in sig.parameters.items()
            if name != mcs._PARAM_SELF
        ]

        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, classmethod) and not attr_name.startswith("__"):
                attrs[attr_name] = mcs.j2p(attr_value, name, attrs, param)
        return super(ModelMeta, mcs).__new__(mcs, name, bases, attrs)

    @classmethod
    def j2p(mcs, cm: classmethod, name: str, attrs: Dict, params=None):
        """Convert JavaObject to Python object according attribute in the ``__init__`` method.

        ``py4j.java_gateway.JavaObject`` return the Java object from the DolphinScheduler server, we can
        access the Java object attribute by ``getAttrName`` method. This method try to assign the Java object
        attribute to the Python object attribute according the attribute in python ``__init__`` method.

        For example, If the method return value is ``py4j.java_gateway.JavaObject`` we temporary call it
        ``JObject``, and we create a ``PObject`` object in Python, the ``__init__`` method is:

        .. code-block:: python

            def __init__(
                self,
                name: str,
                description: str
            ):
                self.name = name
                self.description = description

        Because the ``name`` and ``description`` is the attribute in the ``__init__`` method, so this method
        will try to call method ``getName`` and ``getDescription`` from the ``JObject`` and assign the return
        value to the ``PObject`` attribute. Just like this:

        .. code-block:: python

            return PObject(name=JObject.getName(), description=JObject.getDescription())
        """

        @wraps(cm)
        def wrapper(*args, **kwargs):
            class_ = type(name, (), attrs)

            method_result = cm.__func__(class_, *args, **kwargs)

            # skip convert if method result is not JavaObject, they maybe some property method
            if not isinstance(method_result, JavaObject):
                return method_result

            obj_init_params = []
            for param in params:
                java_func_name = mcs.py4j_attr_func_name(param)
                java_func = getattr(method_result, java_func_name)
                obj_init_params.append(java_func())

            return class_(*obj_init_params)

        return wrapper

    @classmethod
    def py4j_attr_func_name(mcs, name: str) -> str:
        """Convert python attribute name to py4j java attribute name.

        Python attribute name is snake case, but py4j java attribute name is camel case. This method
        will convert snake case to camel case with adding the ``get`` prefix. for example:

        - attr -> getAttr
        - attr_name -> getAttrName
        - attr_ -> getAttr
        """
        return snake2camel(f"get_{name}")
