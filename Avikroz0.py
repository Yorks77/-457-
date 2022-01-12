from .. import loader, utils

class AvikRozMod(loader.Module):
    """Модуль регистрации на розыгрыш Avik"""
    strings = {'name': 'AvikRoz'}

    async def client_ready(self, client, db):
        self.db = db
        self.db.set("AvikRoz", "status", True)

    async def arcmd(self, message):
        """Используй: .ar чтобы включить ловлю розыгрышей от Педро."""
        status = self.db.get("AvikRoz", "status")
        if status is not True:
            await message.edit("<b>Ловля розыгрышей:</b> <code>Включена</code>")
            self.db.set("AvikRoz", "status", True)
        else:
            await message.edit("<b>Ловля розыгрышей:</b> <code>Отключена</code>")
            self.db.set("AvikRoz", "status", False)

    async def watcher(self, message):
        status = self.db.get("AvikRoz", "status")
        me = (await message.client.get_me()).id
        if status:
            if "розыгрыш на" in message.text.lower():
                chat = await message.client.get_entity(message.to_id)
                await message.click(0)
                await message.client.send_message(me, f"Я автоматически зарегистрировался в розыгрыше Avik, в чате: {chat.title}")