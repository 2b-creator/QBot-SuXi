from alicebot import Plugin
from alicebot.adapter.apscheduler import scheduler_decorator
from alicebot.adapter.mirai.message import MiraiMessageSegment

groupList = [784393141, 735211610, 105743754]

class SensitiveWords(Plugin):
    async def handle(self) -> None:
        pass

    async def rule(self) -> bool:
        return False