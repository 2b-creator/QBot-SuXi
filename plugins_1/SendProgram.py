from alicebot import Plugin
from alicebot.adapter.apscheduler import scheduler_decorator
from alicebot.adapter.mirai.message import MiraiMessageSegment

# groupList = [784393141, 735211610, 105743754]
groupList = [784393141]


class SendProgram(Plugin):
    async def handle(self) -> None:
        # msg = MiraiMessageSegment.image(url="https://s2.loli.net/2024/03/10/dfOHV8tMgYG7QDE.png")
        msg = MiraiMessageSegment.image(url="https://s2.loli.net/2024/03/10/dfOHV8tMgYG7QDE.png")
        await self.event.reply(msg)


    async def rule(self) -> bool:
        global fromGroup
        if self.event.adapter.name != "mirai":
            return False
        if self.event.message.get_plain_text() == "/gl":
            return True
