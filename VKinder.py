from random import randrange
from vk_api import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
from datetime import date, datetime
import json
from pprint import pprint
from operator import itemgetter
from registration import Registration
import psycopg2
from findperson import GetPhoto
from database import Get_id

with open('token_group.txt', 'r') as file_object:
    token_group = file_object.read().strip()

vk = vk_api.VkApi(token=token_group)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        id_client = event.user_id
        if event.to_me:
            request = event.text

            if request.lower() == "привет":
                write_msg(event.user_id, f"Хай, {event.user_id}, чтобы найти пару напишите 'найти пару' ")
            elif request == "найти пару":
                sex = Registration.get_sex(Registration, id_client) 
                city = Registration.get_city(Registration, id_client)
                age = Registration.get_age(Registration, id_client)
                person_id = Get_id.find_person(Get_id,sex,city,age,event.user_id)
                url_photo = GetPhoto.get_photo(GetPhoto,person_id)
                # write_msg(event.user_id, f'Ссылка https://vk.com/id{person_id}, Лучшие фото ({},{},{})'.format(url_photo[0],url_photo[1],url_photo[2]))
                write_msg(event.user_id, f'Ссылка https://vk.com/id{person_id}')
                for i in range(len(url_photo)):
                    write_msg(event.user_id, f'Лучшее фото № {i+1} ({url_photo[i]})')
            else:
                write_msg(event.user_id, "Не понял вашего ответа...")

