from astrbot.api import logger
from astrbot.api.event import AstrMessageEvent
from astrbot.api.all import *

async def parse_target(event: AstrMessageEvent):
    """解析@目标或用户名"""
    for comp in event.message_obj.message:
        if isinstance(comp, At) and event.get_self_id() != str(comp.qq):
            return str(comp.qq)
    return None


async def get_meme_image(ids, type):
    """根据QQ号和类型生成表情包图片。"""
    base_url = "https://api.lolimi.cn/API/preview/api.php?action=create_meme"
    logger.info(f"请求参数:QQ号为:{ids}, type为:{type}")
    url =f"{base_url}&qq={ids}&type={type}"
    return url