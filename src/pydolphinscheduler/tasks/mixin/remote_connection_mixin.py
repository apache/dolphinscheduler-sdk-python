from typing import Dict, NamedTuple, Optional

from pydolphinscheduler.models.datasource import Datasource


class RemoteConnectionType(NamedTuple):
    open: bool
    datasourceType: str
    datasourceId: str


class RemoteConnectionList(NamedTuple):
    remoteConnection: Dict


class RemoteConnectionMixin:
    remote_connection: Optional[str]

    def get_remote_connection(self) -> Dict:
        if self.remote_connection is not None:
            connection = Datasource.get_task_usage_4j(self.remote_connection)
            connection_itme = RemoteConnectionType(
                open=True, datasourceType=connection.type, datasourceId=connection.id
            )

            datasource_list = RemoteConnectionList(
                remoteConnection=connection_itme._asdict()
            )
            return datasource_list._asdict()
