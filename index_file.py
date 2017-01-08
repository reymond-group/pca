""" Index a file """
import argparse

PARSER = argparse.ArgumentParser(
    description='Index a file with a from - to index for binary reading.')

PARSER.add_argument('input', metavar='INPUT', type=str,
                    help='the input (line separated) file')


ARGS = PARSER.parse_args()

start = 0

with open(ARGS.input, 'r') as f:
    with open(ARGS.input + '.index', 'a+') as g:
        for line in f:
            length = len(line)
            g.write(str(start) + ',' + str(length) + '\n')
            start += length

