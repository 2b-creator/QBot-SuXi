import asyncio
import os
import pathlib

from alicebot import Plugin
from alicebot.adapter.mirai.message import MiraiMessageSegment
from alicebot.adapter.mirai.message import MiraiMessage
from alicebot.adapter.mirai.event.notice import MemberLeaveEventQuit
from alicebot.message import Message
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from alicebot.adapter.apscheduler import scheduler_decorator

import schedule
import time
import requests
import json
import warnings


class HalloAlice(Plugin):
    async def handle(self) -> None:
        msg = " 花径不曾缘客扫，蓬门今始为君开。欢迎新人入群，来填个小问卷吧。\n1.是江高学子吗？\n2.有没有独立完成的文章（包括小说、诗歌）\n3.强烈建议立刻发篇文，你将会获得来自墨水的好感）\n（回复TD 退订）"
        msg2 = " 欢迎新人入群，来填个小问卷吧。"
        # resp = MiraiMessageSegment.plain(msg)
        # await self.event.reply(msg2)

        await self.event.adapter.call_api("sendGroupMessage", target=addGroupId,
                                          messageChain=[{"type": "At", "target": newMemberId},
                                                        {"type": "Plain", "text": msg}])

    async def rule(self) -> bool:
        global a, newMemberId, addGroupId
        if self.event.adapter.name != "mirai":
            return False
        if self.event.type == "MemberJoinEvent":
            newMemberId = self.event.member.id
            addGroupId = self.event.member.group.id
            return True
        return False


class OneSent(Plugin):
    async def handle(self) -> None:
        url = "https://api.xygeng.cn/one"
        response = requests.post(url)
        sent = response.json()["data"]["content"]
        await self.event.adapter.call_api("sendGroupMessage", target=fromGroup,
                                          messageChain=[{"type": "At", "target": fromWho},
                                                        {"type": "Plain", "text": f" {sent}"}])

    async def rule(self) -> bool:
        global fromWho, fromGroup
        if self.event.adapter.name != "mirai":
            return False
        if self.event.type == "NudgeEvent":
            fromWho = self.event.fromId
            fromGroup = self.event.subject.id
            toWho = self.event.target
            if int(toWho) == 3267653962:
                return True
        return False


class ReRead(Plugin):
    async def handle(self) -> None:
        msg = MiraiMessageSegment.plain(self.event.message.get_plain_text() + "喵~")
        await self.event.reply(msg)

    async def rule(self) -> bool:
        global words, a
        if self.event.adapter.name != "mirai":
            return False
        if self.event.type != "GroupMessage":
            return False
        if self.event.message.get_plain_text() == "复读，启动！":
            a = 1
        if a == 1:
            if self.event.message.get_plain_text() == "复读，关闭！":
                a = 0
        return a == 1


@scheduler_decorator(
    trigger="interval", trigger_args={"seconds": 10}, override_rule=True
)
class SleepNotice(Plugin):
    async def handle(self) -> None:
        await self.bot.get_adapter("mirai").call_api("sendGroupMessage", target=932490832,
                                                     messageChain=[{"type": "Plain", "text": "晚上好，记得睡觉哦~"}])

    async def rule(self) -> bool:
        return False


from alicebot import Bot

bot = Bot()
bot.load_plugins_from_dirs(pathlib.Path("./plugins"))
bot.load_plugins(HalloAlice, OneSent, ReRead)

if __name__ == "__main__":
    bot.run()
    bot.load_adapters("alicebot.adapter.apscheduler")
