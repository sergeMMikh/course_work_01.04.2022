from cls_VkUrl import VkUrl
from pprint import pprint
# import requests
import cls_file_exchange

if __name__ == '__main__':

    vk = VkUrl()

    photo_lst = (vk.get_photo_f_profile('668524'))
    # pprint(photo_lst)
    if photo_lst != "Error":
        cls_file_exchange.format_files_list(photo_lst)
    else:
        print(photo_lst)

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
