import copy
import json


def generate_key(key, pref):
    return f'{pref} {key}'


def get_generated_diff(file1, file2):
    copy_file2 = copy.deepcopy(file2)
    new_file = {}
    pref = [' ', '-', '+']
    for key in file1.keys():
        if file2.get(key):
            if file1[key] == file2[key]:
                new_file[generate_key(key, pref[0])] = copy_file2.pop(key)
            else:
                new_file[generate_key(key, pref[1])] = file1[key]
                new_file[generate_key(key, pref[2])] = copy_file2.pop(key)
        else:
            new_file[generate_key(key, pref[1])] = file1[key]
    if len(copy_file2) > 0:
        for key in copy_file2.keys():
            new_file[generate_key(key, pref[2])] = copy_file2[key]
    return new_file


def generate_diff(filepath1, filepath2):
    file1 = json.load(open(filepath1))
    file2 = json.load(open(filepath2))
    diff_file = get_generated_diff(file1, file2)
    sorted_diff_file = dict(
        sorted(diff_file.items(), key=lambda item: item[0][2:])
    )
    result = json.dumps(sorted_diff_file, indent=2, separators=('', ': '))
    return result.replace('"', '')