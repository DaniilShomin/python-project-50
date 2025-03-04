import argparse
from gendiff.modules import generate_diff


def get_names_files():
    parser = argparse.ArgumentParser(
    description='Compares two configuration files and shows a difference.')
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument('-f', '--format', help='set format of output')
    return parser.parse_args()


def main():
    files = get_names_files()
    filepath1 = 'data/' + files.first_file
    filepath2 = 'data/' + files.second_file
    diff = generate_diff(filepath1, filepath2)
    print(diff)




if __name__ == '__main__':
    main()