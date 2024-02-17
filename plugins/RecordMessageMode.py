import os
import time

from alicebot import Plugin
from alicebot.adapter.mirai.message import MiraiMessageSegment


class RecordMessageMode(Plugin):
    async def handle(self) -> None:
        b = 1
        if self.event.message.get_plain_text() == "/log on":
            await self.event.adapter.call_api("sendGroupMessage", target=563575055,
                                              messageChain=[{"type": "Plain",
                                                             "text": "“喵？”＃揉了揉刚睡醒的眼睛“又有活要干了吗？你们话怎么这么多喵。”\n当前记录已开始，使用（）旁观\nlog off结束记录"}])
        if self.event.message.startswith("（") or self.event.message.startswith("("):
            b = 0
        if self.event.message.get_plain_text() == "/log off":
            pass
        if b == 1:
            fp = open(f'{fileName}.txt', 'a', encoding='utf-8')
            fp.write(f'{self.event.message.get_plain_text()}\n')
            fp.close()

    async def rule(self) -> bool:
        global fileName, a
        if self.event.adapter.name != "mirai":
            return False
        if self.event.message.get_plain_text() == "/log on":
            fileName = time.strftime('%a-%b-%d-%H-%M-%S-%Y', time.localtime())
            a = 1
        if a == 1:
            if self.event.message.get_plain_text() == "/log off":
                await self.event.adapter.call_api("sendGroupMessage", target=563575055,
                                                  messageChain=[{"type": "Plain",
                                                                 "text": f"停止记录，记录保存为{fileName}.txt"}])
                a = 0
                file = open(f'{fileName}.txt', 'r', encoding='utf-8')
                content = file.read()
                await self.event.adapter.call_api("sendGroupMessage", target=563575055,
                                                      messageChain=[{"type": "Plain",
                                                                     "text": f"{content}"}])
                file.close()
        return a == 1
