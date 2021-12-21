import requests
from datetime import date, datetime
import json
from pprint import pprint
from operator import itemgetter
from registration import Registration
import psycopg2
class FindPerson:
    
    def find_person(self,sex,city,age,id_client):
        with open('tokenvk.txt', 'r') as file_object:
            tokenvk = file_object.read().strip()
        URL = 'https://api.vk.com/method/users.search'
        params = {
            'sex' : sex,
            'city' : city,
            'age_from' : age,
            'age_to' : age,
            'status' : 6,
            'has_photo' : 1,
            'access_token' : tokenvk,
            'v':'5.131'
        }
        con = psycopg2.connect(
            database = 'datausers',
            user = 'postgres',
            password = 'deman1997123',
            host = 'localhost',
            port = '5432'
        )
        cur = con.cursor()
        cur.execute(''' SELECT person_id 
                        FROM pair
                        WHERE id_client = {}'''.format(id_client))
        rows = cur.fetchall()
        res = requests.get(URL, params=params)
        info = res.json()
        i = 0
        a = False
        if rows == []:
            id_person = int(info['response']['items'][i]['id'])
        else:
            while a == False :
                b = info['response']['items'][i]['id']
                tuple = (b,)
                if (tuple in rows) or (info['response']['items'][i]['is_closed'] == True):
                    i += 1
                # elif info['response']['items'][i]['is_closed'] == False:
                #     i += 1
                else:
                   id_person = b
                   a = True

        cur.execute(''' INSERT INTO pair (id_client, person_id) VALUES ({}, {})'''.format(id_client, id_person) )
        con.commit()
        con.close()
        return id_person





    def get_photo(self, person_id):
        with open('tokenvk.txt', 'r') as file_object:
            tokenvk = file_object.read().strip()
        URL = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id' : person_id,
            'album_id' : 'profile',
            'extended' : 1,
            'access_token' : tokenvk,
            'v':'5.131'
        }
        data = {}
        res = requests.get(URL, params=params)
        info = res.json()
        dataphoto = []
        for i in range(len(info['response']['items'])):
            url = info['response']['items'][i]['sizes'][-1]['url']
            popular = (info['response']['items'][i]['likes']['count'] + info['response']['items'][i]['comments']['count'])
            dict = {'url':url,'popular':popular}
            dataphoto.append(dict)
        newlist = sorted(dataphoto, key=itemgetter('popular'),  reverse=True)
        url_photo = []
        top_photo = newlist[0:3]
        for a in top_photo: 
            for key,value in a.items():
                if key == 'url':
                    url_photo.append(value)
                elif key != 'url':
                    pass
        return url_photo


if __name__ == '__main__':
    id_client = int(input('Введите id:'))
    person = FindPerson()
    sex = Registration.get_sex(Registration, id_client)
    city = Registration.get_city(Registration, id_client)
    age = Registration.get_age(Registration, id_client)
    person_id = person.find_person(sex,city,age,id_client)
    person.get_photo(person_id)