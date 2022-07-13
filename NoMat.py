import telebot
from datetime import datetime

file = open('mat.txt', 'r', buffering=-1, encoding="utf-8")
line_file = file.readlines()
line_file = str(line_file).strip('[]')
line = line_file.split(', ')
line = set(line)
file.close()


flag = False
dictr_users = {}

token = '5141555936:AAENS5n27O69-mtkDm6N5C2jBsV7nYl6KPE'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    global flag
    flag = True
    #user_status = bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    #print(user_status)
    #print(user_status.is_member)
    bot.send_message(message.chat.id, 'Поработаем с вашей речью!')

@bot.message_handler(commands=['hello'])
def hello_message(message):
    bot.send_message(message.chat.id, 'Привет. Я бот, который удаляет маты из вашего лексикона. Если я вижу мат в вашем сообщении то я его сразу удаляю. Запомни в моем присутствие лучше не выражаться! Для ознакомления с командами введите /info')
    
@bot.message_handler(commands=['info'])
def info_message(message):
    bot.send_message(message.chat.id, '/hello - информация о боте\n/statis - статистика по матам\n/time - дата и время\n/start - начать работу по удалению мата\n/stop - завершить работу по удалению мата')

@bot.message_handler(commands=['statis'])
def statis_message(message):
    global dictr_users
    statis_string = ''
    if dictr_users != {}:
        for key, value in dictr_users.items():
            statis_string =  statis_string + '@' + str(key) + ' 👉👉👉 ' + str(value) +'🤬\n'
    bot.send_message(message.chat.id, statis_string)

@bot.message_handler(commands=['time'])    #функция определения времени
def time_message(message):
    bot.send_message(message.chat.id, str(datetime.now()))

@bot.message_handler(commands=['stop'])
def stop_message(message):
    global flag
    global dictr_users
    flag = False
    dictr_users.clear()
    bot.send_message(message.chat.id, 'На этом закончим:)')
    #bot.stop_polling()

@bot.message_handler(content_types='text')
def processing_message(message):
    global flag
    global dictr_users
    if flag:
        user_name = message.from_user.username
        if user_name not in dictr_users.keys():
            dictr_users[user_name] = 0
        
        string = message.text
        string = string.lower()
        words = string.split(' ')
        replac = string.split(' ')
        words = set(words)
        cenz = words.intersection(line)
        if cenz != set():
            user_name = cenz_user_name = message.from_user.username
            for i, word in enumerate(replac):
                for cen in cenz:
                    if word == cen:
                        replac[i] = '*****'
            for key in dictr_users.keys():
                if  cenz_user_name == key:
                    dictr_users[key] =  dictr_users[key] + 1
                    break
            user_name = '@' + user_name + ' ,ТАК БУДЕТ ЛУЧШЕ: "' + str(replac).replace('[','').replace(']','').replace(',', '').replace('\'', '') + '"'
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, user_name)
            
        for key, value in dictr_users.items():
            if key == user_name and value >= 5:
                if message.text == "sorry":
                    dictr_users[key] = 0
                else:
                    try:
                        bot.delete_message(message.chat.id, message.message_id)
                    except:
                        print('message not found')
                    
bot.infinity_polling()
