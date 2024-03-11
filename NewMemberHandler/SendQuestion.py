import random
from alicebot import Plugin
import threading
import asyncio
from alicebot.adapter.apscheduler import scheduler_decorator
from apscheduler.schedulers.blocking import BlockingScheduler

ans = 0
res = 0
j = 0


class SendQuestion(Plugin):
    async def f(self):
        global j
        recallPtrMessage = res["messageId"]
        await asyncio.sleep(60)
        await self.bot.get_adapter("mirai").call_api("kick", target=fromGroup, memberId=newMember)
        await self.bot.get_adapter("mirai").call_api("recall", target=fromGroup, messageId=recallPtrMessage)
        t.cancel()
        self.skip()

    async def handle(self) -> None:
        global res, ans, t
        await self.bot.get_adapter("mirai").call_api("mute", memberId=newMember, target=fromGroup, time=120)
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        ans = a + b
        question = f" 请在 1 分钟内完成下面的问题并使用临时会话的方式发给我,否则将会被移除\n {a} + {b} = ?"

        res = await self.bot.get_adapter("mirai").call_api("sendGroupMessage", target=fromGroup,
                                                           messageChain=[{"type": "At", "target": newMember},
                                                                         {"type": "Plain", "text": question}])
        t = asyncio.create_task(self.f())
        # f_stop = threading.Event()
        # start calling f now and every 60 sec thereafter
        # await self.f(f_stop)
        # stop the thread when needed
        # f_stop.set()
        # await asyncio.sleep(60)
        # self.bot.get_adapter("mirai").call_api("kick", target=fromGroup, memberId=newMember)

    async def rule(self) -> bool:
        global newMember, fromGroup
        if self.event.adapter.name != "mirai":
            return False
        if self.event.type == "MemberJoinEvent":
            newMember = self.event.member.id
            fromGroup = self.event.member.group.id
            return True
        if self.event.type == "TempMessage" and self.event.message.get_plain_text() == str(ans):
            await self.bot.get_adapter("mirai").call_api("unmute", memberId=newMember, target=fromGroup)
            recallPtrMessage = res["messageId"]
            await self.bot.get_adapter("mirai").call_api("recall", target=fromGroup, messageId=recallPtrMessage)
            t.cancel()
            self.skip()

# class OverTimeHandler(Plugin):
#
#     async def handle(self) -> None:
#         sched = BlockingScheduler(timezone="Asia/Shanghai")
#         sched.add_job(self.task, "interval", seconds=10)
#         sched.start()
#
#     async def rule(self) -> bool:
#         global newMember, fromGroup
#         if self.event.type == "MemberJoinEvent":
#             newMember = self.event.member.id
#             fromGroup = self.event.member.group.id
#             return True
#         if self.event.type == "TempMessage" and self.event.message.get_plain_text() == str(ans):
#             await self.bot.get_adapter("mirai").call_api("unmute", memberId=newMember, target=fromGroup)
#             recallPtrMessage = res["messageId"]
#             await self.bot.get_adapter("mirai").call_api("recall", target=fromGroup, messageId=recallPtrMessage)
#             self.skip()
#
#     def task(self):
#         recallPtrMessage = res["messageId"]
#         self.bot.get_adapter("mirai").call_api("kick", target=fromGroup, memberId=newMember)
#         self.bot.get_adapter("mirai").call_api("recall", target=fromGroup, messageId=recallPtrMessage)
#         self.skip()
