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


async def get_meme_image(ids, type):
    result = MessageChain()
    result.chain = []
    base_url = "https://api.lolimi.cn/API/preview/api.php?action=create_meme"
    logger.info(f"请求参数:QQ号为:{ids}, type为:{type}")
    url = f"{base_url}&qq={ids}&type={type}"
    logger.info(f"请求地址:{url}")
    try:
        # 使用 aiohttp 发送异步 GET 请求
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                # 检查请求是否成功
                if response.status == 200:
                    # 读取图片内容
                    image_data = await response.read()
                    # 将图片保存到本地
                    file_path = (
                        f"./data/plugins/emoji/petemoji_{ids}_{type}.gif"
                    )
                    with open(file_path, "wb") as file:
                        file.write(image_data)
                    # 构造返回结果
                    result.chain = [Image.fromFileSystem(file_path)]
                    logger.info(f"表情包制作成功，保存路径: {file_path}")
                    return result
                else:
                    result.chain = [Plain(f"表情包制作失败，状态码: {response.status}")]
                    logger.error(f"表情包制作失败，状态码: {response.status},{response.text}")
                    return result
    except aiohttp.ClientError as e:
        result.chain = [Plain(f"请求异常: {e}")]
        logger.error(f"请求异常: {e}")
        return result
