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

"""DolphinScheduler parameter object."""

from pydolphinscheduler.exceptions import PyDSParamException


class Direction:
    """Constants for direction."""

    IN = "IN"
    OUT = "OUT"


class BaseDataType:
    """Base data type.

    Use to convert value to ParameterType
    """

    def __init__(self, value=None):
        self.data_type = self.__class__.__name__
        self.value = self.convert_value(value) if value is not None else ""

    def convert_value(self, value=None):
        """Convert value."""
        if value is None or value == "":
            return ""
        else:
            return self._convert(value)

    def _convert(self, value=None):
        return str(value)

    def __eq__(self, data):
        return (
            type(self) is type(data)
            and self.data_type == data.data_type
            and self.value == data.value
        )


def create_data_type(class_name, convert_func=None):
    """Create ParameterType and set the convert_func."""
    convert = convert_func or BaseDataType._convert
    return type(class_name, (BaseDataType,), {"_convert": convert})


class ParameterType:
    """ParameterType corresponds to dolphinscheduler."""

    VARCHAR = create_data_type("VARCHAR", str)
    LONG = create_data_type("LONG")
    INTEGER = create_data_type("INTEGER", int)
    FLOAT = create_data_type("FLOAT", float)
    DOUBLE = create_data_type("DOUBLE")
    DATE = create_data_type("DATE")
    TIME = create_data_type("TIME")
    TIMESTAMP = create_data_type("TIMESTAMP")
    BOOLEAN = create_data_type("BOOLEAN", bool)
    LIST = create_data_type("LIST")
    FILE = create_data_type("FILE")

    type_sets = {
        key: value for key, value in locals().items() if not key.startswith("_")
    }

    _TYPE_MAPPING = {
        "int": INTEGER,
        "float": FLOAT,
        "ScalarFloat": FLOAT,
        "str": VARCHAR,
        "bool": BOOLEAN,
        "NoneType": VARCHAR,
    }


class Parameter:
    """Parameter."""

    def __init__(self, name, direction, data_type, value=None):
        self.name = name
        self.direction = direction
        self.data_type = data_type
        self.value = value or ""

    @property
    def data(self):
        """Convert to local_params in task define."""
        return {
            "prop": self.name,
            "direct": self.direction,
            "type": self.data_type,
            "value": self.value,
        }


class ParameterHelper:
    """Use for task to handle parameters."""

    @staticmethod
    def convert_params(params, direction):
        """Convert params to format local_params.

        :param params: dict[str, Any], the input_params or output_params of Task.
        :param direction: [Direction.IN | Direction.OUT], direction of parameter.
        """
        parameters = []
        params = params or {}
        if not isinstance(params, dict):
            raise PyDSParamException("input_params must be a dict")
        for key, value in params.items():
            if not isinstance(value, BaseDataType):
                data_type_cls = ParameterHelper.infer_parameter_type(value)
                value = data_type_cls(value)

            parameter = Parameter(key, direction, value.data_type, value.value)
            parameters.append(parameter)
        return [p.data for p in parameters]

    @staticmethod
    def infer_parameter_type(value):
        """Infer to ParameterType from the input value."""
        value_type = type(value).__name__

        if value_type not in ParameterType._TYPE_MAPPING:
            raise PyDSParamException(
                f"Can not infer parameter type {value}, please use ParameterType"
            )

        data_type_cls = ParameterType._TYPE_MAPPING[value_type]
        return data_type_cls
