import requests
import os
import time
from progress.bar import IncrementalBar


class YaUploader:
    def __init__(self):
        """
        Here program takes the TOKEN
        """
        with open('ya_token.txt', 'r') as t_file:
            self.token = t_file.read().strip()
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

    def get_upload_link(self, y_disc_file_path: str) -> dict:
        """Метод получает ссылку на загрузку файла на яндекс диск"""

        up_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": y_disc_file_path, "overwrite": "true"}
        response = requests.get(up_url, headers=headers, params=params)

        return response.json()

    def create_dir_link(self, y_disc_file_path: str) -> dict:
        """Метод создаёт папку на yandex disk.
        Если указанная папка уже существует, yandex возвращает ошибку"""

        url = "https://cloud-api.yandex.net/v1/disk/resources?path=" + y_disc_file_path
        headers = self.get_headers()
        response = requests.put(url, headers=headers)

        return response.json()

    def upload_from_local(self, file_path: str, yd_path: str) -> str:
        """Метод загружает файлы по списку file_list на яндекс диск"""

        file_name_ = os.path.basename(file_path)
        href_json = self.get_upload_link(y_disc_file_path=yd_path)
        href = href_json['href']
        response = requests.put(href, data=open(file_path, 'rb'))

        if response.status_code < 300:
            return f"File '{file_name_}' successfully loaded to Yandex Disc."
        else:
            return f"Error code: {response.status_code}"

    def upload_files_from_local(self, files_list: list, yd_path: str) -> str:
        """Метод загружает файлы по списку file_list на яндекс диск"""

        # Create a new directory
        print(self.create_dir_link(yd_path))

        # Upload files to Yandex disc
        with IncrementalBar('Upload files to Yandex disc: ', max=len(files_list)) as bar:
            for file in files_list:
                time.sleep(0.4)

                new_path = yd_path + "/" + file
                href_json = self.get_upload_link(y_disc_file_path=new_path)
                href = href_json['href']
                response = requests.put(href, data=open(file, 'rb'))

                bar.next()

                if response.status_code < 300:
                    pass
                    # print(f"File '{file}' successfully loaded to Yandex Disc.")
                else:
                    return f"Error code: {response.status_code}"

        return "All files uploaded successfully."
