from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.event import *
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.core import AstrBotConfig
from .emoji import get_meme_image


@register("create_meme", "祁筱欣", "一个为AstrBot设计的表情包插件。", "0.0.4")
class HitokotoPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
        logger.info("create_meme插件初始化完成")

    @filter.command("戒导")
    async def emoji_jiedao(self, event: AstrMessageEvent):
        await get_meme_image(event, 2)

    @filter.command("二次元入口")
    async def emoji_entrance(self, event: AstrMessageEvent):
        await get_meme_image(event, 4)

    @filter.command("添乱")
    async def emoji1_tianluan(self, event: AstrMessageEvent):
        await get_meme_image(event, 5)


    @filter.command("上瘾")
    async def emoji1_tianluan(self, event: AstrMessageEvent):
        await get_meme_image(event, 6)


    @filter.command("treasurebag-help")
    async def help_command(self, event: AstrMessageEvent):
        """显示插件帮助信息。"""
        help_text = """
        === 表情包插件帮助 ===
        命令列表:
        - 戒导 @指定用户: 生成包含@指定用户的戒导表情包。
        - 添乱 @指定用户: 生成包含@指定用户的添乱表情包。
        - 二次元入口 @指定用户: 生成包含@指定用户的二次元入口表情包。
        - treasurebag-help: 显示帮助信息。
        """
        yield event.plain_result(help_text)

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
        logger.info("create_meme插件已终止")
