from alicebot import Plugin
from alicebot.adapter.apscheduler import scheduler_decorator
from alicebot.adapter.mirai.message import MiraiMessageSegment


@scheduler_decorator(
    trigger="cron", trigger_args={"hour": 17, "minute": 45}, override_rule=True
)
class DeMuteAll_1(Plugin):
    async def handle(self) -> None:
        await self.bot.get_adapter("mirai").call_api("unmuteAll", target=105743754)

    async def rule(self) -> bool:
        if self.event.adapter.name != "mirai":
            return False


@scheduler_decorator(
    trigger="cron", trigger_args={"hour": 17, "minute": 45}, override_rule=True
)
class DeMuteAll_2(Plugin):
    async def handle(self) -> None:
        await self.bot.get_adapter("mirai").call_api("unmuteAll", target=735211610)

    async def rule(self) -> bool:
        if self.event.adapter.name != "mirai":
            return False
