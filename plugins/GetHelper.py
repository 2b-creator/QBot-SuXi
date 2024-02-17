import random

from alicebot import Plugin
from alicebot.adapter.mirai.message import MiraiMessageSegment


class GetHelper(Plugin):
    async def handle(self) -> None:
        text = """详细使用方案/？
指令列表/help
记录标签/set 内容 tag=标签1，标签2
查看记录/see tag=标签1，标签2
开始记录/log on
结束记录/log off
随机一言#戳一戳"""
        msg = MiraiMessageSegment.plain(text)
        await self.event.reply(msg)

    async def rule(self) -> bool:
        if self.event.adapter.name != "mirai":
            return False
        if self.event.message.startswith('/help'):
            return True

class GetHelperPic(Plugin):
    async def handle(self) -> None:
        msg = MiraiMessageSegment.image(url="https://s2.loli.net/2024/02/17/wmcNT6fyUsieMdj.png")
        await self.event.reply(msg)

    async def rule(self) -> bool:
        if self.event.adapter.name != "mirai":
            return False
        if self.event.message.startswith('/？') or self.event.message.startswith("/?"):
            return True