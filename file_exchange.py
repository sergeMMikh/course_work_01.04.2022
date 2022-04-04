import requests
import json
import time
from progress.bar import IncrementalBar


def format_files_list(photo_list: dict, qtt: int) -> list:
    """
    Format a list of files_inf_list by template:
        [{
        "file_name": "34.jpg",
        "data": "data"
        "url": url to download
        "size": "z"
        "width": width of photo
        }]
    Make a list of files (files_list) for next
    """
    files_inf_list = list()

    for photo in photo_list:
        # Choose the best resolution photo
        max_photo = max(photo['sizes'], key=lambda size: int(size['width']))

        file_name = f"{photo['likes']['count']}.jpeg"

        # Collect the list of files.
        files_inf_list.append({'file_name': file_name,
                               'date': photo['date'],
                               'url': max_photo['url'],
                               'size': max_photo['type'],
                               'width': max_photo['width']})

    files_inf_list.sort(key=lambda x: int(x['width']), reverse=True)

    if len(files_inf_list) < qtt:
        qtt = len(files_inf_list)

    print(f"qtt: {qtt}")
    files_inf_list = [files_inf_list[i] for i in range(qtt)]

    # Solve the file name conflict
    tmp_list = list()
    for file in files_inf_list:
        new_file_name = file['file_name']
        if new_file_name in tmp_list:
            new_file_name = f"{file['file_name']}_{file['date']}"
            file['file_name'] = new_file_name
        tmp_list.append(new_file_name)

    files_list = [i['file_name'] for i in files_inf_list]

    # Download files to the local disc.
    with IncrementalBar('Download files to the local disc:', max=len(files_inf_list)) as bar:
        for file in files_inf_list:
            r = requests.get(file['url'])

            with open(file['file_name'], 'wb') as f:
                f.write(r.content)

            bar.next()
            time.sleep(0.4)

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
