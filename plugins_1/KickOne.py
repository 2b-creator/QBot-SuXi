from alicebot import Plugin
from alicebot.adapter.apscheduler import scheduler_decorator
from alicebot.adapter.mirai.message import MiraiMessageSegment

groupList = [784393141, 735211610, 105743754]


class KickOne(Plugin):
    async def handle(self) -> None:
        commandKickMode = self.event.message.get_plain_text()
        argumentList = commandKickMode.split(" ")
        for i in groupList:
            groupMemberDic = await self.bot.get_adapter("mirai").call_api("memberList", target=i)
            for j in groupMemberDic["data"]:
                intId = int(argumentList[1])
                if intId == j["id"]:
                    await self.bot.get_adapter("mirai").call_api("kick", target=i, memberId=intId)

    async def rule(self) -> bool:
        global argumentList
        if self.event.message.startswith('/kick') or self.event.message.startswith("/kick"):
            return True

        if self.event.adapter.name != "mirai":
            return False
