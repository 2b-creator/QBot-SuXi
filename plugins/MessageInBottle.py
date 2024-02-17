import random

from alicebot import Plugin
from alicebot.adapter.mirai.message import MiraiMessageSegment


class MessageInBottleWrite(Plugin):
    async def handle(self) -> None:
        commandTest = self.event.message.get_plain_text()
        commandTest = commandTest.replace("/set ", "")
        splitList = commandTest.split(" tag=")
        messagePart = splitList[0]
        tagPart = splitList[1].replace(" ", "").split("，")
        theDict = {"text": messagePart, "tag": tagPart}
        msg = MiraiMessageSegment.plain(f"\"text\":{messagePart};\"tag\":{tagPart}")
        await self.event.reply("我记下了喵~")
        fp = open('list.txt', 'a', encoding='utf-8')
        fp.write(f"{str(theDict)},")
        fp.close()

    async def rule(self) -> bool:
        if self.event.adapter.name != "mirai":
            return False
        if self.event.message.startswith('/set '):
            return True


class MessageInBottleRead(Plugin):
    async def handle(self) -> None:
        commandPlph = self.event.message.get_plain_text()
        commandPlph = commandPlph.replace("/see ", "")
        selectTag = commandPlph.replace("tag=", "")
        selectTagList=selectTag.split("，")
        fp = open('list.txt', 'r', encoding='utf-8')
        strList = list(eval(fp.read().strip(",")))
        allTheTagMatches = []
        for i in range(len(strList)):
            # for j in range(len(strList[i]["tag"])):
            #     if strList[i]["tag"][j] == selectTag:
            #         allTheTagMatches.append(strList[i])
            if set(selectTagList).issubset(set(strList[i]["tag"])):
                allTheTagMatches.append(strList[i])
        preSend = allTheTagMatches[random.randint(0, len(allTheTagMatches) - 1)]["text"]
        msg = MiraiMessageSegment.plain(f"{preSend}")
        fp.close()
        await self.event.reply(msg)

    async def rule(self) -> bool:
        if self.event.adapter.name != "mirai":
            return False
        if self.event.message.startswith('/see '):
            return True
