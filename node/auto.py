import ujson
import httpx
from typing import List, Tuple

from uc_flow_nodes.schemas import NodeRunContext
from uc_flow_nodes.service import NodeService
from uc_flow_nodes.views import info, execute
from uc_flow_schemas import flow
from uc_flow_schemas.flow import Property, CredentialProtocol, RunState
from uc_http_requester.requester import Request
from uc_flow_schemas.flow import OptionValue



class AuthCredentialType(flow.CredentialType):
    id: str = 'auth_credential'
    is_public: bool = False
    displayName: str = 'Аутентификация'
    protocol: CredentialProtocol = CredentialProtocol.ApiKey
    protected_properties: List[Property] = [
        Property(
            displayName='Email',
            name='email',
            type=Property.Type.STRING,
            required=True,
        ),
        Property(
            displayName='api_key',
            name='api_key',
            type=Property.Type.STRING,
            required=True,
        ),
        Property(
            displayName='hostname',
            name='hostname',
            type=Property.Type.STRING,
            required=True,
        )
    ]

class NodeType(flow.NodeType):
    id: str = 'f1736b10-12f3-4df2-b8d3-02ba49cc3f25'
    type: flow.NodeType.Type = flow.NodeType.Type.action
    name: str = 'log in'
    is_public: bool = False
    displayName: str = 'Авторизация'
    icon: str = '<svg><text x="8" y="50" font-size="50">🤖</text></svg>'
    description: str = 'Вход'
    


class InfoView(info.Info):
    class Response(info.Info.Response):
        node_type: NodeType


class ExecuteView(execute.Execute):
    async def post(self, json: NodeRunContext) -> NodeRunContext:
        try:
            credentials = await json.get_credentials()
            email = credentials.data['email']
            api_key = credentials.data['api_key']
            host_name = credentials.data['hostname']

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url=f'https://{host_name}/v2api/auth/login',
                    json={'email': email, 'api_key': api_key},
                )

            if response.status_code != 200:
                raise Exception(f'Ошибка авторизации: {response.text}')

            token = response.json()['token']
            await json.save_result({'token': str(token), 'hostname': host_name, 'email': email})
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
        
