import requests as requests

from user import User


class Finder:
    API_VERSION = "5.131"
    URL = 'https://api.vk.com/method/'
    token: str

    def __init__(self, token):
        self.token = token

    def __get_top_photos(self, vk_owner_id: str):
        photos_url = self.URL + 'photos.get'
        photos_params = {
            'extended': 1,
            'access_token': self.token,
            'v': self.API_VERSION,
            'album_id': 'profile',
            'owner_id': vk_owner_id
        }
        response = requests.get(photos_url, params=photos_params)
        json = response.json()
        photo_list = json['response']['items']
        sorted_photos_json = sorted(photo_list, key=lambda item: item['likes']['count'] + item['comments']['count'], reverse=True)
        top_photos = []
        for photo_json in sorted_photos_json[:3]:
            top_photos.append(photo_json['sizes'][-1]['url'])
        return top_photos

    def find_matches(self, age_from, age_to, city, sex, status) -> list:
        search_params = {
            'access_token': self.token,
            'count': 5,
            'fields': 'city,relation,sex',
            'city': city,
            'sex': sex,
            'age_from': age_from,
            'age_to': age_to,
            'status': status,
            'v': self.API_VERSION
        }
        response = requests.get(
            self.URL + "users.search",
            params=search_params)
        json = response.json()
        users = []
        for item in json['response']['items']:
            if not item['is_closed'] and 'city' in item is not None:
                user = User(item['id'],
                            item['first_name'],
                            item['last_name'],
                            item['city']['title'],
                            item['sex'],
                            status)
                users.append(user)

        for user in users:
            user.top_photos = self.__get_top_photos(user.id)
        return users






