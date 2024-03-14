import random
import requests
from alicebot import Plugin
import threading
import asyncio
from alicebot.adapter.apscheduler import scheduler_decorator
from apscheduler.schedulers.blocking import BlockingScheduler

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