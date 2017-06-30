from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import plotnine as p9

abline = p9.geom_abline
area = p9.geom_area
bar = p9.geom_bar
bin2d = p9.geom_bin2d
blank = p9.geom_blank
boxplot = p9.geom_boxplot
col = p9.geom_col
count = p9.geom_count
crossbar = p9.geom_crossbar
density = p9.geom_density
dotplot = p9.geom_dotplot
errorbar = p9.geom_errorbar
errorbarh = p9.geom_errorbarh
freqpoly = p9.geom_freqpoly
histogram = p9.geom_histogram
hist = p9.geom_histogram
hline = p9.geom_hline
jitter = p9.geom_jitter
label = p9.geom_label
line = p9.geom_line
linerange = p9.geom_linerange
path = p9.geom_path
point = p9.geom_point
pointrange = p9.geom_pointrange
polygon = p9.geom_polygon
qq = p9.geom_qq
quantile = p9.geom_quantile
rect = p9.geom_rect
ribbon = p9.geom_ribbon
rug = p9.geom_rug
segment = p9.geom_segment
smooth = p9.geom_smooth
spoke = p9.geom_spoke
step = p9.geom_step
text = p9.geom_text
tile = p9.geom_tile
violin = p9.geom_violin
vline = p9.geom_vline

def _make_geom(*args, **kwargs):
    name = args[0]
    args = args[1:]

    if isinstance(name, p9.geoms.geom.geom):
        # returning an existing instance, can't pass it params
        assert not args and not kwargs
        return name

    if isinstance(name, type) and issubclass(name, p9.geoms.geom.geom):
        cls = name
    else:
        cls = globals()[name]

    return cls(*args, **kwargs)
