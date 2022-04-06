import requests
import json
from cls_HttpReq import HttpR
import hashlib
from pprint import pprint

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
            pprint(json_data)

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

        print(result)

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

        print(result)

        return result.json()

    def get_photo_f_profile(self, fid: str) -> dict:
        """
        Gets a current user's data by user id
        """
        # Get a signature.
        sig = self.get_sig(application_key=self.public_key,
                           fid=fid,
                           format="json",
                           method='photos.getPhotos' + self.session_secret_key)

        print(f"sig: {sig}")

        result = requests.get(url=self.url_,
                              params={"application_key": self.public_key,
                                      "fid": fid,
                                      "format": "json",
                                      "method": "photos.getPhotos",
                                      "sig": sig,
                                      "access_token": self.token},
                              timeout=5)

        print(result)

        self.get_photo_inf(fid, result.json())

        return result.json()

    def get_photo_inf(self, fid: str, photo_list_json: dict) -> dict:
        """
        Gets a current user's data by user id
        """
        print('photo_list_json:')
        pprint(photo_list_json)
        print('photo_list:')

        photo_list = [photo['id'] for photo in photo_list_json['photos']]

        pprint(photo_list)

        for photo in photo_list:

            # Get a signature.
            #  application_key=CIMDIKKGDIHBABABAformat=jsonmethod=photos.getPhotoInfophoto_id=915269097285e86663104a0b9e79f081647af1a2ffe2
            sig = self.get_sig(application_key=self.public_key,
                               format="json",
                               method='photos.getPhotoInfo',
                               photo_id=photo + self.session_secret_key)

            print(f"sig: {sig}")

            result = requests.get(url=self.url_,
                                  params={"application_key": self.public_key,
                                          "format": "json",
                                          "method": "photos.getPhotoInfo",
                                          "photo_id": photo,
                                          "sig": sig,
                                          "access_token": self.token},
                                  timeout=5)

            pprint(result)
            pprint(result.json())

        # return result.json()

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

        return files_inf_list
