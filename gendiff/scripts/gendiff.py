import argparse

from gendiff.modules import generate_diff


def get_file_paths():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.')
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument('-f', '--format', help='set format of output')
    return parser.parse_args()


def main():
    args = get_file_paths()
    filepath1 = args.first_file
    filepath2 = args.second_file
    format = args.format
    diff = generate_diff(filepath1, filepath2, format)
    print(diff)


if __name__ == '__main__':
    main()