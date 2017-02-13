""" Check a file """
import argparse

PARSER = argparse.ArgumentParser(
    description='Check a file for wether it is a well-formed smi file or not.')

PARSER.add_argument('input', metavar='INPUT', type=str,
                    help='the input (.smi) file')

PARSER.add_argument('-f', '--fingerprint-values', type=int, default=42,
                    help='use instead of FINGERPRINT_VALUES as the number of fingerprint values')

PARSER.add_argument('-p', '--property-values', type=int, default=9,
                    help='use instead of PROPERTY_VALUES as the number of properties')

FIX = PARSER.add_mutually_exclusive_group(required=False)
FIX.add_argument('--fix', dest='fix', action='store_true')
FIX.add_argument('--no-fix', dest='fix', action='store_false')
PARSER.set_defaults(fix=False)

ARGS = PARSER.parse_args()

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def run():
    """ Do the actual checking """
    i = 0
    with open(ARGS.input, 'r', errors='replace') as in_file:
        for line in in_file:
            i += 1

            if i % 1000000 == 0:
                if not ARGS.fix:
                    print('Checking line ' + str(i) + ' ...')
            
            split_line = line.split(' ')

            if len(split_line) != 3:
                if not ARGS.fix:
                    print('There are not three values delimited by a space.')
                    print(str(i) + ',' + line)
                continue

            info = split_line[0].split(';')
            
            if len(info) != 2:
                if not ARGS.fix:
                    print('The first value does not consist of two parts seperated by a semicolon.')
                    print(str(i) + ',' + line)
                continue

            fingerprint = split_line[1].split(';')

            if len(fingerprint) != ARGS.fingerprint_values:
                if not ARGS.fix:
                    print('The fingerprint contains ' + str(len(fingerprint)) + ' instead of ' + str(ARGS.fingerprint_values) + ' values')
                    print(str(i) + ',' + line)
                continue

            properties = split_line[2].split(';')

            if len(properties) != ARGS.property_values:
                if not ARGS.fix:
                    print('The properties contain ' + str(len(properties)) + ' instead of ' + str(ARGS.property_values) + ' values')
                    print(str(i) + ',' + line)
                continue

            not_number = False
            
            for p in properties:
                if not is_number(p):
                    not_number = True

            for f in fingerprint:
                if not is_number(f):
                    not_number = True

            if not_number:
                if not ARGS.fix:
                    print('There is a character which is not a number in either the fingerprint or the properties')
                    print(str(i) + ',' + line)
                continue

            if ARGS.fix:
                print(line)
run()
