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
from uc_flow_schemas.flow import DisplayOptions



class CustomerNodeType(flow.NodeType):
    id: str = '4069be80-5e96-4880-b0aa-261c60263261'
    type: flow.NodeType.Type = flow.NodeType.Type.action
    name: str = 'Customers'
    is_public: bool = False
    displayName: str = 'Customer'
    icon: str = '<svg><text x="8" y="50" font-size="50">👥</text></svg>'
    description: str = 'Запрос списка клиентов из AlfaCRM'
    properties: List[Property] = [
        Property(
            displayName='token',
            name='tok',
            type=Property.Type.STRING
        ),
        Property(
            displayName='hostname',
            name='host',
            type=Property.Type.STRING
        ),
        Property(
            displayName='Resource',
            name='res',
            type=Property.Type.OPTIONS,
            options=[
                OptionValue(name='Customer', value='customer'),
            ],
        ),
        Property(
            displayName='branch_id',
            name='id',
            type=Property.Type.STRING,
        ),
        Property(
            displayName='Operation',
            name='oper',
            type=Property.Type.OPTIONS,
            options=[
                OptionValue(name='index', value='index'),
                OptionValue(name='create', value='create'),
                OptionValue(name='update', value='update')
            ]
        ),
        Property(
            displayName='Parameters',
            name='Parameters',
            type=Property.Type.COLLECTION,
            placeholder='Add',
            default={},
            displayOptions=DisplayOptions(
                show={
                    'oper': ['index']
                }
                ),
            options=[
                Property(
                    displayName='id',
                    name='id',
                    type=Property.Type.NUMBER,
                    #"values": [
                    #        {
                    #            "displayOptions": {},
                    #            "name": "id",
                    #            "typeOptions": {},
                    #            "type": "number"
                    #        }
                    #        ]
                ),
                Property(
                    displayName='is_study',
                    name='is_study',
                    default=True,
                    type=Property.Type.BOOLEAN,
                    #values": [
                     #       {
                      #          "displayOptions": {},
                       #         "name": "is_study",
                        #        "typeOptions": {},
                         #       "type": "BOOLEAN"
                          #  }
                           # ]
                ),
                Property(
                    displayName='name',
                    name='name',
                    default='qdadas',
                    type=Property.Type.STRING,
                    #"values": [
                    #        {
                    #            "displayOptions": {},
                    #            "name": "name",
                    #            "typeOptions": {},
                    #            "type": "STRING"
                    #        }
                    #        ]
                ),
                Property(
                    displayName='data_from',
                    name='data_from',
                    type=Property.Type.DATETIME,
                    #"values": [
                    #        {
                    #            "displayOptions": {},
                    #            "name": "data_from",
                    #            "typeOptions": {},
                    #            "type": "DATETIME"
                    #        }
                    #        ]
                ),
                Property(
                    displayName='balance_contract_from',
                    name='balance_contract_from',
                    type=Property.Type.NUMBER,
                    #"values": [
                    #        {
                    #            "displayOptions": {},
                    #            "name": "balance_contract_from",
                    #            "typeOptions": {},
                    #            "type": "NUMBER"
                    #        }
                    #        ]
                ),
            ]
        ),
        Property(
            displayName='Parameters',
            name='Parameters',
            type=Property.Type.COLLECTION,
            placeholder='Add',
            default={},
            displayOptions=DisplayOptions(
                show={
                    'oper': ['create']
                }
                ),
            options=[
                Property(
                    displayName='is_study',
                    name='is_study',
                    type=Property.Type.BOOLEAN,
                    #"values": [
                    #        {
                    #            "displayOptions": {},
                    #            "name": "is_study",
                    #            "typeOptions": {},
                    #            "type": "BOOLEAN"
                    #        }
                    #        ]
                ),
                Property(
                    displayName='name',
                    name='name',
                    type=Property.Type.STRING,
                    #"values": [
                    #        {
                    #            "displayOptions": {},
                    #            "name": "name",
                    #            "typeOptions": {},
                    #            "type": "STRING"
                    #        }
                    #        ]
                ),
                Property(
                    displayName='branch_ids',
                    name='branch_ids',
                    type=Property.Type.NUMBER,
                    #"values": [
                    #        {
                    #            "displayOptions": {},
                    #            "name": "branch_ids",
                    #            "typeOptions": {},
                    #            "type": "NUMBER"
                    #        }
                    #        ]
                ),
                Property(
                    displayName='legal_type',
                    name='legal_type',
                    type=Property.Type.BOOLEAN,
                    #"values": [
                    #        {
                    #            "displayOptions": {},
                    #            "name": "legal_type",
                    #            "typeOptions": {},
                    #            "type": "BOOLEAN"
                    #        }
                    #        ]
                ),
            ]
        ),
        Property(
            displayName='Parameters',
            name='Parameters',
            type=Property.Type.COLLECTION,
            placeholder='Add',
            default={},
            displayOptions=DisplayOptions(
                show={
                    'oper': ['update']
                }
                ),
            options=[
                Property(
                    displayName='id',
                    name='id',
                    type=Property.Type.NUMBER,
                    #"values": [
                    #        {
                    #            "displayOptions": {},
                    #            "name": "id",
                    #            "typeOptions": {},
                    #            "type": "NUMBER"
                    #        }
                    #        ]
                ),
                Property(
                    displayName='name',
                    name='name',
                    type=Property.Type.STRING,
                    #"values": [
                    #        {
                    #            "displayOptions": {},
                    #            "name": "name",
                    #            "typeOptions": {},
                    #            "type": "STRING"
                    #        }
                    #        ]
                ),
            ]
        )
    ]


class CustomerView(info.Info):
    class Response(info.Info.Response):
        node_type: CustomerNodeType

import json as js

class CustomerExecuteView(execute.Execute):
    async def create_customer(self, hostname, token, branch_id, customer_data):
        url = f'https://{hostname}/v2api/{branch_id}/customer/create'
        headers = {
            'X-ALFACRM-TOKEN': token,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        customer_data_json = js.dumps(customer_data)
        self.log.info(f'Create URL: {url}')
        self.log.info(f'Create data: {customer_data}')

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, content=customer_data_json)

        if response.status_code != 200:
            raise Exception(f'Ошибка запроса: {response.text}')

        return response.json()


    async def update_customer(self, hostname, token, branch_id, customer_id, update_data):
        url = f'https://{hostname}/v2api/{branch_id}/customer/update?id={customer_id}'
        self.log.info(f'Update URL: {url}')
        self.log.info(f'Update data: {update_data}')
        headers = {
            'X-ALFACRM-TOKEN': token,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        update_data_json = js.dumps(update_data)

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, content=update_data_json)

        if response.status_code != 200:
            raise Exception(f'Ошибка запроса: {response.text}')

        return response.json()


    async def post(self, json:NodeRunContext) -> NodeRunContext:
        try:
            parent_data = context.get_parent_result('')
            branch_id = json.node.data.properties['id']
            hostname = json.node.data.properties['host']
            token = json.node.data.properties['tok']
            headers = {
                    'X-ALFACRM-TOKEN': token,
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }


            if json.node.data.properties['oper'] == 'index':
                url = f'https://{hostname}/v2api/{branch_id}/customer/index'
                params = json.node.data.properties.get('Parametrs', {})
                customer_data = {k: v[0] for k, v in params.items() if v and isinstance(v, list)}
                
                request_data = js.dumps(customer_data)

                async with httpx.AsyncClient() as client:
                    response = await client.post(url, headers=headers, content=request_data)
                if response.status_code != 200:
                    raise Exception(f'Ошибка запроса: {response.text}')
                await json.save_result(response.json())


            elif json.node.data.properties['oper'] == 'create':
                params = json.node.data.properties.get('Parametrs', {})
                customer_data1 = {k: v[0] for k, v in params.items() if v}
                customer_data = {}
                for key, value in customer_data1.items():
                    if isinstance(value, dict):
                        inner_value = next(iter(value.values()))
                        customer_data[key] = inner_value
                    elif isinstance(value, list) and value:
                        customer_data[key] = value[0]
                    else:
                        customer_data[key] = value
                result = await self.create_customer(hostname, token, branch_id, customer_data)

                await json.save_result(result)


            elif json.node.data.properties['oper'] == 'update':
                params = json.node.data.properties.get('Parametrs', {})
                customer_id = None
                update_data = {}
                for k, v in params.items():
                    if k == 'id':
                        customer_id = v[0]
                    elif v:
                        update_data[k] = v[0]
                update_data = update_data.get('name')
                if customer_id is None:
                    raise Exception("ID клиента не предоставлен")
                else:
                    customer_id = customer_id.get('id')

                result = await self.update_customer(hostname, token, branch_id, customer_id, update_data)
                await json.save_result(result)
                
            json.state = RunState.complete



        except Exception as e:
            self.log.warning(f'Error {e}')
            await json.save_error(str(e))
            json.state = RunState.error
        return json

class Service(NodeService):
    class Routes(NodeService.Routes):
        Info = CustomerView
        Execute = CustomerExecuteView
