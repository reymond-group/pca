""" Pad a file """
import argparse

PARSER = argparse.ArgumentParser(
    description='Pad a file.')

PARSER.add_argument('input', metavar='INPUT', type=str,
                    help='the input (csv) file')

PARSER.add_argument('output', metavar='OUTPUT', type=str,
                    help='the output (csv) file')


ARGS = PARSER.parse_args()

max_line_length = 0

with open(ARGS.input, 'r') as f:
    for line in f:
        if len(line) > max_line_length:
            max_line_length = len(line)

print(max_line_length - 1)

with open(ARGS.input, 'r') as f:
    with open(ARGS.output, 'a+') as g:
        for line in f:
            diff = max_line_length - len(line)
            g.write(line[:-1] + ' ' * diff)

