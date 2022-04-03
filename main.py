from cls_VkUrl import VkUrl
from cls_YaUploader import YaUploader
from pprint import pprint
import file_exchange

if __name__ == '__main__':

    vk = VkUrl()

    vk_id = input("Input vk id: \t")
    photo_quant = int(input("Input a quantity of photos: \t"))
    yd_path = input("Input a yandex disc directory to save files: \t")

    photo_lst = (vk.get_photo_f_profile(vk_id))
    if photo_lst != "Error":
        files_list = file_exchange.format_files_list(photo_lst, photo_quant)
        pprint(files_list)

        y_disc = YaUploader()
        y_disc.upload_files_from_local(files_list=files_list, yd_path=yd_path)

    else:
        print(photo_lst)

    input("Close?")
