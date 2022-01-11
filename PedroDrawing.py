from .. import loader, utils

class PedroDrawingMod(loader.Module):
    """Модуль регистрации на розыгрыш педро. [SPECIAL] creator seen"""
    strings = {'name': 'PedroDrawing'}

    async def client_ready(self, client, db):
        self.db = db
        self.db.set("PedroDrawing", "status", True)

    async def pdcmd(self, message):
        """Используй: .pd чтобы включить ловлю розыгрышей от Педро."""
        status = self.db.get("PedroDrawing", "status")
        if status is not True:
            await message.edit("<b>Ловля розыгрышей:</b> <code>Включена</code>")
            self.db.set("PedroDrawing", "status", True)
        else:
            await message.edit("<b>Ловля розыгрышей:</b> <code>Отключена</code>")
            self.db.set("PedroDrawing", "status", False)

    async def watcher(self, message):
        status = self.db.get("PedroDrawing", "status")
        me = (await message.client.get_me()).id
        if status:
            if "устраивает розыгрыш" in message.text.lower():
                chat = await message.client.get_entity(message.to_id)
                await message.click(0)
                await message.client.send_message(me, f"Я автоматически зарегестрировался в розыгрыше, в чате: {chat.title}")