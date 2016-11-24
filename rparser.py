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
                        default=os.path.join(os.getcwd(), 'output.txt'))
    return parser.parse_args()


def route_parser(path_to_file):
    """
    :param path_to_file: OS Path to file
    :return: dict with next-hops and its bound subnets
    """
    result = {}
    with open(path_to_file) as open_file:
        regex = re.compile(r'^.+ via (?P<ip>(\d{1,3}\.?){4})')
        file_lines = []
        all_nh = []
        for line in open_file:
            file_lines.append(line)
            if regex.match(line):
                all_nh.append(regex.match(line).group('ip'))
    unique_nh = set(all_nh)
    for nh in unique_nh:
        result[nh] = []
        pattern = r'^.+ (?P<network>(\d{1,3}\.?){4}/\d{1,2}).+ ' + re.escape(nh)
        regex = re.compile(pattern)
        for line in file_lines:
            if regex.match(line):
                network = regex.match(line).group('network')
                result[nh].append(network)
        result[nh].sort()
    return result


def output_saver(output, path_to_file):
    with open(path_to_file, 'w') as outfile:
        for nh in output:
            string = nh + '\n'
            outfile.write(string)
            for subnet in output[nh]:
                string = '\t' + subnet + '\n'
                outfile.write(string)


def main():
    args = get_args()
    path_to_rfile = args.rfile
    path_to_ofile = args.ofile
    parsed_output = route_parser(path_to_rfile)
    output_saver(parsed_output, path_to_ofile)


if __name__ == main():
    main()
