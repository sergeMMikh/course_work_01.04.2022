import time
# import BeautifulSoup
import requests
from pprint import pprint


class VkUrl:
    url_ = "https://api.vk.com/method/"

    def __init__(self):
        with open('token.txt', 'r') as tfile:
            self.TOKEN = tfile.read().strip()
            print(f'TOKEN: {self.TOKEN}')

    def get_url(self, method: str):
        return self.url_ + method

    def get_params(self, fields: str, pdict: dict):
        return {'access_token': self.TOKEN,
                'v': '5.131',
                'fields': fields} | pdict

    def search_groups(self, gr_name: str, sorting=0):
        result = requests.get(self.get_url(method="groups.search"),
                              params=self.get_params(
                                  fields='',
                                  pdict={'q': gr_name, 'sort': sorting, 'count': 10}),
                              timeout=5)

        print(result)

        result = result.json()['response']['items']

        return result

    def search_groups_by_id(self, sorting=0, *list_):
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
        result = requests.get(self.get_url(method="users.get"),
                              params=self.get_params(
                                  fields='education,photo_400_orig,contacts',
                                  pdict={'user_ids': user_id}),
                              timeout=5)

        print(result)

        result = result.json()  # ['response'][0]

        return result

    def get_photo_profile(self, user_id: str) -> str:
        return "Ok"


if __name__ == '__main__':

    vk = VkUrl()

    pprint(vk.get_personal_data('id668524'))
    # pprint(search_groups('Python'))

    search_gr_res = vk.search_groups('Berloga')
    target_group_list = []
    #
    print(result['screen_name'] for result in search_gr_res)

    for result in search_gr_res:
        print(result['screen_name'])
        target_group_list.append(result['id'])

    pprint(target_group_list)
    pprint(vk.search_groups_by_id(*target_group_list))
