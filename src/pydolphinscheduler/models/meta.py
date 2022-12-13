from functools import wraps
from inspect import signature
from typing import Tuple, Dict

from py4j.java_gateway import JavaObject
from pydolphinscheduler.utils.string import snake2camel


class ModelMeta(type):
    _FUNC_INIT = "__init__"
    _PARAM_SELF = "self"

    def __new__(mcs, name: str, bases: Tuple, attrs: Dict):

        if mcs._FUNC_INIT not in attrs:
            raise TypeError("Class with mateclass %s must have %s method", (mcs.__name__, mcs._FUNC_INIT))

        sig = signature(attrs.get(mcs._FUNC_INIT))
        param = [param.name for name, param in sig.parameters.items() if name != mcs._PARAM_SELF]

        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, classmethod) and not attr_name.startswith("__"):
                attrs[attr_name] = mcs.j2p(attr_value, name, attrs, param)
        return super(ModelMeta, mcs).__new__(mcs, name, bases, attrs)

    @classmethod
    def j2p(mcs, cm: classmethod, name: str, attrs: Dict, params=None):
        @wraps(cm)
        def wrapper(*args, **kwargs):
            class_ = type(name, (), attrs)

            java_obj = cm.__func__(class_, *args, **kwargs)
            assert isinstance(java_obj, JavaObject), "The function %s must return JavaObject" % cm.__func__.__name__

            obj_init_params = []
            for param in params:
                java_func_name = mcs.py4j_attr_func_name(param)
                java_func = getattr(java_obj, java_func_name)
                obj_init_params.append(java_func())

            return class_(*obj_init_params)

        return wrapper

    @classmethod
    def py4j_attr_func_name(mcs, name: str) -> str:
        return snake2camel(f"get_{name}")
