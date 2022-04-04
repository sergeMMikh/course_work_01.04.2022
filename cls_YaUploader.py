import requests
import os
import time
from progress.bar import IncrementalBar
from cls_HttpReq import HttpR


class YaUploader(HttpR):
    def __init__(self, token_file_n: str):
        super().__init__(token_file_n)

    def get_headers(self) -> dict:
        """This method forms a list of headers"""

        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_files_list(self) -> dict:
        """The method receives data about files already stored on the disk"""

        url = "https://cloud-api.yandex.net/v1/disk/resources/files"
        headers = self.get_headers()
        response = requests.get(url, headers=headers, timeout=5)

        return response.json()

    def get_upload_link(self, y_disc_file_path: str) -> dict:
        """The method receives a link to upload a file to Yandex disk"""

        up_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": y_disc_file_path, "overwrite": "true"}
        response = requests.get(up_url, headers=headers, params=params)

        return response.json()

    def create_dir_link(self, y_disc_file_path: str) -> dict:
        """The method creates a folder on yandex disk.
        If the specified folder already exists, yandex just returns an error message"""

        url = "https://cloud-api.yandex.net/v1/disk/resources?path=" + y_disc_file_path
        headers = self.get_headers()
        response = requests.put(url, headers=headers)

        return response.json()

    def upload_from_local(self, file_path: str, yd_path: str) -> str:
        """The method loads file according to the file_list on yandex disk"""

        file_name_ = os.path.basename(file_path)
        href_json = self.get_upload_link(y_disc_file_path=yd_path)
        href = href_json['href']
        with open(file_path, 'rb') as data:
            response = requests.put(href, data=data)

        if response.status_code < 300:
            return f"File '{file_name_}' successfully loaded to Yandex Disc."
        else:
            return f"Error code: {response.status_code}"

    def upload_files_from_local(self, files_list: list, yd_path: str) -> str:
        """The method loads files according to the file_list on yandex disk"""

        # Create a new directory
        self.create_dir_link(yd_path)

        # Upload files to Yandex disc
        with IncrementalBar('Upload files to Yandex disc: ', max=len(files_list)) as bar:
            for file in files_list:
                time.sleep(0.4)

                new_path = yd_path + "/" + file
                href_json = self.get_upload_link(y_disc_file_path=new_path)
                href = href_json['href']

                with open(file, 'rb') as data:
                    response = requests.put(href, data=data)

                # Delete files from local disk.
                os.remove(file)

                bar.next()

                if response.status_code < 300:
                    pass
                    # print(f"File '{file}' successfully loaded to Yandex Disc.")
                else:
                    return f"Error code: {response.status_code}"

        return "All files uploaded successfully."
