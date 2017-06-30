from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import plotnine as p9

bin = p9.stat_bin
bin2d = p9.stat_bin2d
bin_2d = p9.stat_bin_2d
bindot = p9.stat_bindot
boxplot = p9.stat_boxplot
count = p9.stat_count
density = p9.stat_density
ecdf = p9.stat_ecdf
function = p9.stat_function
identity = p9.stat_identity
qq = p9.stat_qq
quantile = p9.stat_quantile
smooth = p9.stat_smooth
sum = p9.stat_sum
summary = p9.stat_summary
summary_bin = p9.stat_summary_bin
unique = p9.stat_unique
ydensity = p9.stat_ydensity

def _make_stat(*args, **kwargs):
    name = args[0]
    args = args[1:]

    if isinstance(name, p9.stats.stat.stat):
        # returning an existing instance, can't pass it params
        assert not args and not kwargs
        return name

    if isinstance(name, type) and issubclass(name, p9.stats.stat.stat):
        cls = name
    else:
        cls = globals()[name]

    return cls(*args, **kwargs)
