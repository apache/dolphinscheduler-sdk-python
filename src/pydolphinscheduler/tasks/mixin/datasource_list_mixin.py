from typing import Dict, List, NamedTuple, Optional

from pydolphinscheduler.models.datasource import Datasource


class DatasourceType(NamedTuple):
    type: str
    datasource: str


class DatasourceList(NamedTuple):
    dataSourceList: List[Dict]


class DatasourceListMixin:
    datasource_name: Optional[List[str]]

    def get_datasource(self) -> Dict:
        datasource_list_detail = []
        for name in self.datasource_name:
            datasource_task_u = Datasource.get_task_usage_4j(name)
            datasource_itme = DatasourceType(
                type=datasource_task_u.type, datasource=datasource_task_u.id
            )
            datasource_list_detail.append(datasource_itme._asdict())

        datasource_list = DatasourceList(dataSourceList=datasource_list_detail)
        return datasource_list._asdict()
