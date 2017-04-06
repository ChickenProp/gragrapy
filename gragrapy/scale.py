from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

from enum import Enum
import numbers
import warnings
from collections import OrderedDict

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
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

    def __init__(self, *args, **kwargs):
        self.init(*args, **kwargs)
        self.args = args
        self.kwargs = kwargs

    def init(self):
        pass

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

    def copy(self):
        return self.__class__(*self.args, **self.kwargs)

    @staticmethod
    def transform_scales(df, scales, columns=None):
        def trans_col(col, name):
            if name in scales and (columns is None or name in columns):
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

    def get_legend(self):
        pass

class ScaleCartesianContinuous(Scale):
    level = Level.CONTINUOUS

    def init(self, domain=None):
        self.domain = domain

    def train(self, cols):
        if self.domain:
            self.min, self.max = self.domain
        else:
            self.min = min(c.min() for c in cols)
            self.max = max(c.max() for c in cols)

class ScaleCartesianDiscrete(Scale):
    level = Level.DISCRETE

    def init(self, labels=None):
        self.labels = labels

    def train(self, cols):
        vals = util.sorted_unique(pd.concat(cols, ignore_index=True))
        self.mapper = OrderedDict((v, i) for i,v in enumerate(vals))

    def map(self, series):
        return series.map(self.mapper)

class ScaleXContinuous(ScaleCartesianContinuous):
    aes = 'x'

    def apply_ax(self, ax):
        if self.domain:
            ax.set_xlim(self.min, self.max)
        else:
            ax.autoscale_view(scaley=False)

class ScaleXDiscrete(ScaleCartesianDiscrete):
    aes = 'x'

    def apply_ax(self, ax):
        ax.autoscale_view(scaley=False)
        ax.set_xticks(range(len(self.mapper)))
        ax.set_xticklabels(self.labels or list(self.mapper))

class x(object):
    continuous = ScaleXContinuous
    discrete = ScaleXDiscrete

class ScaleYContinuous(ScaleCartesianContinuous):
    aes = 'y'

    def apply_ax(self, ax):
        if self.domain:
            ax.set_ylim(self.min, self.max)
        else:
            ax.autoscale_view(scalex=False)

class ScaleYDiscrete(ScaleCartesianDiscrete):
    aes = 'y'

    def apply_ax(self, ax):
        ax.autoscale_view(scalex=False)
        ax.set_yticks(range(len(self.mapper)))
        ax.set_yticklabels(self.labels or list(self.mapper))

class y(object):
    continuous = ScaleYContinuous
    discrete = ScaleYDiscrete

class ScaleColorDiv(Scale):
    aes = 'color'
    level = Level.CONTINUOUS

    def train(self, cols):
        self.min = min(c.min() for c in cols)
        self.max = max(c.max() for c in cols)
        self.norm = matplotlib.colors.Normalize(self.min, self.max)

    def map(self, series):
        cm = matplotlib.cm.get_cmap('bwr')
        normed = self.norm(series)
        colors = cm(normed)
        return pd.Series([ tuple(c) for c in colors ], index=series.index)

    def get_legend(self):
        vals = pd.Series(np.linspace(self.min, self.max, 5))
        colors = self.map(vals)
        return [ mpl.patches.Patch(color=c, label=v)
                 for c,v in zip(colors, vals) ]

class ScaleColorQual(Scale):
    aes = 'color'
    level = Level.DISCRETE

    def train(self, cols):
        cmap = matplotlib.cm.get_cmap('Set1')
        vals = util.sorted_unique(pd.concat(cols, ignore_index=True))

        # There's no obvious way to get the number of distinct colors from a
        # colormap. Looking at cmap._segmentdata might work, but it's hacky.
        if len(vals) > 9:
            raise ValueError('Too many distinct values for qualitative color'
                             ' scale. Need at most 9. Given: %d' % (len(vals),))

        colors = cmap(np.linspace(0, 1, 9))
        # Has to be an ordered dict for legend to give the correct ordering
        self.mapper = OrderedDict(zip(vals, colors))

    def map(self, series):
        return series.map(self.mapper)

    def get_legend(self):
        return [ mpl.patches.Patch(color=v, label=k)
                 for k, v in self.mapper.items() ]

class color(object):
    div = ScaleColorDiv
    qual = ScaleColorQual

default_scales = {
    'x': (x.continuous, x.discrete),
    'y': (y.continuous, y.discrete),
    'color': (color.div, color.qual),
}

def guess_default_scales(dataset, existing_scales):
    """If `dataset` has columns with no scales, guess some scales to use for
    them.

    Return a dict of new scales (with no keys in common with `existing_scales`).
    """
    wanted_scales = set(dataset.columns) - set(existing_scales)
    ret = {}

    for scl in wanted_scales.intersection(set(default_scales)):
        level = Level.guess_series_level(dataset[scl])
        if level == Level.CONTINUOUS:
            default = default_scales[scl][0]
        else:
            default = default_scales[scl][1]
        if default is not None:
            ret[scl] = default()

    return ret
