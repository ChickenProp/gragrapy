from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

from enum import Enum
import numbers
import warnings

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.cm

from . import util

class Level(Enum):
    DISCRETE = 1
    CONTINUOUS = 2

    @staticmethod
    def _continuous_dtype_kinds():
        """The values of `dtype.kind` that suggest a continuous Series."""
        return 'biufcmM'

    @staticmethod
    def _discrete_dtype_kinds():
        """The values of `dtype.kind` that suggest a discrete Series."""
        return 'OSUV'

    @staticmethod
    def guess_series_level(series):
        kind = series.dtype.kind
        if kind in Level._continuous_dtype_kinds():
            return Level.CONTINUOUS
        elif kind in Level._discrete_dtype_kinds():
            return Level.DISCRETE
        else:
            warnings.warn('Unknown dtype kind: %r. Assuming series is discrete.'
                          % (kind,))
            return Level.DISCRETE

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

class color(object):
    div = ScaleColorDiv
    qual = ScaleColorQual

def guess_default_scales(dataset, existing_scales):
    """If `dataset` has columns with no scales, guess some scales to use for
    them.

    Return a dict of new scales (with no keys in common with `existing_scales`).
    """
    if 'color' in dataset and 'color' not in existing_scales:
        color_level = Level.guess_series_level(dataset.color)
        if color_level == Level.CONTINUOUS:
            return { 'color': color.div() }
        else:
            return { 'color': color.qual() }

    return {}
