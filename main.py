from cls_VkUrl import VkUrl
from cls_OkUrl import OkUrl
from cls_YaUploader import YaUploader
import file_exchange

if __name__ == '__main__':

    while True:
        command = input("Please choose the social net: \n('v'-VKontakte, 'o' -Odnoklassniki, 'q'- to quit): \t")

        match command:
            case 'q':
                break
            case 'v':
                print("This program takes VK token from file 'vk_token.txt'")
                print("and Yandex token from file 'yd_token.txt'")

                vk = VkUrl('vk_token.txt')

                vk_id = input("Input vk id: \t")
                album_name = input("Input a album name: \t")
                photo_quant = int(input("Input a quantity of photos: \t"))
                yd_path = input("Input a yandex disc directory to save files: \t")

                # Get the photo list from user account.
                photo_lst = vk.get_photo_f_profile(vk_id, album_name)

                if photo_lst != "Error":
                    # Download files Form the list of files.
                    files_list = file_exchange.download_files(vk.format_files_list(photo_lst, photo_quant))

                    # Upload files to Yandex disk.
                    y_disc = YaUploader('yd_token.txt')
                    y_disc.upload_files_from_local(files_list=files_list, yd_path=yd_path)

                else:
                    # Print "Error"
                    print(photo_lst)

            case 'o':
                print("This program takes Odnoklassniki token from file 'ok_token.txt',")
                print("Yandex token from file 'yd_token.txt'")
                print("and other authorization data from file 'ok_data.txt'")
                ok = OkUrl('ok_token.txt')

                photo_quant = int(input("Input a quantity of photos: \t"))
                yd_path = input("Input a yandex disc directory to save files: \t")
                second_user = input("Input a Odnoklassniki user id: \t")

                photo_lst = ok.format_files_list(ok.get_photo_f_profile(fid=second_user), photo_quant)

                # Download files Form the list of files.
                files_list = file_exchange.download_files(photo_lst)

                # Upload files to Yandex disk.
                y_disc = YaUploader('yd_token.txt')
                y_disc.upload_files_from_local(files_list=files_list, yd_path=yd_path)
