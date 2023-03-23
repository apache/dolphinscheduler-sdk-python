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

"""Module database."""
import json
import re
from typing import NamedTuple, Optional

from py4j.java_gateway import JavaObject

from pydolphinscheduler.java_gateway import gateway
from pydolphinscheduler.models.connection import Connection
from pydolphinscheduler.models.meta import ModelMeta


class TaskUsage(NamedTuple):
    """Class for task usage just like datasource in web ui."""

    id: int
    type: str


class Datasource(metaclass=ModelMeta):
    """Model datasource, communicate with DolphinScheduler API server and convert Java Object into Python.

    We use metaclass :class:`pydolphinscheduler.models.meta.ModelMeta` to convert Java Object into Python.
    And code in this class just call Java API method.

    You provider database_name contain connection information, it decisions which
    database type and database instance would run task.

    :param id_: datasource id, the primary key of table t_ds_datasource.
    :param name: datasource name, part of unique key (:param:``type_``, :param:``name``) for datasource
        object, we support both query the datasource by name or by (type_ + name). But name must be required
        unique when you want to query with the name only.
    :param note: datasource description. A note for current datasource.
    :param type_: datasource type, part of unique key (:param:``type_``, :param:``name``) for datasource.
        It is a datasource type code instead of datasource type name. Optional when you query datasource by
        name only. But it must be required when you create it.
    :param user_id: user id for who create this datasource.
    :param connection_params: datasource connection detail, including protocol, host, port, schema etc.
        In json format and just like this:

        .. code-block:: json

            {
                "user": "root",
                "password": "mysql",
                "address": "jdbc:mysql://127.0.0.1:3306",
                "database": "test",
                "jdbcUrl": "jdbc:mysql://127.0.0.1:3306/test",
                "driverClassName": "com.mysql.cj.jdbc.Driver",
                "validationQuery": "select 1"
            }

    """

    _PATTERN = re.compile("jdbc:.*://(?P<host>[\\w\\W]+):(?P<port>\\d+)")

    _DATABASE_TYPE_MAP = dict(
        mysql=0,
        postgresql=1,
        hive=2,
        spark=3,
        clickhouse=4,
        oracle=5,
        sqlserver=6,
        db2=7,
        presto=8,
        h2=9,
        redshift=10,
        dameng=11,
        starrocks=12,
    )

    def __init__(
        self,
        type_: str,
        name: str,
        connection_params: str,
        user_id: Optional[int] = None,
        id_: Optional[int] = None,
        note: Optional[str] = None,
    ):
        self.id = id_
        self.name = name
        self.note = note
        # TODO try to handle type_ in metaclass
        self.type_: JavaObject = type_
        self.user_id = user_id
        self.connection_params = connection_params

    @classmethod
    def get(
        cls, datasource_name: str, datasource_type: Optional[str] = None
    ) -> "Datasource":
        """Get single datasource.

        :param datasource_name: datasource name
        :param datasource_type: datasource type, if not provided, will get datasource by name only
        """
        datasource = gateway.get_datasource(datasource_name, datasource_type)
        if datasource is None:
            raise ValueError(
                f"Datasource with name: {datasource_name} and type: {datasource_type} not found."
            )
        return datasource

    @classmethod
    def get_task_usage_4j(
        cls, datasource_name: str, datasource_type: Optional[str] = None
    ) -> TaskUsage:
        """Get the necessary information of datasource for task usage in web UI."""
        datasource: "Datasource" = cls.get(datasource_name, datasource_type)
        return TaskUsage(
            id=datasource.id,
            type=datasource.type.upper(),
        )

    @property
    def connection(self) -> Connection:
        """Parse dolphinscheduler connection_params to Connection."""
        data = json.loads(self.connection_params)

        address_match = self._PATTERN.match(data.get("jdbcUrl", None)).groupdict()

        return Connection(
            host=address_match.get("host", None),
            port=int(address_match.get("port", None)),
            schema=data.get("database", None),
            username=data.get("user", None),
            password=data.get("password", None),
        )

    @property
    def type(self) -> str:
        """Property datasource type."""
        return self.type_.getDescp()

    @property
    def type_code(self) -> str:
        """Property datasource type."""
        return self.type_.getCode()

    @property
    def host(self) -> str:
        """Property datasource host, such as ``127.0.0.1`` or ``localhosts``."""
        return self.connection.host

    @property
    def port(self) -> int:
        """Property datasource host, such as ``3306`` or ``5432``."""
        return int(self.connection.port)

    @property
    def username(self) -> str:
        """Property datasource username, such as ``root`` or ``postgres``."""
        return self.connection.username

    @property
    def password(self) -> str:
        """Property datasource password."""
        return self.connection.password

    @property
    def schema(self) -> str:
        """Property datasource schema."""
        return self.connection.schema
