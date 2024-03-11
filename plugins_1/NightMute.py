from alicebot import Plugin
from alicebot.adapter.apscheduler import scheduler_decorator
from alicebot.adapter.mirai.message import MiraiMessageSegment



@scheduler_decorator(
    trigger="cron", trigger_args={"hour": 17, "minute": 10}, override_rule=True
)
class NightMute_1(Plugin):
    async def handle(self) -> None:
        await self.bot.get_adapter("mirai").call_api("mute",target=105743754)

    async def rule(self) -> bool:
        if self.event.adapter.name != "mirai":
            return False

@scheduler_decorator(
    trigger="cron", trigger_args={"hour": 19, "minute": 50}, override_rule=True
)
class NightMute_2(Plugin):
    async def handle(self) -> None:
        await self.bot.get_adapter("mirai").call_api("muteAll",target=706586649)

    async def rule(self) -> bool:
        if self.event.adapter.name != "mirai":
            return False