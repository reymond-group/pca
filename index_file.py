""" Index a file """
import argparse

PARSER = argparse.ArgumentParser(
    description='Index a file with a from - to index for binary reading.')

PARSER.add_argument('input', metavar='INPUT', type=str,
                    help='the input (line separated) file')


ARGS = PARSER.parse_args()

def run():
    """ Generate the index for the given file """
    start = 0
    with open(ARGS.input, 'r') as in_file:
        with open(ARGS.input + '.index', 'a+') as out_file:
            for line in in_file:
                length = len(line)
                out_file.write(str(start) + ',' + str(length) + '\n')
                start += length

run()
