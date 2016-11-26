""" Pad a xyz coordinate file """
import argparse

PARSER = argparse.ArgumentParser(
    description='Pad a xyz coordinate file.')

PARSER.add_argument('input', metavar='INPUT', type=str,
                    help='the input (csv) file')

PARSER.add_argument('output', metavar='OUTPUT', type=str,
                    help='the padded output file')


ARGS = PARSER.parse_args()

max_line_length = 0

with open(ARGS.input, 'r') as f:
    for line in f:
        values = line[:-1].split(',')
        tmp_line = ''
        for value in values:
            tmp_line += str(round(float(value), 3)) + ','
        length = len(tmp_line) - 1
        if length > max_line_length:
            max_line_length = length

print(max_line_length)

with open(ARGS.input, 'r') as f:
    with open(ARGS.output, 'a+') as g:
        for line in f:
            values = line[:-1].split(',')
            tmp_line = ''
            for value in values:
                tmp_line += str(round(float(value), 3)) + ','
            tmp_line = tmp_line[:-1]
            diff = max_line_length - len(tmp_line)
            g.write(tmp_line + ' ' * diff)

