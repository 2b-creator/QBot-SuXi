import random
import requests
from alicebot import Plugin
import threading
import asyncio
from alicebot.adapter.apscheduler import scheduler_decorator
from apscheduler.schedulers.blocking import BlockingScheduler


class Autolx(Plugin):
    async def handle(self) -> None:
        await self.bot.get_adapter("mirai").call_api("resp_botInvitedJoinGroupRequestEvent", operate=1)

    async def rule(self) -> bool:
        if self.event.adapter.name != "mirai":
            return False
        if self.event.type == "BotInvitedJoinGroupRequestEvent":
            return True
