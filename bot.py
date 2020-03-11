import json
from random import randint
import requests
import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll

session = requests.Session()
vk_session = vk_api.VkApi(token = '29ed229ab090ede80113f9772a88043205ac028cde2fb479dd6f03f1674af904b1568489b99ccacfd866d')
longPoll = VkLongPoll (vk_session)
vk = vk_session.get_api()

# Logging
log_info = "[INFO]:   "
log_warn = "[WARNING]:"
log_err  = "[ERROR]:  "

def log(log_type, msg):
    print(log_type, msg)
    if log_type == log_err:
        quit()

# User DB
class User(object):
    def __init__(self, uid = 0, lvl = 0):
        self.uid = uid
        self.lvl = lvl

    def level_up(self, points = 1):
        log(log_info, f'User {self.uid}: {self.lvl} ---> {self.lvl + 1}')
        self.lvl += points

    def level_zero(self):
        log(log_info, f'User {self.uid}: {self.lvl} ---> {0}')
        self.lvl = 0

    def __str__(self):
        return f'{self.uid}:{self.lvl}'

users = []

def load_db():
    log(log_info, 'Loading user database...')

    for line in open('./users.txt', 'r'):
        uid, level = (int(x) for x in line.split(':'))
        users += User(uid, level)
        log(log_info, f'User {line} loaded')

def update_db(user):
    global users
    if not user in users:
        file = open('./users.txt', 'w')
        file.write(f'{user.uid}:{user.lvl}')
        users.append(user)
        log(log_info, f"New user {str(user)}")

# Messages
msg_unknown = '???'

def level_0(msg):
    if msg in messages[0][0]:
        return 'Привет! Здесь ты можешь создавать тесты! Xочешь создать тест?'
    return msg_unknown

def level_1(msg):
    if msg in messages[1][0]:
        return 'Имя теста?'
    return msg_unknown

def level_2(msg):
    if msg[:10] in messages[2][0]:
        try:    open(f'{msg[10:]}.txt', 'r').close()
        except:
            open(f'{msg[10:]}.txt', 'w').close()
            return 'Тест создан :)'
        return 'Такой тест уже существует :)'

    return msg_unknown

messages = [
    (['привет', 'хай', 'hi', 'hello', 'приветики'], level_0),
    (['хочу создать тест', 'да', 'тест'], level_1),
    (['имя теста:'], level_2)
]

# Собсна логика сама

for event in longPoll.listen():
    if event.type !=  VkEventType.MESSAGE_NEW or not event.to_me:
        continue

    log(log_info, users)

    user = User(event.user_id)

    for u in users:
        if u.uid == event.user_id:
            user = u

    update_db(user)

    log(log_info, user)

    rsp = messages[user.lvl][1](event.text.lower())

    user.level_zero() if rsp == msg_unknown else user.level_up()

    vk.messages.send(user_id=event.user_id, random_id=randint(0,2**32), message=rsp)

"""
for event in longPoll.listen():
 if event.type ==  VkEventType.MESSAGE_NEW and event.to_me:
    idu = event.user_id
    lvl = check(idu, data)
    
    print(event.text, '--->', event.text.lower(), sep='')
    print(f'lvl: {lvl}, type(lvl): {type(lvl)}, idu: {idu}')

    response = ' '
    if lvl == 0:
        print('in lvl0')
        if event.text.lower() == 'привет' or event.text.lower() == 'хай' or event.text.lower() == 'hi' or event.text.lower() == 'hello' or event.text.lower() == 'приветики':
            response = 'привет! здесь ты можешь создавать тесты! Xочешь создать тест?'
            print(11)
            level(idu , data)
        else : 
            response = '???'
    elif lvl == 1:
        print(55)
        if event.text.lower() ==  'хочу создать тест' or event.text.lower() ==  'да' or event.text.lower() == 'тест':
            response = 'напиши имя своего теста: "имя текста:"'
            level(idu, data)
        else : 
            lvl = 0 
            response  = 'привет'
    elif lvl == 2:
        if event.text.lower() [0:11] == 'имя теста :':
            name = input()
            open (name+".txt", "w")
            response = 'напиши язык : "язык:'
            level(idu)
        else :
            lvl = 0
    elif lvl == 3:
        if event.text.lower() [0:5] == 'язык: ':
            open (name+".txt", "w" )
            language = input()
            response = 'напиши категорию'
            level(idu)
        else :
            lvl = 0
    elif lvl == 4 :
        if event.text.lower() [0:11] == 'категория: ':
            category = input()
            open (name+".txt","w")
            response = 'напиши свой первый вопрос : "вопрос 1 :"'
            level(idu)
        else:
            lvl = 0
    elif lvl == 5:
        if event.text.lower() [0:10] == 'вопрос 1 :':
            question1 = input()
            open (name+".txt","w" )
            response = 'напиши верный ответ на вопрос'
            level(idu)
        else:
            lvl = 0
    elif lvl == 6:
        if event.text.lower() [0:9] == 'ответ 1 :':
            answer1 = input()
            open (name+".txt", "w")
            response = 'напиши следующий вопрос'
            level(idu)
        else:
            lvl = 0
    elif lvl == 7 :
        if event.text.lower() [0:10] == 'вопрос 2 :':
            question2 = input()
            open (name+".txt","w" )
            response = 'напиши верный ответ на вопрос'
            level(idu)
        else :
            lvl = 0
    elif lvl == 8:
        if event.text.lower() [0:9] == 'ответ 2 :':
            answer2 = input()
            open (name+".txt", "w")
            response = 'напиши следующий вопрос'
            level(idu)
        else :
            lvl = 0
    elif lvl == 9 :
        if event.text.lower() [0:10] == 'вопрос 3 :':
            question2 = input()
            open (name+".txt", "w")
            response = 'напиши верный ответ на вопрос'
            level(idu)
        else :
            lvl = 0
    elif lvl == 10 :
        if event.text.lower() [0:9] == 'ответ 3 :':
            answer2 = input()
            open (name+".txt","w" )
        else:
            lvl = 0
        

    print(data)
    info = f'{event.user_id} от {event.text} '
    logging (info)
    print(response)       
    vk.messages.send(user_id=event.user_id, random_id=randint(0,2**32), message=response)
    #eval(input(">>> "))
"""