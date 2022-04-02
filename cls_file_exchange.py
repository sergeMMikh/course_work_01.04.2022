import requests
import json
from pprint import pprint


def format_files_list(photo_list: list) -> list:
    """
    Format a list of files by template:
        [{
        "file_name": "34.jpg",
        "url": url to download
        "size": "z"
        }]
    """

    files_list = list()
    for photo in photo_list:
        print('1')
        # pprint(photo)

        # Choose a best resolution photo
        max_photo = max(photo['sizes'], key=lambda size: int(size['width']))
        # pprint(f"max_photo: {max_photo}")

        # Solve the file name conflict
        file_name = f"{photo['likes']['count']}.jpeg"
        counter = 1
        new_file_name = file_name
        for file in files_list:
            if file_name in file['file_name']:
                new_file_name = f"({counter}){file_name}"
                counter += 1

        # Collect the list of files.
        files_list.append({'file_name': new_file_name,
                           'url': max_photo['url'],
                           'size': max_photo['type']})

    pprint(files_list)

    # Download files to the local disc.
    # for f in files_list:
    #     r = requests.get(f['url'])
    #     with open(f['file_name'], 'wb') as f:
    #         f.write(r.content)

    make_jsons(files_list)
    return files_list


def make_jsons(files_list: list):
    json_list = [{"file_name":i["file_name"], 'size': i['size']} for i in files_list]
    pprint(json_list)

    # for file in json_list:
    #     with open(f"{file['file_name']}.json", 'w') as f:
    #         json.dump(file, f, ensure_ascii=False, indent=3)

