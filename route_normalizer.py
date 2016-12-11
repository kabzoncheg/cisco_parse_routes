import argparse
import os
import re


def get_args():
    """
    get_args() gets arguments from user input, when run from cmd
    :return: dict with arguments
    """
    parser = argparse.ArgumentParser(description=''
                                                 'Script for parsing  Cisoc show ip route command output')
    parser.add_argument('-r', '--rfile', type=str, help='Path to .txt file with show ip route output',
                        default=os.path.join(os.getcwd(), 'routes.txt'))
    parser.add_argument('-o', '--ofile', type=str, help='Path to output .txt file',
                        default=os.path.join(os.getcwd(), 'normalized_routes.txt'))
    return parser.parse_args()


def route_normalizer(path_to_file):
    """
    :param path_to_file: OS Path to file
    :return: list with routes
    """
    with open(path_to_file) as open_file:
        regex = re.compile(r'^\[\d+/\d+\].+')
        file_lines = []
        for line in open_file:
            new_line = line.strip()
            if regex.match(new_line):
                new_line = file_lines.pop() + new_line
            file_lines.append(new_line)
    return file_lines


def output_saver(output, path_to_file):
    with open(path_to_file, 'w') as outfile:
        for line in output:
            string = line + '\n'
            outfile.write(string)


def main():
    args = get_args()
    path_to_rfile = args.rfile
    path_to_ofile = args.ofile
    parsed_output = route_normalizer(path_to_rfile)
    output_saver(parsed_output, path_to_ofile)


if __name__ == main():
    main()
