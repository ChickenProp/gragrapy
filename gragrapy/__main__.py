from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import sys
import argparse

import gragrapy as gg

def parse_kwargs(kwargs):
    def parse_val(v):
        try:
            return int(v)
        except Exception as e:
            return v

    return { k: parse_val(v) for k,v in [a.split('=', 1) for a in kwargs] }

def parse_command_line(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--data')
    parser.add_argument('--geom', '-g', action='append', nargs='+')
    parser.add_argument('--stat', '-s', action='append', nargs='+')
    parser.add_argument('--facet', '-f', nargs='+')
    parser.add_argument('aes', nargs='*')

    args = parser.parse_args(argv)
    print(args)
    args.aes = gg.Aes(**parse_kwargs(args.aes))
    args.geom = [ getattr(gg.geom, g[0])(**parse_kwargs(g[1:]))
                  for g in args.geom or [] ]
    args.stat = [ getattr(gg.stat, s[0])(**parse_kwargs(s[1:]))
                  for s in args.stat or [] ]
    if args.facet:
        args.facet = gg.facet(args.facet[0], **parse_kwargs(args.facet[1:]))
    return args

def main():
    args = parse_command_line(sys.argv[1:])
    print(args)
    data = getattr(gg.data, args.data)
    geoms = args.geom or gg.geom.point
    stats = args.stat or []
    facet = args.facet or []
    (gg.Plot(data, args.aes) + geoms + stats + facet).show()

if __name__ == '__main__':
    main()
