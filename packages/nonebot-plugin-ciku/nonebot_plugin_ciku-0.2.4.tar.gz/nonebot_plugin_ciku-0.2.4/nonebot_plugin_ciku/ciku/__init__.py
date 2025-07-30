from .main import check_input
from nonebot.adapters.onebot.v11 import GroupMessageEvent,Event,Message
from typing import Literal, Type, TypeVar
from nonebot.adapters.onebot.v11 import Adapter
from nonebot.log import logger
from nonebot.typing import overrides
from .webui import *

Event_T = TypeVar("Event_T", bound=Type[Event])

def register_event(event: Event_T) -> Event_T:
    Adapter.add_custom_model(event)
    logger.opt(colors=True).trace(
        f"Custom event <e>{event.__qualname__!r}</e> registered from module <g>{event.__class__.__module__!r}</g>"
    )
    return event


@register_event
class GroupMessageSentEvent(GroupMessageEvent):
    """群聊消息里自己发送的消息"""

    post_type: Literal["message_sent"]
    message_type: Literal["group"]

    @overrides(Event)
    def get_type(self) -> str:
        """伪装成message类型。"""
        return "message"