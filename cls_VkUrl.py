import requests
from cls_HttpReq import HttpR


class VkUrl(HttpR):
    url_ = "https://api.vk.com/method/"

    def __init__(self, token_file_n: str):
        super().__init__(token_file_n)

    def get_url(self, method: str):
        """
        This method just merge an default url and http method name.
        """
        return self.url_ + method

    def get_params(self, fields: str, pdict: dict):
        """
        This method just merge http request parameters.
        """
        return {'access_token': self.token,
                'v': '5.81',
                'fields': fields} | pdict

    def search_groups(self, gr_name: str, sorting=0) -> dict:
        """
        Gets data of vk groups by group name.
        """
        result = requests.get(self.get_url(method="groups.search"),
                              params=self.get_params(
                                  fields='',
                                  pdict={'q': gr_name, 'sort': sorting, 'count': 10}),
                              timeout=5)

        print(result)

        result = result.json()['response']['items']

        return result

    def search_groups_by_id(self, *list_) -> dict:
        """
        Gets data of vk groups by group id.
        """
        result = requests.get(self.get_url(method="groups.getById"),
                              params=self.get_params(
                                  fields='members_count,activity,description',
                                  pdict={'group_ids': ','.join(str(idx) for idx in list_)}),
                              timeout=5)

        result = result.json()['response']

        return result

    def get_personal_data(self, user_id: str) -> dict:
        """
        Gets a user's data by user id
        """
        result = requests.get(self.get_url(method="users.get"),
                              params=self.get_params(
                                  fields='education,photo_400_orig,contacts',
                                  pdict={'user_ids': user_id}),
                              timeout=5)

        return result.json()

    def get_photo_f_profile(self, user_id: str, album_name: str) -> dict | str:

        """
        Gets a user's photos data by user id
        """
        result = requests.get(self.get_url(method="photos.get"),
                              params=self.get_params(
                                  fields='',
                                  pdict={'owner_id': user_id,
                                         'album_id': album_name,
                                         'count': '200',
                                         'photo_sizes': '1',
                                         'extended': '1'}),
                              timeout=5)

        if result.status_code == 200 and 'error' not in result.json():
            return result.json()['response']['items']
        else:
            return f"Error"

    def search_albums(self, user_id: str) -> dict:
        """
        Gets data of vk groups by group name.
        """
        result = requests.get(self.get_url(method="photos.getAlbums"),
                              params=self.get_params(
                                  fields='',
                                  pdict={'owner_id': user_id}),
                              timeout=5)

        result = result.json()

        return result
