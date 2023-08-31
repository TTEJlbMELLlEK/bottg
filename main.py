import requests
from bs4 import BeautifulSoup as BS
import telebot
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from telebot import types

def find_teachers():
    teachersURL='http://nmt.edu.ru/html/cp.htm'
    teachers_request=requests.get(teachersURL)
    teachers_data=BS(teachers_request.content,'lxml')
    all_teachers_data=teachers_data.find('table',class_='inf')
    list_of_teachers=[]
    for item in all_teachers_data.find_all('tr'):
        pos1=str(item).find('href="')
        pos2=str(item).find('" title')
        pos3=str(item).find('Открыть расписание">')
        pos4=str(item).find('</a></td>')
        list_of_teachers.append(str(item)[pos3 + 20:pos4])
        list_of_teachers.append(str(item)[pos1 + 6:pos2])
    list_of_teachers.pop(0)
    list_of_teachers.pop(0)
    return list_of_teachers

teachers=find_teachers()


def check(bad):
    a = process.extract(bad, teachers,limit=3)
    return a
bot=telebot.TeleBot('6417564469:AAGenqpUkREAJn1ssGcQHsmrCMvUsMN4URc')
@bot.message_handler(content_types=['text'])
def choice(message):
    name_of_teacher_mb_bad=message.text
    name_of_teacher_good=check(name_of_teacher_mb_bad)
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1= types.KeyboardButton(name_of_teacher_good[0][0])
    btn2 = types.KeyboardButton(name_of_teacher_good[1][0])
    btn3 = types.KeyboardButton(name_of_teacher_good[2][0])
    markup.add(btn1,btn2,btn3)
    if name_of_teacher_mb_bad in teachers:
        bot.reply_to(message, 'http://nmt.edu.ru/html/' + teachers[teachers.index(name_of_teacher_mb_bad) + 1])
    else:
        bot.send_message(message.chat.id,'Выберите нужного преподавателя', reply_markup=markup)

        message2=message.text
        if message2 == name_of_teacher_good[0][0]:
            name_of_teacher=name_of_teacher_good[0][0]
        if message2== name_of_teacher_good[1][0]:
            name_of_teacher = name_of_teacher_good[1][0]
        if message2== name_of_teacher_good[2][0]:
            name_of_teacher=name_of_teacher_good[2][0]
        if name_of_teacher in teachers:
            bot.reply_to(message,'http://nmt.edu.ru/html/'+ teachers[teachers.index(name_of_teacher)+1])
    #bot.delete_message(message.chat.id, message.message_id+1)
bot.infinity_polling()








