from time import sleep
import telebot 
from telebot import types
import os 
import re

bot = telebot.TeleBot('5432818658:AAHNCv2cCmy9f2L5aoxgJInct_kP0fZrvvk') #создание бота через токен от @FatherBot
print('Bot started') #вывод в консоль, чтобы понимать что бот запустился 

num = [] #глобальная переменная для работы с id студентов

@bot.message_handler(commands=['start']) #создаем обработку команды /start
def start(message): #основная функция работы команды
    with open ('./annotation/start.txt') as s: 
        content = s.read()
    bot.send_message(message.from_user.id, content) #в предыдущих строчках мы открыли текстовый файл с аннотацией и прочитали его, теперь отправляем пользователю
    sleep(1) #задержка, иначе сообщения будут приходить очень быстро
    bot.send_message(message.from_user.id, 'Если вы студент вам необходимо только зарегестрироваться - /reg')
    sleep(1)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создаем и заменяем клавиатуру пользователя на кнопки 
    btn1 = types.KeyboardButton(text = "/work") #создаем кнопку
    btn2 = types.KeyboardButton(text = "/help")
    btn3 = types.KeyboardButton(text = "/reg")
    markup.add(btn1, btn2, btn3) #собираем кнопки
    bot.send_message(message.from_user.id, 'Для начала работы от лица преподавателя и выбора группы напишите или нажите - /work', reply_markup=markup) #пием ответ пользователю заменив клавиатуру на кнопки


@bot.message_handler(commands=['work']) #функция для создания и обработки работы с кнопками и выбора групп преподавателю
def work(message):
    markup = types.ReplyKeyboardMarkup()
    directory = './groups'  #директория в которой хранятся файлы с id студентов из группы
    files = os.listdir(directory)
    for i in files:
        i = types.KeyboardButton(f'{i}') #создаем кнопки через цикл, чтобы вывести все группы
        markup.add(i)
    msg = bot.send_message(message.from_user.id, "Нажмите на кнопку и выберите группу ", reply_markup=markup)
    bot.register_next_step_handler(msg, snd_msg) #переходим к следующей функции

def snd_msg(message):
    global num
    fi = f'./groups/{message.text}'
    with open (fi, 'r') as file_group: #открываем и проверяем что все id настоящие 
        for inp_str in file_group:
            buf = re.findall(r'\d+', inp_str) 
            num += buf
        for i in num:
            for i in num:
                if (len(i) > 5):
                    continue
                else:
                    num.remove(i)
    msg = bot.send_message(message.from_user.id, 'Enter text to send: ') #вводим текст для отправки студентам
    bot.register_next_step_handler(msg, snd) #переходим к следующей функции
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) 
    btn1 = types.KeyboardButton(text = "/work")
    btn2 = types.KeyboardButton(text = "/help")
    markup.add(btn1, btn2)
    with open ('./annotation/after_work.txt', 'r') as a_w:
        content = a_w.read()
    bot.send_message(message.from_user.id, content, reply_markup=markup) #читаем и отправляем еще один файл аннотации


def snd(message): #в этой функции просто отправляем всем id студентов пересланное сообщение
    global num
    for i in num:
        bot.forward_message(i, message.from_user.id, message.message_id)

@bot.message_handler(commands=['reg'], content_types=['text']) #функция для создания и обработки работы с кнопками и выбора групп для студентов
def reg(message):
    directory = './groups' 
    files = os.listdir(directory) 
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Новая группа')
    markup.add(btn1)
    for i in files:
        i = types.KeyboardButton(f'{i}')
        markup.add(i)
    msg = bot.send_message(message.from_user.id, "Нажми на кнопку и выбери группу ", reply_markup=markup)
    if (msg.text == 'Новая группа') or (msg.text == btn1): #проверяем что если нажата новая группа - нужна другая функция
        bot.register_next_step_handler(msg, ngr)
    elif msg.text not in files: #если введен неверный текст вызвать помощь
        bot.register_next_step_handler(msg, help)
    else: #переходим в регистрацию студента
        bot.register_next_step_handler(msg, wrt)

def wrt(message): #проверяем зарегестрирован ли студент и если нет, регистрируем
    fi = f'.groups/{message.text}'
    registred = False
    with open (fi, 'r') as file_group:
        line = str(message.from_user.id) + ' - ' + str(message.from_user.username) + '\n'
        for i in file_group:
            if line in i:
                bot.send_message(message.from_user.id, 'Вы уже зарегестрированы')
                registred = True
        if not registred:
            with open (fi, 'a') as f_g:
                f_g.write(str(message.from_user.id) + ' - ' + str(message.from_user.username) + '\n')
            bot.send_message(message.from_user.id, 'Отлично! Теперь ты зарегестрирован')

def ngr(message): #записываем номер группы для создания нового файла
    msg = bot.send_message(message.from_user.id, 'Enter number of group in format: uis_111')
    bot.register_next_step_handler(msg, ntxt)

def ntxt(message): #создаем файл для новой группы и пишем ответ пользователю
    with open (f'./groups/{message.text}.txt', 'x') as f:
        bot.send_message(message.from_user.id, 'Отлично!  Группа создана! Теперь вернемся через /reg и зарегестрируемся в неё! ЖМИ!')

@bot.message_handler(commands=['help']) #обработчик команды help
def help(message):
    with open ('./annotation/help.txt', 'r') as h:
        content = h.read() 
    bot.send_message(message.from_user.id, content) #открываем файл с аннотацией и отправляем его содержимое пользователю 


bot.polling(none_stop=True, interval=0) #бесконечное обновление проверки новых сообщений от пользователя
