import random
from alicebot import Plugin
import threading
import asyncio
from alicebot.adapter.apscheduler import scheduler_decorator
from apscheduler.schedulers.blocking import BlockingScheduler

groupList = [765662972]


class SendProToNew(Plugin):
    async def f(self):
        recallPtrMessage = res["messageId"]
        await asyncio.sleep(60 * 30)
        await self.bot.get_adapter("mirai").call_api("kick", target=fromGroup, memberId=newMember)
        t.cancel()
        self.skip()

    async def handle(self) -> None:
        global res, t
        await self.bot.get_adapter("mirai").call_api("mute", memberId=newMember, target=fromGroup,
                                                     time=60 * 40)
        question = "请阅读群公告，并确认是否同意加入本群...\n"
        fp = open("NewMemberHandler/Pro.txt", "r", encoding="utf-8")
        question += fp.read()
        fp.close()
        question += "\n请回复“同意(1)”或“拒绝(2)”"
        question += "\n若您在 30 分钟内未作出选择，系统将自动选择“拒绝”，并将您移除本群。"
        notice = " 请阅读我的私信（临时会话）内容，并确认是否同意加入本群"
        await self.bot.get_adapter("mirai").call_api("sendTempMessage", group=fromGroup, qq=newMember,
                                                     messageChain=[{"type": "Plain", "text": question}])
        res = await self.bot.get_adapter("mirai").call_api("sendGroupMessage", target=fromGroup,
                                                           messageChain=[{"type": "At", "target": newMember},
                                                                         {"type": "Plain", "text": notice}])
        t = asyncio.create_task(self.f())

    async def rule(self) -> bool:
        global newMember, fromGroup, wordls_1, wordls_2
        wordls_1 = ["1", "同意", "yes", "是"]
        wordls_2 = ["2", "拒绝", "no", "否"]
        if self.event.adapter.name != "mirai":
            return False

        if self.event.type == "MemberJoinEvent":
            newMember = self.event.member.id
            fromGroup = self.event.member.group.id
            if fromGroup in groupList:
                return True
        if self.event.type == "TempMessage":
            if self.event.message.get_plain_text() in wordls_1:
                await self.bot.get_adapter("mirai").call_api("unmute", memberId=newMember, target=fromGroup)
                # recallPtrMessage = res["messageId"]
                # await self.bot.get_adapter("mirai").call_api("recall", target=fromGroup, messageId=recallPtrMessage)
                t.cancel()
                self.skip()
            if self.event.message.get_plain_text() in wordls_2:
                await self.bot.get_adapter("mirai").call_api("kick", target=fromGroup, memberId=newMember)
                t.cancel()
                self.skip()
