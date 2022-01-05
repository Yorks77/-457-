from .. import loader, utils

class AntiHelpMod(loader.Module):
	"""Отвечает всем на команду .help Ух ты юзер-бот. Модуль сделал @Friendly_telegram_userbot - @hecker_belugga"""
	strings = {"name":"AntiHelpMod"}
	
	async def client_ready(self, client, db):
		self.db = db
		self.db.set("AntiHelpMod", "status", True)

	
	async def antihelpcmd(self, message):
		status = self.db.get("AntiHelpMod", "status")
		if status is not False:
			self.db.set("AntiHelpMod", "status", False)
			await message.edit("<b>Анти-хелп выключен!</b>")
		else:
			self.db.set("AntiHelpMod", "status", True)
			await message.edit("<b>Анти-хелп включен</b>")
	
	
	async def watcher(self, message):
		status = self.db.get("AntiHelpMod", "status")
		me = (await message.client.get_me())
		if message.sender_id != me.id:
			if status is not False:
				if message.sender_id != me.id:
					if message.text.lower() == ".help":
						await message.reply("Ух ты юзер-бот!")