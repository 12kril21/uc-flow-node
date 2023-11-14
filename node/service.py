import ujson
from typing import List, Tuple

from uc_flow_nodes.schemas import NodeRunContext
from uc_flow_nodes.service import NodeService
from uc_flow_nodes.views import info, execute
from uc_flow_schemas import flow
from uc_flow_schemas.flow import Property, CredentialProtocol, RunState
from uc_http_requester.requester import Request


class NodeType(flow.NodeType):
    id: str = 'OrderProcessor' #Идентификатор типа узла
    type: flow.NodeType.Type = flow.NodeType.Type.action
    name: str = 'OrderProcessor' #Тех имя узла
    is_public: bool = False
    displayName: str = 'Обработчик заказов' # Отображаемое имя узла
    icon: str = '<svg><text x="8" y="50" font-size="50">🤖</text></svg>'
    description: str = 'Обработка и управление заказами' #Описание узла
    properties: List[Property] = [
        Property(
            displayName='Тестовое поле',
            name='foo_field',
            type=Property.Type.JSON,
            placeholder='Foo placeholder',
            description='Foo description',
            required=True,
            default='Test data',
        )
    ]


class InfoView(info.Info):
    class Response(info.Info.Response):
        node_type: NodeType


class ExecuteView(execute.Execute):
    async def post(self, json: NodeRunContext) -> NodeRunContext:
        try:
            await json.save_result({
                "result": json.node.data.properties['foo_field']
            })
            json.state = RunState.complete
        except Exception as e:
            self.log.warning(f'Error {e}')
            await json.save_error(str(e))
            json.state = RunState.error
        return json


class Service(NodeService):
    class Routes(NodeService.Routes):
        Info = InfoView
        Execute = ExecuteView
