from .. import loader, utils

class RdnoRozMod(loader.Module):
    """Модуль регистрации на розыгрыш rdno."""
    strings = {'name': 'RdnoRoz'}

    async def client_ready(self, client, db):
        self.db = db
        self.db.set("RdnoRoz", "status", True)

    async def rdcmd(self, message):
        """Используй: .rd чтобы включить ловлю розыгрышей от rdno."""
        status = self.db.get("RdnoRoz", "status")
        if status is not True:
            await message.edit("<b>Ловля розыгрышей:</b> <code>Включена</code>")
            self.db.set("RdnoRoz", "status", True)
        else:
            await message.edit("<b>Ловля розыгрышей:</b> <code>Отключена</code>")
            self.db.set("RdnoRoz", "status", False)

    async def watcher(self, message):
        status = self.db.get("RdnoRoz", "status")
        me = (await message.client.get_me()).id
        if status:
            if "предлагает принять участие" in message.text.lower():
                chat = await message.client.get_entity(message.to_id)
                await message.click(0)
                await message.client.send_message(me, f"Я автоматически зарегистрировался в розыгрыше rdno, в чате: {chat.title}")