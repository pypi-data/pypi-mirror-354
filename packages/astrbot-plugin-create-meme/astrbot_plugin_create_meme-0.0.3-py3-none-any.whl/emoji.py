from astrbot.api import logger
from astrbot.api.event import AstrMessageEvent
from astrbot.api.all import *
import aiohttp


async def parse_target(event: AstrMessageEvent):
    """解析@目标或用户名"""
    for comp in event.message_obj.message:
        if isinstance(comp, At) and event.get_self_id() != str(comp.qq):
            return str(comp.qq)
    return None


async def get_meme_image(event: AstrMessageEvent, type: int):
    """根据QQ号和类型生成表情包图片。"""
    base_url = "https://api.lolimi.cn/API/preview/api.php?action=create_meme"
    ids = await parse_target(event)
    logger.info(f"请求参数:QQ号为:{ids}, type为:{type}")
    url = f"{base_url}&qq={ids}&type={type}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    logger.info(f"链接测试成功: {url}")
                    yield event.image_result(url)
                else:
                    logger.error(
                        f"链接测试失败，请检查图片链接是否有效。状态码: {response.status}, URL: {url}"
                    )
                    return None
    except aiohttp.ClientError as e:
        logger.error(f"请求链接时发生错误: {e}, URL: {url}")
        yield event.plain_result(f"生成表情包失败，请稍后再试。错误信息: {e}")
