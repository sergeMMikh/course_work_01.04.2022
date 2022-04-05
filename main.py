from cls_VkUrl import VkUrl
# from cls_OkUrl import OkUrl
from cls_YaUploader import YaUploader
import file_exchange

# from pprint import pprint

if __name__ == '__main__':

    vk_token = input("Please input your vk token: \t")
    vk = VkUrl(vk_token)

    # to take a token from file
    # vk = VkUrl('vk_token.txt')

    vk_id = input("Input vk id: \t")
    album_name = input("Input a album name: \t")
    photo_quant = int(input("Input a quantity of photos: \t"))
    y_disc_token = input("Please input your yandex token: \t")
    yd_path = input("Input a yandex disc directory to save files: \t")

    # Get the photo list from user account.
    photo_lst = (vk.get_photo_f_profile(vk_id, album_name))

    if photo_lst != "Error":
        # Form the list of files.
        files_list = file_exchange.format_files_list(photo_lst, photo_quant)

        # Upload files to Yandex disk.
        y_disc = YaUploader(y_disc_token)

        # to take a token from file
        # y_disc = YaUploader('yd_token.txt')

        y_disc.upload_files_from_local(files_list=files_list, yd_path=yd_path)

    else:
        # Print "Error"
        print(photo_lst)

    # while True:
    #     command = input("Please choose the social net: \n('v'-VKontakte, 'o' -Odnoklassniki, 'q'- to quit): \t")
    #
    #     match command:
    #         case 'q':
    #             break
    #         case 'v':
    #             vk = VkUrl('vk_token.txt')
    #
    #             vk_id = input("Input vk id: \t")
    #             album_name = input("Input a album name: \t")
    #             photo_quant = int(input("Input a quantity of photos: \t"))
    #             yd_path = input("Input a yandex disc directory to save files: \t")
    #
    #             # Get the photo list from user account.
    #             photo_lst = (vk.get_photo_f_profile(vk_id, album_name))
    #
    #             if photo_lst != "Error":
    #                 # Form the list of files.
    #                 files_list = file_exchange.format_files_list(photo_lst, photo_quant)
    #
    #                 # Upload files to Yandex disk.
    #                 y_disc = YaUploader('yd_token.txt')
    #                 y_disc.upload_files_from_local(files_list=files_list, yd_path=yd_path)
    #
    #             else:
    #                 # Print "Error"
    #                 print(photo_lst)
    #         case 'o':
    #             ok = OkUrl('ok_token.txt')
    #             # ok_user_id = input("Input ok id: \t")
    #             ok_user_id = '178218028613'
    #
    #             pprint(ok.get_personal_data(ok_user_id))
