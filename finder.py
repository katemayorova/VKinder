import requests as requests

from user import User


class Finder:
    __API_VERSION = "5.131"
    __URL = 'https://api.vk.com/method/'
    __token: str

    __FIND_COUNT = 3
    __FIND_WINDOW = 5

    def __init__(self, token, persistence):
        self.__token = token
        self.persistence = persistence

    def __get_top_photos(self, vk_owner_id: int):
        photos_url = self.__URL + 'photos.get'
        photos_params = {
            'extended': 1,
            'access_token': self.__token,
            'v': self.__API_VERSION,
            'album_id': 'profile',
            'owner_id': vk_owner_id
        }
        response = requests.get(photos_url, params=photos_params)
        json = response.json()
        photo_list = json['response']['items']
        sorted_photos_json = sorted(photo_list, key=lambda item: item['likes']['count'] + item['comments']['count'], reverse=True)
        top_photos = []
        for photo_json in sorted_photos_json[:3]:
            top_photos.append(f'photo{photo_json["owner_id"]}_{photo_json["id"]}')
        return top_photos

    def get_city_id(self, city):
        city_id_url = self.__URL + 'database.getCities'
        city_id_params = {
            'access_token': self.__token,
            'v': self.__API_VERSION,
            'country_id': 1,
            'q': city
        }
        response = requests.get(city_id_url, params=city_id_params)
        response_json = response.json()
        if response_json['response']['count'] > 0:
            return response_json['response']['items'][0]['id']
        else:
            return -1

    def find_unique_matches(self, requester_id, age_from, age_to, city_id, sex, status) -> list:
        users = []
        offset = 0
        while len(users) < self.__FIND_COUNT:
            current_users = self.__find_matches(age_from, age_to, city_id, sex, status, self.__FIND_WINDOW, self.__FIND_WINDOW * offset)
            offset += 1
            unique_users = []
            for user in current_users:
                if self.persistence.check_uniqueness(user.vk_id, requester_id):
                    unique_users.append(user)
            users.extend(unique_users)
        users = users[:self.__FIND_COUNT]

        for user in users:
            user.top_photos = self.__get_top_photos(user.vk_id)
            self.persistence.save_match(user.vk_id, requester_id)
        return users

    def __find_matches(self, age_from, age_to, city_id, sex, status, count, offset) -> list:
        search_params = {
            'access_token': self.__token,
            'count': count,
            'offset': offset,
            'fields': 'city,relation,sex',
            'city': city_id,
            'sex': sex,
            'age_from': age_from,
            'age_to': age_to,
            'status': status,
            'v': self.__API_VERSION
        }
        response = requests.get(
            self.__URL + "users.search",
            params=search_params)
        json = response.json()
        users = []
        for item in json['response']['items']:
            if not item['is_closed'] and 'city' in item is not None:
                user = User(item['id'],
                            item['first_name'],
                            item['last_name'],
                            item['city']['title'],
                            User.SEX_MAPPING_REVERSE[item['sex']],
                            status)
                users.append(user)
        return users




