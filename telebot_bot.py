from time import sleep
import telebot 

bot = telebot.TeleBot('5432818658:AAHNCv2cCmy9f2L5aoxgJInct_kP0fZrvvk')
print('Bot started')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, 'Здравствуйте!')
    sleep(2)
    bot.send_message(message.from_user.id, 'Вас приветствует бот-помощник преподавателя ИУЦТ')
    sleep(2)
    bot.send_message(message.from_user.id, 'Мой функционал пока ограничен, но мой создатель очень старается!')
    sleep(2)
    bot.send_message(message.from_user.id, 'Для начала предлагаем вам зарегестрироваться!')
    sleep(2)
    bot.send_message(message.from_user.id, 'Если вы готовы сделать это сейчас введите: рег или регистрация или /reg')

@bot.message_handler(commands=['reg'])
def reg(message):
    bot.send_message(message.from_user.id, 'Send your name')
    bot.register_next_step_handler(message, get_name)


def get_name(message): #получаем имя
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Send your surname')
    bot.register_next_step_handler(message, get_surname)

def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, f'You are {name} {surname}')
    bot.send_message(message, 'Glad to know you!')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.from_user.id, 'RN I only can /start /help /reg')

@bot.message_handler(content_types=['text'])
def text(message):
    if (message.text == 'рег') or (message.text == 'регистрация') or (message.text == '/reg'):
        bot.register_next_step_handler(message, reg)    
    else:
        bot.send_message(message.from_user.id, 'Can\'t understand you. Send /help')
bot.polling(none_stop=True, interval=0) #listening to message from user
