import ujson
from typing import List, Tuple

from uc_flow_nodes.schemas import NodeRunContext
from uc_flow_nodes.service import NodeService
from uc_flow_nodes.views import info, execute
from uc_flow_schemas import flow
from uc_flow_schemas.flow import Property, CredentialProtocol, RunState
from uc_http_requester.requester import Request
from uc_flow_schemas.flow import OptionValue
from uc_flow_schemas.flow import DisplayOptions

class NodeType(flow.NodeType):
    id: str = '97cc87fc-ae4e-4bcc-9481-7cb2aeba16db' #Идентификатор типа узла
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
        ),
        Property(
            displayName='Числовое поле',
            name='number_field',
            type=Property.Type.NUMBER,
            required=True,
        ),
        Property(
            displayName='Текстовое поле',
            name='text_field',
            type=Property.Type.STRING,
            required=True,
        ),
        Property(
            displayName='Переключатель',
            name='toggle',
            type=Property.Type.BOOLEAN,
            required=False,
            default=False,
        ),
        Property(
            displayName='Переключатель2',
            name='toggle2',
            type=Property.Type.BOOLEAN,
            default=False,
        ),
        Property(
            displayName='Выбор 1',
            name='choice_one',
            type=Property.Type.OPTIONS,
            options=[
                OptionValue(name='Значение 1', value='value1'),
                OptionValue(name='Значение 2', value='value2')
            ],
            displayOptions=DisplayOptions(
                show={'toggle2': [True]},  # Отображать, если переключатель включен
            ),
        ),
        Property(
            displayName='Выбор 2',
            name='choice_two',
            type=Property.Type.OPTIONS,
            options=[
                OptionValue(name='Значение 1', value='value1'),
                OptionValue(name='Значение 2', value='value2')
            ],
            displayOptions=DisplayOptions(
                show={'toggle2': [True]},  # Отображать, если переключатель включен
            ),
        ),

        # Добавляем поля, которые будут отображаться в зависимости от выбора в выпадающих списках
        Property(
            displayName='Email',
            name='email_field',
            type=Property.Type.STRING,
            displayOptions=DisplayOptions(
                show={
                    'choice_one': ['value1'],  # Отображать, если в первом списке выбрано "Значение 1"
                    'choice_two': ['value1'],
                    'toggle2': [True] # и во втором списке также выбрано "Значение 1"
                },
            ),
        ),
        Property(
            displayName='Дата и Время',
            name='date_time_field',
            type=Property.Type.DATETIME,
            displayOptions=DisplayOptions(
                show={
                    'choice_one': ['value2'],  # Отображать, если в обоих списках выбрано "Значение 2"
                    'choice_two': ['value2'],
                    'toggle2': [True]
                },
            ),
        ),
        ]


class InfoView(info.Info):
    class Response(info.Info.Response):
        node_type: NodeType


class ExecuteView(execute.Execute):
    async def post(self, json: NodeRunContext) -> NodeRunContext:
        try:
            text_value = int(json.node.data.properties['text_field'])
            number_value = json.node.data.properties['number_field']
            toggle = json.node.data.properties['toggle']
            
            result = text_value + number_value
            if toggle:
                result = str(text_value + number_value)
            else:
                result = text_value + number_value    
            
            await json.save_result({"result": result})
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
