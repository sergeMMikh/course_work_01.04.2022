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

    def get_sig(self, **kwargs):
        return hashlib.md5("".join([key + '=' + value for key, value in kwargs.items()]).encode('utf-8')).hexdigest()

    def get_current_user_personal_data(self) -> dict:
        """
        Gets a current user's data by user id
        """
        # Get a signature.
        sig = self.get_sig(application_key= self.public_key,
                           format= 'json',
                           method= 'users.getCurrentUser' + self.session_secret_key)

        result = requests.get(url= self.url_,
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
        sig = self.get_sig(application_key= self.public_key,
                           fields= fields_,
                           format= 'json',
                           method= 'users.getInfoByuid='+ uid + self.session_secret_key)

        result = requests.get(url= self.url_,
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

    def get_photo_f_profile(self, uid: str) -> dict:
        """
        Gets a current user's data by user id
        """
        # Get a signature.
        fields_ = "FIRST_NAME,PICGIF"
        sig = self.get_sig(application_key= self.public_key,
                           fields= fields_,
                           format= 'json',
                           method= 'users.getInfoByuid='+ uid + self.session_secret_key)

        result = requests.get(url= self.url_,
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

