from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import sys
import argparse

import gragrapy as gg

def parse_kwargs(kwargs):
    return { k:v for k,v in [a.split('=', 1) for a in kwargs] }

def parse_command_line(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--data')
    parser.add_argument('--geom', '-g', action='append', nargs='+')
    parser.add_argument('--stat', '-s', action='append', nargs='+')
    parser.add_argument('aes', nargs='*')

    args = parser.parse_args(argv)
    print(args)
    args.aes = gg.Aes(**parse_kwargs(args.aes))
    args.geom = [ getattr(gg.geom, g[0])(**parse_kwargs(g[1:]))
                  for g in args.geom or [] ]
    args.stat = [ getattr(gg.stat, s[0])(**parse_kwargs(s[1:]))
                  for s in args.stat or [] ]
    return args

def main():
    args = parse_command_line(sys.argv[1:])
    print(args)
    data = getattr(gg.data, args.data)
    geoms = args.geom or gg.geom.point
    stats = args.stat or []
    (gg.Plot(data, args.aes) + geoms + stats).show()

if __name__ == '__main__':
    main()
