import copy
import json


def generate_key(key, pref):
    return f'{pref} {key}'


def generate_diff(filepath1, filepath2):
    file1 = json.load(open(filepath1))
    file2 = json.load(open(filepath2))
    copy_file2 = copy.deepcopy(file2)
    new_file = {}
    for key in file1.keys():
        if file2.get(key):
            if file1[key] == file2[key]:
                new_file[generate_key(key, ' ')] = copy_file2.pop(key)
            else:
                new_file[generate_key(key, '-')] = file1[key]
                new_file[generate_key(key, '+')] = copy_file2.pop(key)
        else:
            new_file[generate_key(key, '-')] = file1[key]
    
    if len(copy_file2) > 0:
        for key in copy_file2.keys():
            new_file[generate_key(key, '+')] = copy_file2[key]
    sorted_new_file = dict(
        sorted(new_file.items(), key=lambda item: item[0][2:])
    )

    result_str = '{\n'
    for k, v in sorted_new_file.items():
        result_str += f'  {k}: {str(v).lower()}\n'
    result_str += '}'
    return result_str


