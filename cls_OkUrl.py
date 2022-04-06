import time
import requests
import json
from cls_HttpReq import HttpR
import hashlib
from progress.bar import IncrementalBar

"""
This is the Odnoklassniki API communication class

Methods:
{api_server}fb.do?method=[method_name] - for example, https://api.ok.ru/fb.do?method=friends.get
or
{api_server}api/[method_group]/[method_name] - for example, https://api.ok.ru/api/friends/get
"""


class OkUrl(HttpR):
    url_ = "https://api.ok.ru/fb.do"

    def __init__(self, token_file_n: str):
        super().__init__(token_file_n)

        with open('ok_data.txt') as f:
            json_data = json.load(f)
            # pprint(json_data)

        self.application_iD = json_data['ApplicationID']
        self.public_key = json_data['PublicKey']
        self.secret_key = json_data['SecretKey']
        self.session_secret_key = json_data['SessionSecretKey']

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

    @staticmethod
    def get_sig(**kwargs):
        return hashlib.md5("".join([key + '=' + value for key, value in kwargs.items()]).encode('utf-8')).hexdigest()

    def get_current_user_personal_data(self) -> dict:
        """
        Gets a current user's data by user id
        """
        # Get a signature.
        sig = self.get_sig(application_key=self.public_key,
                           format='json',
                           method='users.getCurrentUser' + self.session_secret_key)

        result = requests.get(url=self.url_,
                              params={"application_key": "CIMDIKKGDIHBABABA",
                                      "format": "json",
                                      "method": "users.getCurrentUser",
                                      "sig": sig,
                                      "access_token": self.token},
                              timeout=5)

        return result.json()

    def get_personal_data(self, uid: str) -> dict:
        """
        Gets a current user's data by user id
        """
        # Get a signature.
        fields_ = "FIRST_NAME,PICGIF"
        sig = self.get_sig(application_key=self.public_key,
                           fields=fields_,
                           format='json',
                           method='users.getInfoByuid=' + uid + self.session_secret_key)

        result = requests.get(url=self.url_,
                              params={"application_key": "CIMDIKKGDIHBABABA",
                                      "fields": "FIRST_NAME,PICGIF",
                                      "format": "json",
                                      "method": "users.getInfoBy",
                                      "uid": uid,
                                      "sig": sig,
                                      "access_token": self.token},
                              timeout=5)

        return result.json()

    def get_photo_f_profile(self, fid: str) -> list:
        """
        Gets a current user's data by user id
        """
        # Get a signature.
        sig = self.get_sig(application_key=self.public_key,
                           fid=fid,
                           format="json",
                           method='photos.getPhotos' + self.session_secret_key)

        result = requests.get(url=self.url_,
                              params={"application_key": self.public_key,
                                      "fid": fid,
                                      "format": "json",
                                      "method": "photos.getPhotos",
                                      "sig": sig,
                                      "access_token": self.token},
                              timeout=5)

        result = self.get_photo_inf(result.json())

        return result

    def get_photo_inf(self, photo_list_json: dict) -> list:
        """
        Gets a current user's data by user id
        """
        photo_list = [photo['id'] for photo in photo_list_json['photos']]

        new_list = list()

        with IncrementalBar('Get file information:', max=len(photo_list)) as bar:

            for photo in photo_list:

                # Get a signature.
                sig = self.get_sig(application_key=self.public_key,
                                   format="json",
                                   method='photos.getPhotoInfo',
                                   photo_id=photo + self.session_secret_key)

                result = requests.get(url=self.url_,
                                      params={"application_key": self.public_key,
                                              "format": "json",
                                              "method": "photos.getPhotoInfo",
                                              "photo_id": photo,
                                              "sig": sig,
                                              "access_token": self.token},
                                      timeout=5)

                new_list.append(result.json())

                bar.next()
                time.sleep(0.4)

        return new_list

    @staticmethod
    def format_files_list(photo_list: list, qtt: int) -> list:

        # print('format_files_list')
        """
        Format a list of files_inf_list by template:
            [{
            "file_name": "34.jpg",
            "likes": "2"
            "data": "data"
            "url": url to download
            "size": "640x480"
            }]
        Make a list of files (files_list) for next
        """
        files_inf_list = list()

        for photo in photo_list:

            file_name = f"{photo['photo']['like_count']}.jpeg"

            # Collect the list of files.
            files_inf_list.append({'file_name': file_name,
                                   'likes': photo['photo']['like_count'],
                                   'date': photo['photo']['id'],
                                   'url': photo['photo']['pic640x480'],
                                   'size': '640x480',
                                   'width': ' '})

        if len(files_inf_list) < qtt:
            qtt = len(files_inf_list)

        files_inf_list = [files_inf_list[i] for i in range(qtt)]

        # Solve the file name conflict
        tmp_list = list()
        for file in files_inf_list:
            new_file_name = file['file_name']
            if new_file_name in tmp_list:
                new_file_name = f"{file['likes']}_{file['date']}.jpeg"
                file['file_name'] = new_file_name
            tmp_list.append(new_file_name)

        return files_inf_list
