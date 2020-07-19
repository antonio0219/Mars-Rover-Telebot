# Mars Rover; marsrover_bot

import telebot, random
import requests

TOKEN = '993607592:AAGW2h2-sNO2akQ_R4OAZ_eJHehobf06Gzs' # TOKEN DEL BOT
tb = telebot.TeleBot(TOKEN)

# CONSTANTS
res = None
API_KEY = '7a8dOjjKtckW5kbU5UnvFd5uUpmoeMI4wOUHbL8y'
rover_list = ['curiosity', 'opportunity', 'spirit']

# VARIABLES
state = None
rover = None
data = None
cameras = []
camera = None
dicCamera = {}

# ORDERS


@tb.message_handler(commands=['start'])
def instructions(message):
	global state
	chatid = message.chat.id
	markup = telebot.types.InlineKeyboardMarkup()
	for i in rover_list:
		markup.add(telebot.types.InlineKeyboardButton(text=i, callback_data=i))
	tb.send_message(chatid, 'Selecciona rover:', reply_markup = markup)
	state = 'rover'


@tb.message_handler(commands=['getPhoto'])
def instructions(message):
	chatid = message.chat.id
	tb.send_message(chatid, 'Enviando foto...')
	tb.send_photo(chatid, data['photos'][0]['img_src'])

@tb.callback_query_handler(func=lambda call: True) # Para leer las respuestas de los botones
def query_handler(call):
	global state, rover, camera, data, dicCamera
	chatid = call.message.chat.id
	if state == 'rover':
		tb.send_message(chatid, 'Has seleccionado el ' + call.data)
		rover = call.data
		if call.data == 'curiosity':
			tb.send_message(chatid, 'Introduce la fecha en la Tierra en formato aaaa-m-d, teniendo en cuenta que el Curiosity lleva operativo desde el 6 de agosto de 2012')
		if call.data == 'spirit':
			tb.send_message(chatid, 'Introduce la fecha en la Tierra en formato aaaa-m-d, teniendo en cuenta que el Spirit aterrizó en Marte el 4 de enero de 2004 y su última comunicación con la Tierra fue el 22 de marzo de 2010')
		if call.data == 'opportunity':
			tb.send_message(chatid, 'Introduce la fecha en la Tierra en formato aaaa-m-d, teniendo en cuenta que el Opportunity aterrizó en Marte el 25 de enero de 2004 y su última comunicación con la Tierra fue el 13 de febrero de 2019')
		state = 'date'
	if state == 'camera':
		camera = call.data
		tb.send_photo(chatid, random.choice(dicCamera[camera])['img_src'])
		
@tb.message_handler(func=lambda message: True)
def echo_all(message):
	global state, res, data, cameras, dicCamera
	chatid = message.chat.id
	if state == 'date':
		res = requests.get('https://api.nasa.gov/mars-photos/api/v1/rovers/' + rover + '/photos?earth_date=' + message.text + '&api_key=' + API_KEY)
		data = res.json()		
		if len(data['photos']) == 0:
			tb.send_message(chatid, 'No se ha encontrado información de la fecha solicitada')
		else:
			for i in data['photos']:
				if i['camera']['full_name'] not in cameras:
					cameras.append(i['camera']['full_name'])
					dicCamera[i['camera']['full_name']] = []
				dicCamera[i['camera']['full_name']].append(i)
			markup = telebot.types.InlineKeyboardMarkup()
			for i in cameras:
				markup.add(telebot.types.InlineKeyboardButton(text=i, callback_data=i))
			tb.send_message(chatid, 'Selecciona la cámara para obtener una foto aleatoria de dicha cámara en esa fecha:', reply_markup = markup)
			state = 'camera'
	
tb.polling()
