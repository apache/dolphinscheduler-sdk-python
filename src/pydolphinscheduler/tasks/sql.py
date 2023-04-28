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

"""Task sql."""

import logging
import re
import warnings
from typing import Dict, List, Optional, Sequence, Union

from pydolphinscheduler.constants import TaskType
from pydolphinscheduler.core.task import Task
from pydolphinscheduler.models.datasource import Datasource

log = logging.getLogger(__file__)


class SqlType:
    """SQL type, for now it just contain `SELECT` and `NO_SELECT`."""

    SELECT = "0"
    NOT_SELECT = "1"


class Sql(Task):
    """Task SQL object, declare behavior for SQL task to dolphinscheduler.

    It should run sql job in multiply sql lik engine, such as:
    - ClickHouse
    - DB2
    - HIVE
    - MySQL
    - Oracle
    - Postgresql
    - Presto
    - SQLServer
    You provider datasource_name contain connection information, it decisions which
    database type and database instance would run this sql.

    :param name: SQL task name
    :param datasource_name: datasource name in dolphinscheduler, the name must exists and must be ``online``
        datasource instead of ``test``.
    :param sql: SQL statement, the sql script you want to run. Support resource plugin in this parameter.
    :param sql_type: SQL type, whether sql statement is select query or not. If not provided, it will be auto
        detected according to sql statement using :func:`pydolphinscheduler.tasks.sql.Sql.sql_type`, and you
        can also set it manually. by ``SqlType.SELECT`` for query statement or ``SqlType.NOT_SELECT`` for not
        query statement.
    :param sql_delimiter: SQL delimiter to split one sql statement into multiple statements, ONLY support in
        ``sql_type=SqlType.NOT_SELECT``, default is None.
    :param pre_statements: SQL statements to be executed before the main SQL statement.
    :param post_statements: SQL statements to be executed after the main SQL statement.
    :param display_rows: The number of record rows number to be displayed in the SQL task log, default is 10.
    """

    _task_custom_attr = {
        "sql",
        "sql_type",
        "segment_separator",
        "pre_statements",
        "post_statements",
        "display_rows",
    }

    ext: set = {".sql"}
    ext_attr: str = "_sql"

    def __init__(
        self,
        name: str,
        datasource_name: str,
        sql: str,
        datasource_type: Optional[str] = None,
        sql_type: Optional[str] = None,
        sql_delimiter: Optional[str] = None,
        pre_statements: Union[str, Sequence[str], None] = None,
        post_statements: Union[str, Sequence[str], None] = None,
        display_rows: Optional[int] = 10,
        *args,
        **kwargs
    ):
        self._sql = sql
        super().__init__(name, TaskType.SQL, *args, **kwargs)
        self.param_sql_type = sql_type
        if sql_type == SqlType.SELECT and sql_delimiter:
            warnings.warn(
                "Parameter `sql_delimiter` is only supported in `sql_type=SqlType.NO_SELECT`, but current "
                "sql_type is `sql_type=SqlType.SELECT`, so `sql_delimiter` will be ignored.",
                UserWarning,
                stacklevel=2,
            )
        self.segment_separator = sql_delimiter or ""
        self.datasource_name = datasource_name
        self.datasource_type = datasource_type
        self.pre_statements = self.get_stm_list(pre_statements)
        self.post_statements = self.get_stm_list(post_statements)
        self.display_rows = display_rows

    @staticmethod
    def get_stm_list(stm: Union[str, Sequence[str]]) -> List[str]:
        """Convert statement to str of list.

        :param stm: statements string
        :return: statements list
        """
        if not stm:
            return []
        elif isinstance(stm, str):
            return [stm]
        return list(stm)

    @property
    def sql_type(self) -> str:
        """Judgement sql type, it will return the SQL type for type `SELECT` or `NOT_SELECT`.

        If `param_sql_type` dot not specific, will use regexp to check
        which type of the SQL is. But if `param_sql_type` is specific
        will use the parameter overwrites the regexp way
        """
        if (
            self.param_sql_type == SqlType.SELECT
            or self.param_sql_type == SqlType.NOT_SELECT
        ):
            log.info(
                "The sql type is specified by a parameter, with value %s",
                self.param_sql_type,
            )
            return self.param_sql_type
        pattern_select_str = (
            "^(?!(.* |)insert |(.* |)delete |(.* |)drop "
            "|(.* |)update |(.* |)truncate |(.* |)alter |(.* |)create ).*"
        )
        pattern_select = re.compile(pattern_select_str, re.IGNORECASE)
        if pattern_select.match(self._sql) is None:
            return SqlType.NOT_SELECT
        else:
            return SqlType.SELECT

    @property
    def datasource(self) -> Dict:
        """Get datasource for procedure sql."""
        datasource_task_u = Datasource.get_task_usage_4j(
            self.datasource_name, self.datasource_type
        )
        return {
            "datasource": datasource_task_u.id,
            "type": datasource_task_u.type,
        }

    @property
    def task_params(self, camel_attr: bool = True, custom_attr: set = None) -> Dict:
        """Override Task.task_params for sql task.

        sql task have some specials attribute for task_params, and is odd if we
        directly set as python property, so we Override Task.task_params here.
        """
        params = super().task_params
        params.update(self.datasource)
        return params
