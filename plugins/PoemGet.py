import random
import asyncio
import requests
import json

from alicebot import Plugin
from alicebot.adapter.mirai.message import MiraiMessageSegment


class PoemGet(Plugin):
    async def handle(self) -> None:
        # need headers
        r1 = requests.get(url="https://v2.jinrishici.com/sentence", headers=headers)
        getData = r1.json()
        content = getData["data"]["content"]
        title = getData["data"]["origin"]["title"]
        author = getData["data"]["origin"]["author"]
        dynasty = getData["data"]["origin"]["dynasty"]
        allPoem = f"{content}\n《{title}》{author}·{dynasty}"
        await self.event.adapter.call_api("sendGroupMessage", target=563575055,
                                                  messageChain=[{"type": "Plain",
                                                                 "text": f"{allPoem}"}])

    async def rule(self) -> bool:
        if self.event.adapter.name != "mirai":
            return False
        if self.event.message.get_plain_text() == "/poem":
            return True
