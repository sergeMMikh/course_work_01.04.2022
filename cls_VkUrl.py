import requests
from pprint import pprint


class VkUrl:
    url_ = "https://api.vk.com/method/"

    def __init__(self):
        """
        Here program takes the TOKEN
        """
        with open('my_token.txt', 'r') as tfile:
            self.TOKEN = tfile.read().strip()
            print(f'TOKEN: {self.TOKEN}')

    def get_url(self, method: str):
        """
        This method just merge an default url and http method name.
        :param method:
        :return:
        """
        return self.url_ + method

    def get_params(self, fields: str, pdict: dict):
        """
        This method just merge http request parameters.
        :param fields:
        :param pdict:
        :return:
        """
        return {'access_token': self.TOKEN,
                'v': '5.81',
                'fields': fields} | pdict

    def search_groups(self, gr_name: str, sorting=0):
        """
        :param gr_name:
        :param sorting:
        :return:
        """
        result = requests.get(self.get_url(method="groups.search"),
                              params=self.get_params(
                                  fields='',
                                  pdict={'q': gr_name, 'sort': sorting, 'count': 10}),
                              timeout=5)

        print(result)

        result = result.json()['response']['items']

        return result

    def search_groups_by_id(self, sorting=0, *list_):
        """
        :param sorting:
        :param list_:
        :return:
        """
        result = requests.get(self.get_url(method="groups.getById"),
                              params=self.get_params(
                                  fields='members_count,activity,description',
                                  pdict={'group_ids': ','.join(str(idx) for idx in list_)}),
                              timeout=5)

        print(result)

        # pprint(result.json())

        result = result.json()['response']

        return result

    def get_personal_data(self, user_id: str):
        """
        :param user_id:
        :return: json()
        """
        result = requests.get(self.get_url(method="users.get"),
                              params=self.get_params(
                                  fields='education,photo_400_orig,contacts',
                                  pdict={'user_ids': user_id}),
                              timeout=5)

        # print(result)

        return result.json()

    def get_photo_f_profile(self, user_id: str) -> dict | str:

        """
        https://vk.com/dev/photos.get?params[owner_id]=-1&params[album_id]=wall&params[rev]=0&params[extended]=0
        &params[photo_sizes]=0&params[count]=2&params[v]=5.77
        :param user_id:
        :return: dict or str
        """

        owner_id = '-' + user_id
        print(owner_id)

        result = requests.get(self.get_url(method="photos.get"),
                              params=self.get_params(
                                  fields='',
                                  pdict={'owner_id': user_id,
                                         'album_id': 'wall',
                                         'count': '200',
                                         'photo_sizes': '1',
                                         'extended': '1'}),
                              timeout=5)

        print(result)
        # pprint(result.json())

        if result.status_code == 200 and 'error' not in result.json():
            return result.json()['response']['items']
        else:
            return f"Error"
