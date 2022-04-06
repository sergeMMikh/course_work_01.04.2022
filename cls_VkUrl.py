import requests
from cls_HttpReq import HttpR

"""
This is the VKontakte API communication class
"""


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
        Gets albums list.
        """
        result = requests.get(self.get_url(method="photos.getAlbums"),
                              params=self.get_params(
                                  fields='',
                                  pdict={'owner_id': user_id}),
                              timeout=5)

        result = result.json()

        return result

    @staticmethod
    def format_files_list(photo_list: dict, qtt: int) -> list:
        """
        Format a list of files_inf_list by template:
            [{
            "file_name": "34.jpg",
            "data": "data"
            "url": url to download
            "size": "z"
            "width": width of photo
            }]
        Make a list of files (files_list) for next
        """
        files_inf_list = list()

        for photo in photo_list:
            # Choose the best resolution photo
            max_photo = max(photo['sizes'], key=lambda size: int(size['width']))

            file_name = f"{photo['likes']['count']}.jpeg"

            # Collect the list of files.
            files_inf_list.append({'file_name': file_name,
                                   'date': photo['date'],
                                   'url': max_photo['url'],
                                   'size': max_photo['type'],
                                   'width': max_photo['width']})

        files_inf_list.sort(key=lambda x: int(x['width']), reverse=True)

        if len(files_inf_list) < qtt:
            qtt = len(files_inf_list)

        print(f"qtt: {qtt}")
        files_inf_list = [files_inf_list[i] for i in range(qtt)]

        # Solve the file name conflict
        tmp_list = list()
        for file in files_inf_list:
            new_file_name = file['file_name']
            if new_file_name in tmp_list:
                new_file_name = f"{file['likes']['count']}_{file['date']}.jpeg"
                file['file_name'] = new_file_name
            tmp_list.append(new_file_name)

        return files_inf_list
