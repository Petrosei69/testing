#Подлкючаем библиотеку requests
import json
import requests
import telegram
#Подключаем нужные для бота модули из библиотеки telegram.ext
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

token = "1614512010:AAG2EEsHeXkSDpyF7rE1MFLzzYe2I4i1fXc"

#это наша функция для получения адреса по координатам. С ней мы знакомы.
def get_address_from_coords(coords):
    PARAMS = {
        "apikey": "81341db1-4eae-4959-b845-073da1769876",
        "format": "json",
        "lang": "ru_RU",
        "kind": "house",
        "geocode": coords
    }

    try:
        r = requests.get(url="https://geocode-maps.yandex.ru/1.x/", params=PARAMS)
        json_data = r.json()
        address_str = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
            "GeocoderMetaData"]["AddressDetails"]["Country"]["AddressLine"]
        return address_str

    except Exception as e:
        #единственное что тут изменилось, так это сообщение об ошибке.
        return "Не могу определить адрес по этой локации/координатам.\n\nОтправь мне локацию или координаты (долгота, широта):"


#Эта функция будет использоваться когда человек первый нажал в боте START
def start(update, context):
    #эта строка отправляет сообщение пользователю с просьбой послать локацию или координаты
    update.message.reply_text('Отправь мне локацию или координаты (долгота, широта):')

#Эта функция будет использоваться, если пользователь послал в бота любой текст.
#Мы ожидаем координаты, но если прийдет что-то другое не страшно, ведь мы описали в функции получения адреса возвращение ошибки в случае чего.
def text(update, context):
    #получаем текст от пользователя
    coords = update.message.text
    #отправляем текст в нашу функцио получения адреса из координат
    address_str = get_address_from_coords(coords)
    #вовщращаем результат пользователю в боте
    update.message.reply_text(address_str)

#Эта функция будет использоваться, если пользователь послал локацию.
def location(update, context):
    #получаем обьект сообщения (локации)
    message = update.message
    #вытаскиваем из него долготу и ширину
    current_position = (message.location.longitude, message.location.latitude)
    #создаем строку в виде ДОЛГОТА,ШИРИНА
    coords = f"{current_position[0]},{current_position[1]}"
    #отправляем координаты в нашу функцию получения адреса
    address_str = get_address_from_coords(coords)
    #вовщращаем результат пользователю в боте
    update.message.reply_text(address_str)

def handler(event, context):
    body = json.loads(event['body'])
    chat_id = body['message']['from']['id']
    text = body['message']['text']
    send_message(chat_id, text)

    #send message function
def send_message(chat_id, text):
    url = 'https://api.telegram.org/bot1614512010:AAG2EEsHeXkSDpyF7rE1MFLzzYe2I4i1fXc/sendMessage'
    data = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, data=data)

#Это основная функция, где запускается наш бот
def main():
    #создаем бота и указываем его токен
    updater = Updater("1614512010:AAG2EEsHeXkSDpyF7rE1MFLzzYe2I4i1fXc", use_context=True)
    #создаем регистратор событий, который будет понимать, что сделал пользователь и на какую функцию надо переключиться.
    dispatcher = updater.dispatcher

    #регистрируем команду /start и говорим, что после нее надо использовать функцию def start
    dispatcher.add_handler(CommandHandler("start", start))
    #регистрируем получение текста и говорим, что после нее надо использовать функцию def text
    dispatcher.add_handler(MessageHandler(Filters.text, text))
    #регистрируем получение локации и говорим, что после нее надо использовать функцию def location
    dispatcher.add_handler(MessageHandler(Filters.location, location))
    #запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    #запускаем функцию def main
    main()