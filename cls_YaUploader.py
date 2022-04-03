import requests
import os
import time
from progress.bar import IncrementalBar


class YaUploader:
    def __init__(self):
        """
        Here program takes the TOKEN
        """
        with open('ya_token.txt', 'r') as tfile:
            self.token = tfile.read().strip()
            print(f'TOKEN: {self.token}')

    def get_headers(self) -> dict:
        """Метод формирует словарь заголовков"""

        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_files_list(self) -> dict:
        """Метод получает данные о файлах, уже хранящихся на диске"""

        url = "https://cloud-api.yandex.net/v1/disk/resources/files"
        headers = self.get_headers()
        response = requests.get(url, headers=headers, timeout=5)
        print(headers)

        return response.json()

    def get_uplooad_link(self, y_disc_file_path: str) -> dict:
        """Метод получает ссылку на загрузку файла на яндекс диск"""

        up_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": y_disc_file_path, "overwrite": "true"}
        responce = requests.get(up_url, headers=headers, params=params)

        return responce.json()

    def upload_from_local(self, file_path: str, yd_path: str) -> str:
        """Метод загружает файлы по списку file_list на яндекс диск"""

        file_name_ = os.path.basename(file_path)
        href_json = self.get_uplooad_link(y_disc_file_path=yd_path)
        href = href_json['href']
        response = requests.put(href, data=open(file_path, 'rb'))

        if response.status_code < 300:
            return f"File '{file_name_}' successfully loaded to Yandex Disc."
        else:
            return f"Error code: {response.status_code}"

    def upload_files_from_local(self, files_list: list, yd_path: str) -> str:
        """Метод загружает файлы по списку file_list на яндекс диск"""

        bar = IncrementalBar('Upload files to Yandex disc: ', max=len(files_list))
        for file in files_list:

            new_path = yd_path + "/" + file
            href_json = self.get_uplooad_link(y_disc_file_path=new_path)
            href = href_json['href']

            response = requests.put(href, data=open(file, 'rb'))

            bar.next()
            time.sleep(0.4)

            if response.status_code < 300:
                pass
                # print(f"File '{file}' successfully loaded to Yandex Disc.")
            else:
                return f"Error code: {response.status_code}"

        bar.finish()

        return "All files uploaded successfully."
