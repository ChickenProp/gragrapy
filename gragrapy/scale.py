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
        """Called when this scale is used in a plot."""
        pass

    def transform(self, series):
        """Initial transformation of data.

        This takes place before stats are applied."""
        return series

    def train(self, series):
        """Learn the domain of the scale."""
        pass

    def map(self, series):
        """Map the series into plot-space."""
        return series

    @staticmethod
    def transform_scales(df, scales):
        def trans_col(col, name):
            if name in scales:
                return scales[name].transform(col)
            return col

        return pd.DataFrame({ cname: trans_col(df[cname], cname)
                              for cname in df.columns })

    @staticmethod
    def train_scales(datas, scales):
        columns = set(c for df in datas for c in df.columns)
        for cname in columns:
            if cname in scales:
                scales[cname].train([ df[cname] for df in datas
                                      if cname in df ])

    @staticmethod
    def map_scales(df, scales):
        def map_col(col, name):
            if name in scales:
                return scales[name].map(col)
            return col

        return pd.DataFrame({ cname: map_col(df[cname], cname)
                              for cname in df.columns })

class ScaleColorDiv(Scale):
    aes = 'color'
    def apply(self):
        mpl.rcParams['image.cmap'] = 'RdBu' # matplotlib.cm.get_cmap('RdBu')

color_div = ScaleColorDiv

class ScaleColorQual(Scale):
    aes = 'color'
    def train(self, cols):
        cmap = matplotlib.cm.get_cmap('Set1')
        vals = util.sorted_unique(pd.concat(cols, ignore_index=True))
        colors = cmap(np.linspace(0, 1, 9))
        self.mapper = dict(zip(vals, colors))

    def map(self, series):
        return series.map(self.mapper)

color_qual = ScaleColorQual
