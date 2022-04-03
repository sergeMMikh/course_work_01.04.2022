from cls_VkUrl import VkUrl
from cls_YaUploader import YaUploader
from pprint import pprint
# import requests
import file_exchange

if __name__ == '__main__':

    vk = VkUrl()

    vk_id = '668524'
    # vk_id = input("Input vk id: \t")

    photo_quant = int(input("Input a quantity of photos: \t"))

    photo_lst = (vk.get_photo_f_profile(vk_id))
    if photo_lst != "Error":
        files_list = file_exchange.format_files_list(photo_lst, photo_quant)
        pprint(files_list)

        y_disc = YaUploader()
        y_disc.upload_files_from_local(files_list=files_list, yd_path='test')

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

    input("Close?")
