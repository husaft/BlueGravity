import json
from os.path import abspath, isdir, isfile
from os import mkdir


def create_dir(name):
    folder = abspath(name)
    if not isdir(folder):
        mkdir(folder)
    return folder


def load_json(file_path):
    if not isfile(file_path):
        save_json({}, file_path)
    with open(file_path, 'r', encoding="utf8") as dic_file:
        return json.load(dic_file)


def save_json(obj, file_path):
    with open(file_path, 'w', encoding="utf8") as dic_file:
        json.dump(obj, dic_file, indent=2, ensure_ascii=False, sort_keys=True)
