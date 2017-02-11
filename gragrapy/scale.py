from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.cm

from . import util

class Scale(object):
    aes = None
    def apply(self):
        pass

    @staticmethod
    def apply_scales(df, scales):
        def map_col(col, name):
            if name in scales:
                return scales[name].transform(col)
            return col

        return pd.DataFrame({ cname: map_col(df[cname], cname)
                              for cname in df.columns })

class ScaleColorDiv(Scale):
    aes = 'color'
    def transform(self, series):
        return series

    def apply(self):
        mpl.rcParams['image.cmap'] = 'RdBu' # matplotlib.cm.get_cmap('RdBu')

color_div = ScaleColorDiv

class ScaleColorQual(Scale):
    aes = 'color'
    def transform(self, series):
        cmap = matplotlib.cm.get_cmap('Set1')
        vals = util.sorted_unique(series)
        colors = cmap(np.linspace(0, 1, 9))
        return series.map(dict(zip(vals, colors)))

color_qual = ScaleColorQual
