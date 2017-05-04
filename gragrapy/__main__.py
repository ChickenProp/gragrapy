from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import sys
import argparse

import gragrapy as gg

def parse_command_line(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--data')
    parser.add_argument('--geom', '-g', action='append')
    parser.add_argument('aes', nargs='*')

    args = parser.parse_args(argv)
    args.aes = gg.Aes(**{k:v for k,v in [a.split('=') for a in args.aes]})
    args.geom = [ getattr(gg.geom, g) for g in args.geom or [] ]
    return args

def main():
    args = parse_command_line(sys.argv[1:])
    print(args)
    data = getattr(gg.data, args.data)
    geoms = args.geom or gg.geom.point
    (gg.Plot(data, args.aes) + geoms).show()

if __name__ == '__main__':
    main()
