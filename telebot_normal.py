from time import sleep
import telebot 
from telebot import types

bot = telebot.TeleBot('5432818658:AAHNCv2cCmy9f2L5aoxgJInct_kP0fZrvvk')
print('Bot started')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 начать работу или /work")
    btn2 = types.KeyboardButton("❓ Задать вопрос или /help")
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, 'Здравствуйте!')
    sleep(1)
    bot.send_message(message.from_user.id, 'Вас приветствует бот-помощник преподавателя ИУЦТ')
    sleep(1)
    bot.send_message(message.from_user.id, 'Мой функционал пока ограничен, но мой создатель очень старается!')
    sleep(1)
    bot.send_message(message.from_user.id, 'Функционал бота - возможность одним сообщением отправить уведомления всей группе Ваших студентов!')
    sleep(1)
    bot.send_message(message.from_user.id, 'Для начала работы и выбора группы напишите или нажите - /work')
    

@bot.message_handler(commands=['work']) #функция для создания и обработки работы с кнопками и выбора групп
def work(message):
    markup = types.InlineKeyboardMarkup()
    buttons = ['g1', 'g2' ]
    for i in buttons:
        i = types.InlineKeyboardButton("Сайт Хабр(выбран для примера)", url='https://habr.com/ru/all/')
        markup.add(i)
    bot.send_message(message.from_user.id, "Нажми на кнопку и перейди на сайт".format(message.from_user.id), reply_markup=markup)


bot.polling(none_stop=True, interval=0) #listening to message from user
