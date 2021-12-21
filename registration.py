import requests
from datetime import date, datetime
import json
from pprint import pprint
from operator import itemgetter

class Registration:
    def get_sex(self, id):
        with open('tokenvk.txt', 'r') as file_object:
            tokenvk = file_object.read().strip()
        URL = 'https://api.vk.com/method/users.get'
        params = {
            'access_token' : tokenvk,
            'user_ids' : id,
            'v':'5.131',
            'fields' : 'bdate,about,city,relation,sex'
        }
        res = requests.get(URL, params=params)
        info = res.json()
        if 'sex' in info['response'][0].keys() :
            sex = int(info['response'][0]['sex'])
            if sex == 2:
                sex = 1
            else:
                sex = 2
        else:
            sex = input('Введите ваш пол М или Ж')
            if sex == 'М':
                sex = 1
            elif sex == 'Ж':
                sex = 2
        return sex  

    def get_city(self, id):
        with open('tokenvk.txt', 'r') as file_object:
            tokenvk = file_object.read().strip()
        URL = 'https://api.vk.com/method/users.get'
        params = {
            'access_token' : tokenvk,
            'user_ids' : id,
            'v':'5.131',
            'fields' : 'bdate,about,city,relation,sex'
        }
        res = requests.get(URL, params=params)
        info = res.json()
        if 'city' in info['response'][0].keys():
            city = info['response'][0]['city']['id']
        else:
            city = input('В каком городе вы живете?')
        return city

    def get_relation(self, id):
        with open('tokenvk.txt', 'r') as file_object:
            tokenvk = file_object.read().strip()
        URL = 'https://api.vk.com/method/users.get'
        params = {
            'access_token' : tokenvk,
            'user_ids' : id,
            'v':'5.131',
            'fields' : 'bdate,about,city,relation,sex'
        }
        res = requests.get(URL, params=params)
        info = res.json()
        if 'relation' in info['response'][0].keys():
            if info['response'][0]['relation'] == 1:
                relation = 'Не женат/не замужем'
            elif info['response'][0]['relation'] == 2:
                relation = 'есть друг/есть подруга'
            elif info['response'][0]['relation'] == 3:
                relation = 'помолвлен/помолвлена'
            elif info['response'][0]['relation'] == 4:
                relation = 'женат/замужем'
            elif info['response'][0]['relation'] == 5:
                relation = 'все сложно'
            elif info['response'][0]['relation'] == 6:
                relation = 'в активном поиске'
            elif info['response'][0]['relation'] == 7:
                relation = 'влюблен/влюблена'
            elif info['response'][0]['relation'] == 8:
                relation = 'в гражданском браке'
            elif info['response'][0]['relation'] == 0:
                relation = 'не указано'
        else:
            relation = input('Ваше семейное положение?') 
        return relation

    def get_age(self, id):
        with open('tokenvk.txt', 'r') as file_object:
            tokenvk = file_object.read().strip()
        URL = 'https://api.vk.com/method/users.get'
        params = {
            'access_token' : tokenvk,
            'user_ids' : id,
            'v':'5.131',
            'fields' : 'bdate,about,city,relation,sex'
        }
        res = requests.get(URL, params=params)
        info = res.json()
        today = date.today()
        if 'bdate' in info['response'][0].keys():
            bdate = info['response'][0]['bdate'].split('.')
            if len(bdate) == 3:
                birth_date = date(int(bdate[2]), int(bdate[1]), int(bdate[0]))
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            else:
                age = 'не указан возраст'
        else:
            age = 'не указан возраст'
        return age
if __name__ == '__main__':   
    registration = Registration()


