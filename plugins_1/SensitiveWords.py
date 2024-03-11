from alicebot import Plugin
from loguru import logger
from alicebot.adapter.apscheduler import scheduler_decorator
from alicebot.adapter.mirai.message import MiraiMessageSegment

groupList = [784393141, 735211610, 105743754, 706586649, 765662972]


class SensitiveWords(Plugin):
    async def handle(self) -> None:
        await self.bot.get_adapter("mirai").call_api("recall", target=fromGroup, messageId=ptrMessage)
        await self.bot.get_adapter("mirai").call_api("mute", target=fromGroup, memberId=fromWho, time=60)

    async def rule(self) -> bool:
        global fromWho, fromGroup, ptrMessage
        if self.event.adapter.name != "mirai":
            return False
        if self.event.type == "GroupMessage":
            fromWho = self.event.sender.id
            fromGroup = self.event.sender.group.id
            ptrMessage = self.event.messageChain.as_message_chain()[0]["id"]
            # logger.info(self.event.messageChain.as_message_chain()[0]["id"])
            fp = open("plugins_1/sensitive_words.txt", "r", encoding="utf-8")
            strList = eval(fp.read())
            for i in strList:
                if i in self.event.message.get_plain_text():
                    fp.close()
                    return True


rels = []


class SensitiveWordsJF(Plugin):
    async def handle(self) -> None:
        fp = open("plugins_1/Record.txt", "r", encoding="utf-8")
        readstr = fp.read()
        contentListstr = f"[{readstr[1:-1]}]"
        contentList = eval(contentListstr)
        fp.close()

        for i in range(len(contentList)):
            if contentList[i]["id"] == fromWhoJ:
                try:
                    sensiDic = contentList[i]["rec"]
                except KeyError:
                    sensiDic = {}
                    for j in restrList:
                        sensiDic.get(j, 0)
                for k in restrList:
                    if k in sensiDic.keys():
                        sensiDic[k] += 1
                    else:
                        sensiDic[k] = 1

                contentList[i]["rec"] = sensiDic
                tempDic = contentList[i]
                contentList.pop(i)
                contentList.append(tempDic)
                break
        else:
            newDic = {}
            newDic["id"] = fromWhoJ
            newDic["rec"] = {}
            for j in restrList:
                newDic["rec"][j] = 1
            contentList.append(newDic)

        fp = open('plugins_1/Record.txt', 'w', encoding='utf-8')
        fp.write(str(contentList)[:-1] + ",")
        fp.close()
        rels.clear()

    async def rule(self) -> bool:
        global fromWhoJ, fromGroupJ, restrList
        if self.event.adapter.name != "mirai":
            return False
        if self.event.type == "GroupMessage":
            fromWhoJ = self.event.sender.id
            fromGroupJ = self.event.sender.group.id
            fp = open("plugins_1/mgc_jf.txt", "r", encoding="utf-8")
            strList = fp.read()
            strListHandler = strList[1:-1]
            strListHandlerContent = strListHandler.split(",")
            restrList = []
            for i in strListHandlerContent:
                if i in self.event.message.get_plain_text():
                    restrList.append(i)
                if i == strListHandlerContent[-1]:
                    fp.close()
                    return True
