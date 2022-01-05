"""
    Copyright 2021 t.me/innocoffee
    Licensed under the Apache License, Version 2.0
    
    Author is not responsible for any consequencies caused by using this
    software or any of its parts. If you have any questions or wishes, feel
    free to contact Dan by sending pm to @innocoffee_alt.
"""

#<3 title: TempChat
#<3 pic: https://img.icons8.com/fluency/48/000000/pause-squared.png
#<3 desc: Создает временный чат для, например, совместной работы над проектом

from .. import loader, utils
import asyncio
import json
import re
import datetime
import time
import telethon

# requires: json


@loader.tds
class TempChatMod(loader.Module):
    """Создаёт временный чат."""
    strings = {"name": "ВременныйЧат", 
    'chat_is_being_removed': '<b>🚫 Чат был удалён...</b>', 
    'args': '<b>PZD with args: </b><code>.help TempChat</code>', 
    'chat_not_found': '<b>Чат не найден</b>',
    'tmp_cancelled': '<b>Чат </b><code>{}</code><b> будет теперь жить вечно!</b>', 
    'delete_error': '<b>Ошибка удаления чата.Удалите вручную</b>', 
    'temp_chat_header': '<b>⚠️ Этот чат</b> (<code>{}</code>)<b> временный и будет удалён {}.</b>', 
    'chat_created': '<b>Чат был создан</b>',
    'delete_error_me': '<b>Произошла ошибка удаления{}</b>'}

    @staticmethod
    def s2time(temp_time):
        seconds, minutes, hours, days, weeks, months = 0, 0, 0, 0, 0, 0

        try:
            seconds = int(str(re.search('([0-9]+)s', temp_time).group(1)))
        except:
            pass

        try:
            minutes = int(
                str(re.search('([0-9]+)min', temp_time).group(1))) * 60
        except:
            pass

        try:
            hours = int(
                str(re.search('([0-9]+)h', temp_time).group(1))) * 60 * 60
        except:
            pass

        try:
            days = int(
                str(re.search('([0-9]+)d', temp_time).group(1))) * 60 * 60 * 24
        except:
            pass

        try:
            weeks = int(
                str(re.search('([0-9]+)w', temp_time).group(1))) * 60 * 60 * 24 * 7
        except:
            pass

        try:
            months = int(
                str(re.search('([0-9]+)m[^i]', temp_time).group(1))) * 60 * 60 * 24 * 31
        except:
            pass

        return round(time.time() + seconds + minutes + hours + days + weeks + months)

    async def chats_handler_async(self):
        while self.db.get('TempChat', 'loop', False):
            # await self.client.send_message('me', 'testing')
            for chat, info in self.chats.items():
                if int(info[0]) <= time.time():
                    try:
                        await self.client.send_message(int(chat), self.strings('chat_is_being_removed'))
                        async for user in self.client.iter_participants(int(chat), limit=50):
                            await self.client.kick_participant(int(chat), user.id)
                        await self.client.delete_dialog(int(chat))
                    except:
                        try:
                            await self.client.send_message(int(chat), self.strings('delete_error'))
                        except:
                            await self.client.send_message('me', self.strings('delete_error_me').format(info[1]))

                    del self.chats[chat]
                    self.db.set("TempChat", "chats", self.chats)
                    break
            await asyncio.sleep(.5)

    async def client_ready(self, client, db):
        self.db = db
        self.chats = self.db.get("TempChat", "chats", {})
        self.client = client
        self.db.set('TempChat', 'loop', False)
        await asyncio.sleep(1)
        self.db.set('TempChat', 'loop', True)
        asyncio.ensure_future(self.chats_handler_async())

    async def тчcmd(self, message):
        """.тч <время> <описание> - Создаёт новый временный чат
Форматы времени: 30s, 30мин, 1ч, 1д, 1неделя, 1месяц
30 сек, 30 мин, 1 час, 1 день, 1 неделя, 1 месяц"""
        args = utils.get_args_raw(message)
        if args == "":
            await utils.answer(message, self.strings('args', message))
            await asyncio.sleep(3)
            await message.delete()
            return

        if len(args.split()) < 2:
            await utils.answer(message, self.strings('args', message))
            await asyncio.sleep(3)
            await message.delete()
            return

        temp_time = args.split()[0]
        tit = args.split(' ', 1)[1].strip()

        until = self.s2time(temp_time)
        if until == round(time.time()):
            await utils.answer(message, self.strings('args', message))
            await asyncio.sleep(3)
            await message.delete()
            return

        res = await self.client(telethon.functions.messages.CreateChatRequest(users=['kanekiguard_tests_bot'], title=tit))
        await utils.answer(message, self.strings('chat_created', message))
        cid = res.chats[0].id

        await self.client.send_message(cid, self.strings('temp_chat_header', message).format(cid, datetime.datetime.utcfromtimestamp(until + 10800).strftime("%d.%m.%Y %H:%M:%S")))
        self.chats[str(cid)] = [until, tit]
        self.db.set("TempChat", "chats", self.chats)

    async def ткcmd(self, message):
        """.тк <время> - Делает текущий чат временным
Форматы времени: 30с, 30мин, 1ч, 1д, 1н, 1м
30 сек, 30 мин, 1 час, 1 день, 1 неделя, 1 месяц"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings('args', message))
            await asyncio.sleep(3)
            await message.delete()
            return

        until = self.s2time(args)
        if until == round(time.time()):
            await utils.answer(message, self.strings('args', message))
            await asyncio.sleep(3)
            await message.delete()
            return

        cid = utils.get_chat_id(message)

        await utils.answer(message, self.strings('temp_chat_header', message).format(cid, datetime.datetime.utcfromtimestamp(until + 10800).strftime("%d.%m.%Y %H:%M:%S")))
        self.chats[str(cid)] = [until, (await self.client.get_entity(cid)).title]
        self.db.set("TempChat", "chats", self.chats)


    async def тчлистcmd(self, message):
        """.тчлист - Список чатов"""
        res = "<b>= Temporary Chats =</b>\n<s>==================</s>\n"
        for chat, info in self.chats.items():
            res += f'<b>{info[1]}</b> (<code>{chat}</code>)<b>: {datetime.datetime.utcfromtimestamp(info[0] + 10800).strftime("%d.%m.%Y %H:%M:%S")}.</b>\n'
        res += "<s>==================</s>"

        await utils.answer(message, res)

    async def тчотменаcmd(self, message):
        """.тчотмена <айди | дополнительно> - Отключает удаление чата по айди."""
        args = utils.get_args_raw(message)
        if args not in self.chats:
            args = str(utils.get_chat_id(message))

        if args not in self.chats:
            await utils.answer(message, self.strings('chat_not_found', message))
            await asyncio.sleep(3)
            await message.delete()
            return

        await utils.answer(message, self.strings('tmp_cancelled', message).format(self.chats[args][1]))
        del self.chats[args]
        self.db.set("TempChat", "chats", json.dumps(self.chats))

    async def тчвремяcmd(self, message):
        """.тчвремя <айди> <новое_время>"""
        args = utils.get_args_raw(message)
        if args == "":
            await utils.answer(message, self.strings('args', message))
            await asyncio.sleep(3)
            await message.delete()
            return

        args = args.split()
        if len(args) == 0:
            await utils.answer(message, self.strings('args', message))
            await asyncio.sleep(3)
            await message.delete()
            return

        if len(args) >= 2:
            chat = args[0]
            new_time = self.s2time(args[1])
        else:
            chat = str(utils.get_chat_id(message))
            new_time = self.s2time(args[0])

        if chat not in list(self.chats.keys()):
            await utils.answer(message, self.strings('chat_not_found', message))
            await asyncio.sleep(3)
            await message.delete()
            return

        self.chats[chat][0] = new_time
        self.db.set('TempChat', 'chats', self.chats)
