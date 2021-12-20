from .. import loader
from asyncio import sleep

@loader.tds
class EternalOnlineMod(loader.Module):
    """Вечный онлайн."""
    strings = {'name': 'Eternal Online'}

    def __init__(self):
        self.online = None

    async def onlineoncmd(self, message):
        """Включить вечный онлайн."""
        self.online = True
        await message.edit("Вечный онлайн включен.")
        while self.online:
            msg = await message.client.send_message('me', 'Онлайн')
            await msg.delete()
            await sleep(180)


    async def onlineoffcmd(self, message):
        """Выключить вечный онлайн."""
        self.online = False
        await message.edit("Вечный онлайн выключен.")