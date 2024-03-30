import random
import requests
from alicebot import Plugin
from IPython.display import Latex
import threading
import asyncio
from alicebot.adapter.apscheduler import scheduler_decorator
from apscheduler.schedulers.blocking import BlockingScheduler

import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import rc


class TexBot(Plugin):
    async def handle(self) -> None:
        command = self.event.message.get_plain_text()
        command_args = command[5:]
        plt.clf()
        plt.rc('text', usetex=True)
        # plt.rcParams["figure.figsize"] = (8, 5)
        plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern Roman'], 'size': 32})
        plt.text(0.5, 0.5, "$" + r"\displaystyle " + command_args + "$", horizontalalignment='center',
                 verticalalignment='center')
        plt.axis('off')
        plt.savefig("temp.png")
        plt.close()
        await self.bot.get_adapter("mirai").call_api("sendGroupMessage", group=from_group,
                                                     messageChain=[{"type": "Image",
                                                                    "path": rf"C:\Users\qjtyk\PycharmProjects\QBot-SuXi\temp.png"}])

    async def rule(self) -> bool:
        global from_who, from_group
        if self.event.adapter.name != "mirai":
            return False
        if self.event.message.startswith("/tex"):
            from_who = self.event.sender.id
            from_group = self.event.sender.group.id
            return True
