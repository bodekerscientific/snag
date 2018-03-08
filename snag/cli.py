import argparse

from snag import create_namelist


def run_command(args):
    fh = None
    if args.output:
        try:
            fh = open(args.output, 'w')
        except IOError:
            print('Error: could not open file {} for writing'.format(args.output))
            exit(1)
    res = create_namelist(args.input, stream=fh)

    if not fh:
        print(res)


def main():
    parser = argparse.ArgumentParser(prog='snag',
                                     description="Generate configuration files for the UM SCM from structured YAML files")

    parser.add_argument('-o', '--output', help='filename for')
    parser.add_argument('input', help='Input YAML file containing the configuration')

    args = parser.parse_args()
    run_command(args)


if __name__ == '__main__':
    main()
