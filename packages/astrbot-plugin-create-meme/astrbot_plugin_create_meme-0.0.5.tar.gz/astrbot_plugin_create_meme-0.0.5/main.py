from astrbot.api.event import filter
from astrbot.api.all import *
from astrbot.api.all import *
from astrbot.api.event import filter, AstrMessageEvent
from .emoji import parse_target,get_meme_image


@register("create_meme", "祁筱欣", "一个为AstrBot设计的表情包插件。", "0.0.5")
class HitokotoPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
        logger.info("create_meme插件初始化完成")

    @filter.command("戒导")
    async def emoji1(self, event: AstrMessageEvent):
        ids = await parse_target(event)
        data = await get_meme_image(ids, 2)
        await event.send(data)

    @filter.command("二次元入口")
    async def emoji_entrance(self, event: AstrMessageEvent):
        ids = await parse_target(event)
        data = await get_meme_image(ids, 4)
        await event.send(data)

    @filter.command("添乱")
    async def emoji1_tianluan(self, event: AstrMessageEvent):
        ids = await parse_target(event)
        data = await get_meme_image(ids, 5)
        await event.send(data)


    @filter.command("上瘾")
    async def emoji1_shangyin(self, event: AstrMessageEvent):
        ids = await parse_target(event)
        data = await get_meme_image(ids, 6)
        await event.send(data)


    @filter.command("一样")
    async def emoji1_tongyi(self, event: AstrMessageEvent):
        ids = await parse_target(event)
        data = await get_meme_image(ids, 7)
        await event.send(data)


    @filter.command("一直")
    async def emoji1_zhiyin(self, event: AstrMessageEvent):
        ids = await parse_target(event)
        data = await get_meme_image(ids, 8)
        await event.send(data)
        

    @filter.command("creatememe-help")
    async def help_command(self, event: AstrMessageEvent):
        """显示插件帮助信息。"""
        help_text = """
        === 表情包插件帮助 ===
        命令列表:
        - 戒导 @指定用户: 生成包含@指定用户的戒导表情包。
        - 添乱 @指定用户: 生成包含@指定用户的添乱表情包。
        - 二次元入口 @指定用户: 生成包含@指定用户的二次元入口表情包。
        - 上瘾 @指定用户: 生成包含@指定用户的上瘾表情包。
        - 一样 @指定用户: 生成包含@指定用户的一样表情包。
        - 一直 @指定用户: 生成包含@指定用户的一直表情包。
        - creatememe-help: 显示帮助信息。
        """
        yield event.plain_result(help_text)

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
        logger.info("create_meme插件已终止")
