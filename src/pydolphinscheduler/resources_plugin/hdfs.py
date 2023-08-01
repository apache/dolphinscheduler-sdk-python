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

"""DolphinScheduler HDFS resource plugin."""

from typing import Optional
from urllib.parse import urljoin

from hdfs import InsecureClient

from pydolphinscheduler.constants import Symbol
from pydolphinscheduler.core.resource_plugin import ResourcePlugin
from pydolphinscheduler.resources_plugin.base.bucket import Bucket, HDFSFileInfo


class HDFS(ResourcePlugin, Bucket):
    """HDFS object, declare HDFS resource plugin for task and workflow to dolphinscheduler.

    :param prefix: A string representing the prefix of HDFS.
    :param hdfs_uri: A string representing the URI of HDFS, e.g., 'hdfs://localhost:8020'.
    """

    def __init__(
        self,
        prefix: str,
        hdfs_uri: Optional[str] = None,
        *args,
        **kwargs
    ):
        super().__init__(prefix, *args, **kwargs)
        self.hdfs_uri = hdfs_uri

    _bucket_file_info: Optional[HDFSFileInfo] = None

    def get_bucket_file_info(self, path: str):
        """Get file information from the file url, like repository name, user, branch, and file path."""
        elements = path.split(Symbol.SLASH)
        self.get_index(path, Symbol.SLASH, 3)
        self._bucket_file_info = HDFSFileInfo(
            hdfs_uri=self.hdfs_uri,
            file_path=Symbol.SLASH.join(
                str(elements[i]) for i in range(3, len(elements))
            ),
        )

    def read_file(self, suf: str):
        """Get the content of the file.

        The address of the file is the prefix of the resource plugin plus the parameter suf.
        """
        path = urljoin(self.prefix, suf)
        self.get_bucket_file_info(path)
        hdfs_uri = self._bucket_file_info.hdfs_uri
        file_path = self._bucket_file_info.file_path
        client = InsecureClient(hdfs_uri)
        with client.read(file_path) as reader:
            content = reader.read().decode("utf-8")
        return content

