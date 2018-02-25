import argparse

from snag import
from wrfconf.process import create_namelists


def create_parser(subparsers):
    create = subparsers.add_parser('create', help='Create new configuration files for a WRF run')
    create.add_argument('input', help='YML configuration file for the run')
    create.add_argument('-n', '--namelist', default='.', help='Folder to store the WRF namelist file')
    create.add_argument('-w', '--wps', default='.', help='Folder to store the WPS file')
    create.add_argument('-o', '--output', help='Folder to store the WPS file')


def run_command(args):
    if args.cmd == 'gen_params':
        print(process_namelist(args.input))
    elif args.cmd == 'create':
        create_namelists(args.input, args.namelist, args.wps)


def main():
    parser = argparse.ArgumentParser(prog='wrfconf',
                                     description="Generate WRF configuration from structured YAML files")
    subparsers = parser.add_subparsers(dest='cmd')

    create_parser(subparsers)

    args = parser.parse_args()
    run_command(args)


main()