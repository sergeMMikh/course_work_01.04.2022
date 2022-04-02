# import time
# import BeautifulSoup
from cls_VkUrl import VkUrl
from pprint import pprint
# import dload
import requests

if __name__ == '__main__':

    vk = VkUrl()

    photo_list = (vk.get_photo_f_profile('668524'))
    pprint(photo_list)
    files_list = list()
    files_dict = {}
    if photo_list != "Error":
        """
            [{
            "file_name": "34.jpg",
            "size": "z"
            }]
        """

        for photo in photo_list:
            max_photo = max(photo['sizes'], key=lambda size: int(size['width']))
            file_name = f"{photo['likes']['count']}.jpeg"

            counter = 1
            new_file_name = file_name
            for file in files_list:
                if file_name in file['file_name']:
                    new_file_name = f"({counter}){file_name}"
                    counter += 1

            files_list.append({'file_name': new_file_name,
                               'url': max_photo['url'],
                               'size': max_photo['type']})

        pprint(files_list)




        # files_list = list([(max(photo['sizes'], key=lambda size: int(size['width'])))['url'] for photo in photo_list])
        # pprint(files_list)
        # counter = 0
        for f in files_list:
            r = requests.get(f['url'])
            # counter += 1
            with open(f['file_name'], 'wb') as f:
                f.write(r.content)

    else:
        print(photo_list)


    # pprint(vk.get_personal_data('668524'))
    # pprint(vk.search_groups('Python'))
    #
    # search_gr_res = vk.search_groups('Berloga')
    # target_group_list = []
    # #
    # print(result['screen_name'] for result in search_gr_res)
    #
    # for result in search_gr_res:
    #     print(result['screen_name'])
    #     target_group_list.append(result['id'])
    #
    # pprint(target_group_list)
    # pprint(vk.search_groups_by_id(*target_group_list))

    # input("Close?")

