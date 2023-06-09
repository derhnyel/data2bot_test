import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Parse JSON files and generate a schema')
    parser.add_argument('source', type=str, help='source path')
    parser.add_argument('target', type=str, help='target path')
    parser.add_argument('--depth', type=int, default=-1, help='depth of search')
    parser.add_argument('--verbose', action='store_true', help='increase output verbosity')
    parser.add_argument('--select', type=str, help='select a particular parent attribute from json file')
    args = parser.parse_args()
    return args
