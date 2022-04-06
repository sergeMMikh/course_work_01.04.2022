import requests
import json
import time
from progress.bar import IncrementalBar

def download_files(files_inf_list: list) -> list:
    # Download files to the local disc.
    with IncrementalBar('Download files to the local disc:', max=len(files_inf_list)) as bar:
        for file in files_inf_list:
            r = requests.get(file['url'])

            with open(file['file_name'], 'wb') as f:
                f.write(r.content)

            bar.next()
            time.sleep(0.4)

    files_list = [i['file_name'] for i in files_inf_list]
    files_list.append(make_json(files_inf_list))
    files_list += make_jsons(files_inf_list)

    return files_list


def make_json(files_list: list) -> str:
    """
    Make one json file with information for all photos.
    """
    json_list = [{"file_name": i["file_name"], 'size': i['size']} for i in files_list]

    with open("Files_info.json", 'w') as f:
        json.dump(json_list, f, ensure_ascii=False, indent=3)

    return "Files_info.json"


def make_jsons(files_list: list):
    """
    Make one json file with information for one photo.
    """
    json_list = [{"file_name": i["file_name"], 'size': i['size']} for i in files_list]
    files_lst = list()

    for file in json_list:
        file_name = f"{file['file_name']}.json"
        files_lst.append(file_name)

        with open(file_name, 'w') as f:
            json.dump(file, f, ensure_ascii=False, indent=3)

    return files_lst
