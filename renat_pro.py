import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import datetime
import asyncio
import aiohttp
import traceback
import pyshorteners
import sqlite3
import random

bot = AsyncTeleBot('')
connect = sqlite3.connect('dz.db', check_same_thread = False)
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS dz(
	predmet TEXT,
	dz TEXT,
	url TEXT,
	files TEXT
	)
""")
connect.commit()

SUBJECTS = ['алгебра', 'математика(внеурочка)', 'планиметрия','биология', 'вероятности', 'география', 'геометрия', 'английскому языку(виноградова)', 'английскому языку(цыбина)', 'индивидуальный проект', 'информатика(гильдин)', 'информатика(низамова)', 'история', 'литература', 'обществознание', 'обзр', 'родной язык', 'родная литература', 'русский язык', 'физика', 'химия']

RASP = [{'2-3': 'обществознание', '4;7': 'геометрия', '5a-6a': 'английский язык(виноградова)', '5b-6b': 'английский язык(цыбина)', '8': 'планиметрия'}, #понедельник
		{'1': 'биология', '2': 'литература', '5': 'химия', '6-7': 'алгебра', '8': 'математика(внеурочка)'}, #вторник
		{'1-2': 'история', '3-4': 'физика', '5a-6a': 'информатика(гильдин)', '5b-6b': 'информатика(низамова)', '7': 'русский язык', '8': 'литература'}, #среда
		{'2a': 'английский язык(виноградова)', '2b': 'английский язык(цыбина)', '3-4': 'алгебра', '5': 'география', '6-7': 'физика', '8': 'математика(внеурочка)', '9': 'обзр'}, #четверг
		{'1': 'родная литература', '2': 'русский язык', '3': 'геометрия', '4': 'вероятности', '5': 'родной язык', '6': 'литература', '7': 'физика', '8': 'математика(внеурочка)', '9': 'индивидуальный проект'} #пятница
	]

ADMIN_ID = 0
CHAT_ID = 0
THREAD_ID = 0
CHAT_PUBLIC_ID = 0

login, password = '', ''

DAYS = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
IMAGES = ['https://imgur.com/HHOTR4a.jpg']

@bot.message_handler(commands=['eat'])
async def func12355(message):
	#print('DA')
	if message.from_user.id != ADMIN_ID:
		return
	while True:
		try:
			n = datetime.datetime.now()
			#print(n)
			if n.hour >= 18: #18 utc+3 
				#print('trying...')
				d = datetime.datetime.today().weekday()
				tomorrow = datetime.date.today() + datetime.timedelta(days=1)
				t = f'{tomorrow.day}.{tomorrow.month}.{tomorrow.year}'
				if d in [6, 0, 1, 2, 3]:
					await bot.send_photo(chat_id = CHAT_ID, message_thread_id = THREAD_ID, photo = random.choice(IMAGES), caption = f'<b>❗Отметьтесь в Сферуме, кто питается завтра ({DAYS[(d+1) % 7]})</b>\n\nЕсли вы первый, кто отмечается, создайте опрос с такими настройками:\n\nТема опроса: "<code>Будете ли вы обедать завтра ({t})?</code>"\nВарианты ответа: "<code>Да</code>" и "<code>Хочу узнать результаты опроса</code>".\nДругие параметры опроса настраивать не нужно.\n\n<i>P.S. Это сообщение отправляется ботом в качестве напоминания, поэтому, если завтра мы по какой-то причине не обедаем, не нужно ничего создавать.</i>', parse_mode='html')
					await asyncio.sleep(50000)
		except:
			print(traceback.format_exc())
		await asyncio.sleep(20)

@bot.message_handler(commands=['work'])
async def func(message):
	if message.from_user.id != ADMIN_ID:
		return
	while True:
		try:
			n = datetime.datetime.now()
			#print(n)
			if n.hour >= 13 and n.minute >= 30 or n.hour >= 14:
				#print('trying...')
				d = datetime.datetime.today().weekday()
				if d == 4:
					d = -1
				date = 'следующий день'
				#пока эж не робит
				# s, date = await get_dz(d+2)
				# print(s)
				# try:
				# 	await bot.send_photo(chat_id = CHAT_ID, message_thread_id = THREAD_ID, photo = 'https://imgur.com/m0B8XWn.jpg', caption = f'<strong>📚Домашнее задание по версии ЭЖ</strong> на {date}\n\n{s}', parse_mode='html')
				# except:
				# 	print(traceback.format_exc())
				# 	await bot.send_message(chat_id = CHAT_ID, message_thread_id = THREAD_ID, text = f'<a href="https://imgur.com/m0B8XWn.jpg">📚</a><strong>📚Домашнее задание по версии ЭЖ</strong> на {date}\n\n{s}', parse_mode='html')					
				

				r = RASP[d+1]
				s2 = ''
				flair = "✍"
				for k, v in r.items():
					cursor.execute("SELECT * FROM dz WHERE predmet=?", (v,))
					try:
						records = cursor.fetchall()
						dz1 = records[-1][1]
						url = records[-1][2]
						file = records[-1][3]
						if file:
							s2+=f"<ins>{k}.) {v[0].upper()+v[1:]}</ins>: <a href='{url}'>{flair}</a>{dz1};\n<a href='{file}'>📎Прикреплённый файл</a>\n"							
						else:
							s2+=f"<ins>{k}.) {v[0].upper()+v[1:]}</ins>: <a href='{url}'>{flair}</a>{dz1};\n"
					except:
						#print(traceback.format_exc())
						pass
				try:
					await bot.send_photo(chat_id = CHAT_ID, message_thread_id = THREAD_ID, photo = 'https://imgur.com/tKcrzAD.jpg', caption = f'<strong>📚Домашнее задание по версии группы ДЗ</strong> на {date}\n\n{s2}', parse_mode='html')
				except:
					print(traceback.format_exc())
					await bot.send_message(chat_id = CHAT_ID, message_thread_id = THREAD_ID, text = f'<a href="https://imgur.com/tKcrzAD.jpg">📚</a><strong>Домашнее задание по версии группы ДЗ</strong> на {date}\n\n{s2}', parse_mode='html')					
				await asyncio.sleep(50000)
		except:
			print(traceback.format_exc())
		await asyncio.sleep(20)

async def get_dz(n):
	async with aiohttp.ClientSession() as session:
		url = 'https://elschool.ru/Logon/Index'
		user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
		async with session.get(url, headers = {'User-Agent': user_agent_val}, verify_ssl = False) as r:
			session.headers.update({'Referer':url})
			session.headers.update({'User-Agent':user_agent_val})
			_xsrf = None
			async with session.post(url, data={'login': login,'password': password,'_xsrf':_xsrf}) as post_request:
				#print(await post_request.text())
				async with session.get('https://elschool.ru/users/diaries', headers = {'User-Agent': user_agent_val}, verify_ssl = False) as r1:
					session.headers.update({'Referer':url})
					session.headers.update({'User-Agent':user_agent_val})
					s = await r1.text()
					#print(s)
					if n == 1:
						ur = s.split('<div class="navigation__nextweek">')[1].split('<a href="')[1].split('"')[0].replace("&amp;", "&")
						async with session.get(f'https://elschool.ru{ur}', headers = {'User-Agent': user_agent_val}, verify_ssl = False) as r11:
							session.headers.update({'Referer':url})
							session.headers.update({'User-Agent':user_agent_val})
							s = await r11.text()
					s1 = s.split('<tbody>')[1:]
					tbody = s1[n-1]
					s = ''
					s2 = tbody.split('<tr class="diary__lesson">')[1:]
					s22 = s2.copy()
					date = s22[0].split('<td class="diary__dayweek')[1].split('<p>')[1].split('</p>')[0].replace('&nbsp;&nbsp;&nbsp;', ' ')
					#print(len(s2))
					j = 0
					for lesson in s2:
						j+=1
						name = lesson.split('<div class="flex-grow-1">')[1].split('</div>')[0]
						work = lesson.split('<div class="diary__homework-text">')[1].split('</div>')[0].replace("&#167;", "§").replace("&quot;", '"').replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")
						try:
							f = lesson.split('<div class="diary__homework__teacher-file__wrapper">')[1].split('<a href="')[1].split('"')[0]
							#print(f)
							flag_file = True
							async with session.get(f'https://elschool.ru{f}#', headers = {'User-Agent': user_agent_val}, verify_ssl = False) as ft:
								txt = await ft.text()
								ID = txt.split('var Parametrs =')[1].split("?Id=")[1].split('+')[1].split('+')[0].strip().lstrip()
								LESSON_ID = txt.split('var Parametrs =')[1].split("&LessonId=")[1].split('+')[1].split('+')[0].strip().lstrip()
								TITLE = txt.split('var Parametrs =')[1].split("&title=")[1].split('+')[1].split('+')[0].strip().lstrip()
								INS_ID = txt.split('var Parametrs =')[1].split("&InstituteId=")[1].split('+')[1].split('+')[0].strip().lstrip()
								DEP_ID = txt.split('var Parametrs =')[1].split("&DepartmentId=")[1].split('+')[1].split('+')[0].strip().lstrip()
								TOKEN = txt.split('var Parametrs =')[1].split("&token=")[1].split('+')[1].split('+')[0].strip().lstrip()
								TYPE = txt.split('var Parametrs =')[1].split("&Type=")[1].split('+')[1].split(';')[0].strip().lstrip()
								ur = 'https://file.elschool.ru/api/LessonToTeacherFile/' + '?Id=' +  ID + "&LessonId=" + LESSON_ID + "&title=" + TITLE[1:-1] + "&InstituteId=" + INS_ID[1:-1] + "&DepartmentId=" + DEP_ID[1:-1] + "&token=" + TOKEN[1:-1] + "&Type=" + TYPE[1:-1]
								ur_short = pyshorteners.Shortener().clckru.short(ur)
						except:
							flag_file = False
							#print(traceback.format_exc())
						flair = "✍"
						if not work:
							work='<em>ДЗ отсутствует</em>'
							flair = ""
						if flag_file:
							s+=f"<ins>{j}.) {name.split('.')[1][1:]}</ins>: {flair}{work};\n<a href='{ur_short}'>📎Прикреплённый файл</a>\n"
						else:
							s+=f"<ins>{j}.) {name.split('.')[1][1:]}</ins>: {flair}{work};\n"
					return s, date

@bot.message_handler(commands=['id'])
async def id(message):
	print(message.chat.id, message.message_thread_id)
	await bot.reply_to(message, 'done')

@bot.callback_query_handler(lambda call: call.data == 'dz_right')
async def right(call):
	message = call.message.reply_to_message
	predm = await get_predmet(message)
	dz = ':'.join(message.text.split(':')[1:]).strip()
	url = f"https://t.me/c/{CHAT_PUBLIC_ID}/1/{message.message_id}"
	file = ''
	cursor.execute("DELETE FROM dz WHERE predmet=?", (predm,))
	connect.commit()
	cursor.execute("INSERT INTO dz VALUES(?,?,?,?);", [predm, dz, url, file])
	connect.commit()
	await bot.delete_message(call.message.chat.id, call.message.message_id)
	await bot.set_message_reaction(message.chat.id, message.message_id, [types.ReactionTypeEmoji('👌')])

@bot.callback_query_handler(lambda call: call.data == 'cancel')
async def cancel(call):
	await bot.answer_callback_query(call.id, '👌Отправьте ДЗ в чат ещё раз')
	await bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.message_handler(content_types=["audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact"])
async def document(message):
	if message.reply_to_message and message.reply_to_message.text[0:5].lower() == 'дз по' and message.chat.id in [CHAT_ID]:
		message_dz = message.reply_to_message
		predm = await get_predmet(message_dz)
		dz = ':'.join(message_dz.text.split(':')[1:]).strip()
		url = f"https://t.me/c/{CHAT_PUBLIC_ID}/1/{message_dz.message_id}"
		file = f"https://t.me/c/{CHAT_PUBLIC_ID}/1/{message.message_id}"
		cursor.execute("DELETE FROM dz WHERE predmet=?", (predm,))
		connect.commit()
		cursor.execute("INSERT INTO dz VALUES(?,?,?,?);", [predm, dz, url, file])
		connect.commit()
		await bot.set_message_reaction(message.chat.id, message.message_id, [types.ReactionTypeEmoji('👌')])

@bot.message_handler(content_types=['text'])
async def dz(message):
	if message.text[0:5].lower() == 'дз по' and int(message.chat.id) in [CHAT_ID]:
		#print('yes')
		predm = await get_predmet(message)
		dz = ':'.join(message.text.split(':')[1:]).strip()
		#cursor.execute("DELETE FROM dz WHERE predm=?", (predm,))
		#connect.commit()
		#cursor.execute("INSERT INTO dz VALUES(?,?);", [predm, dz])
		#connect.commit()
		m = types.InlineKeyboardMarkup()
		m.add(types.InlineKeyboardButton(text='✅Записать ДЗ', callback_data='dz_right'), types.InlineKeyboardButton(text='❌Отменить', callback_data='cancel'))
		await bot.reply_to(message, f'👀Проверьте правильность данных:\n\n<b>Предмет:</b> <code>{predm}</code>\n<b>ДЗ:</b> <code>{dz}</code>', reply_markup = m, parse_mode='html')

async def get_predmet(message):
	try:
		if message.text[0:5].lower() == 'дз по':
			predm = message.text.split(':')[0][6:].lower()
			t1 = super_ai1(predm)
			t2 = super_ai2(predm)
			res = {}
			h = 1
			for k, v in t1.items():
				try:
					res[k][0] += h
					res[k][1] += v
				except:
					res[k] = [h, v]
				h+=1
			h=1
			for k, v in t2.items():
				try:
					res[k][0] += h
					res[k][1] += v
				except:
					res[k] = [h, v]
				h+=1
			#print(res)
			res = [k for k, v in sorted(res.items(), key=lambda item: item[1][1], reverse=True)]
			#print(res)
			if res[0] == 'английскому языку(виноградова)':
				res[0] = 'английский язык(виноградова)'
			if res[0] == 'английскому языку(цыбина)':
				res[0] = 'английский язык(цыбина)'
			return res[0]
	except:
		print(traceback.format_exc())

def super_ai1(predmet: str):
	try:
		sp = {}
		for i in range(len(predmet)):
			for j in range(len(SUBJECTS)):
				if len(SUBJECTS[j]) > i and predmet[i] == SUBJECTS[j][i]:
					try:
						sp[SUBJECTS[j]] += 10
					except:
						sp[SUBJECTS[j]] = 10
		sp2 = {k: v for k, v in sorted(sp.items(), key=lambda item: item[1], reverse=True)}
		sp = [k for k, v in sorted(sp.items(), key=lambda item: item[1], reverse=True)]
		#print(sp2)
		return sp2
	except:
		print(traceback.format_exc())

def super_ai2(predmet: str):
	pr = []
	pr.extend(predmet)
	try:
		sp = {}
		for i in range(len(SUBJECTS)):
			s = SUBJECTS[i]
			sr = []
			sr.extend(s)
			for j in range(len(predmet)):
				symb = predmet[j]
				a, b = pr.count(symb), sr.count(symb)
				if a == b and len(s) > j and s[j] == symb:
					try:
						sp[s] += a * 10
					except:
						sp[s] = a * 10
				elif len(s) > j and s[j] == symb:
					try:
						sp[s] += 1
					except:
						sp[s] = 1
		sp2 = {k: v for k, v in sorted(sp.items(), key=lambda item: item[1], reverse=True)}
		sp = [k for k, v in sorted(sp.items(), key=lambda item: item[1], reverse=True)]
		#print(sp2)
		return sp2
	except:
		print(traceback.format_exc())


def super_ai11(predmet: str):
	try:
		sp = {}
		for i in range(len(predmet)):
			for j in range(len(SUBJECTS)):
				if len(SUBJECTS[j]) > i and predmet[i] == SUBJECTS[j][i]:
					try:
						sp[SUBJECTS[j]] += 10
					except:
						sp[SUBJECTS[j]] = 10
		sp2 = {k: v for k, v in sorted(sp.items(), key=lambda item: item[1], reverse=True)}
		sp = [k for k, v in sorted(sp.items(), key=lambda item: item[1], reverse=True)]
		#print(sp2)
		return sp
	except:
		print(traceback.format_exc())

def super_ai22(predmet: str):
	pr = []
	pr.extend(predmet)
	try:
		sp = {}
		for i in range(len(SUBJECTS)):
			s = SUBJECTS[i]
			sr = []
			sr.extend(s)
			for j in range(len(predmet)):
				symb = predmet[j]
				a, b = pr.count(symb), sr.count(symb)
				if a == b and len(s) > j and s[j] == symb:
					try:
						sp[s] += a * 10
					except:
						sp[s] = a * 10
				elif len(s) > j and s[j] == symb:
					try:
						sp[s] += 1
					except:
						sp[s] = 1
		sp2 = {k: v for k, v in sorted(sp.items(), key=lambda item: item[1], reverse=True)}
		sp = [k for k, v in sorted(sp.items(), key=lambda item: item[1], reverse=True)]
		#print(sp2)
		return sp
	except:
		print(traceback.format_exc())

asyncio.run(bot.polling(none_stop=True, interval=0))
