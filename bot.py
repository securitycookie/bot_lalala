import json
from random import randint
import requests
import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll

session = requests.Session()
vk_session = vk_api.VkApi(token = '*')
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
