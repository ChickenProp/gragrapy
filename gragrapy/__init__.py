from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import plotnine as p9

from .plot import plot
from .data import data

from plotnine import aes, facet_grid, facet_wrap
facet = facet_wrap
from plotnine import ggtitle as title, xlab, ylab

from . import geom
from . import stat
from . import scale
from . import coord
