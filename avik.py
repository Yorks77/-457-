# for more info: Avikbank
# ©2021

import random
from .. import loader, utils
from datetime import timedelta
from telethon import functions
from telethon.tl.types import Message

@loader.tds
class FarmAvikMod(loader.Module):
	"""Для автоматического фарминга монет в авике"""
	strings = {
		'name': 'avikbot',
		'avikon': '<i>⏳Отложенка создана, автофарминг запущен, всё начнётся через 20 секунд...</i>',
		'avikon_already': '<i>Уже запущено</i>',
		'avikoff': '<i>❌Автофарминг остановлен.\n💵Собрано:</i> <b>%coins% $ </b>',
		'bank': '<i>💵Собрано:</i> <b>%coins% $</b>',
	}
	
	def __init__(self):
		self.name = self.strings['name']
		
	async def client_ready(self, client, db):
		self.client = client
		self.db = db
		self.myid = (await client.get_me()).id
		self.avik = 905604193
		
	async def avikoncmd(self, message):
		"""Запустить автофарминг"""
		status = self.db.get(self.name, "status", False)
		if status: return await message.edit(self.strings['avikon_already'])
		self.db.set(self.name, "status", True)
		await self.client.send_message(self.avik, "!бонускости 6", schedule=timedelta(seconds=20))
		await message.edit(self.strings['avikon'])
		
	async def avikoffcmd(self, message):
		"""Остановить автофарминг"""
		self.db.set(self.name, 'status', False)
		coins = self.db.get(self.name, 'coins', 0)
		if coins: self.db.set(self.name, 'coins', 0)
		await message.edit(self.strings['avikoff'].replace("%coins%", str(coins)))
		
	async def bankcmd(self, message):
		"""Вывод кол-ва валюты, за всё время работы этого модуля"""
		coins = self.db.get(self.name, "coins", 0)
		await message.edit(self.strings['bank'].replace("%coins%", str(coins)))
	
	async def watcher(self, event):
		if not isinstance(event, Message): return
		chat = utils.get_chat_id(event)
		if chat != self.avik: return
		status = self.db.get(self.name, 'status', False)
		if not status: return
		if event.raw_text == "!бонускости 6":
			return await self.client.send_message(self.avik, "!бонускости 6", schedule=timedelta(minutes=random.randint(1, 20)))
		if event.sender_id != self.avik: return
		if "Следующий бонускости через" in event.raw_text:
			args = [int(x) for x in event.raw_text.split() if x.isnumeric()]
			randelta = random.randint(20, 60)
			if len(args) == 4: delta = timedelta(hours=args[1], minutes=args[2], seconds=args[3]+randelta)
			elif len(args) == 3: delta = timedelta(minutes=args[1], seconds=args[2]+randelta)
			elif len(args) == 2: delta = timedelta(seconds=args[1]+randelta)
			else: return
			sch = (await self.client(functions.messages.GetScheduledHistoryRequest(self.avik, 1488))).messages
			await self.client(functions.messages.DeleteScheduledMessagesRequest(self.avik, id=[x.id for x in sch]))
			return await self.client.send_message(self.avik, '!бонускости 6', schedule=delta)
		if "Ваш бонус:" in event.raw_text or 'Ваш бонус:' in event.raw_text:
			args = event.raw_text.split()
			for x in args:
				if x[0] == '+': 
					return self.db.set(self.name, 'coins', self.db.get(self.name, 'coins', 0) + int(x[1:]))
