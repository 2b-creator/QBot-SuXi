from alicebot import Plugin
from alicebot.adapter.apscheduler import scheduler_decorator

groupIndex = [784393141, 3267653962, 105743754, 706586649]


class CtrlBotMessage(Plugin):
    async def handle(self) -> None:
        commandSend = self.event.message.get_plain_text()
        commandArguments = commandSend.split(" ")
        groupId = groupIndex[int(commandArguments[1])]
        message = " ".join(commandArguments[2:])
        await self.bot.get_adapter("mirai").call_api("sendGroupMessage", target=groupId,
                                                     messageChain=[{"type": "Plain", "text": f"{message}"}])

    async def rule(self) -> bool:
        if self.event.adapter.name != "mirai":
            return False
        if self.event.message.startswith("/send "):
            return True
