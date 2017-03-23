from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import numpy as np
import pandas as pd

from .layer import Layer, LayerComponent
from .aes import Aes
from . import util

class Stat(LayerComponent):
    default_geom = 'point'
    default_aes = Aes()

    def transform(self, df):
        grouped = df.groupby('group')

        oneval_cols = { gname: util.single_value_columns(group)
                        for gname, group in grouped }
        oneval_col_names = [ set(cols) for cols in oneval_cols.values() ]
        restore_cols = set.intersection(*oneval_col_names)

        def transform_group(gname, group):
            transformed = self.transform_group(group)
            for col in restore_cols:
                if col not in transformed:
                    transformed[col] = oneval_cols[gname][col]
            return transformed

        transformed = [ transform_group(gname, group)
                        for gname,group in grouped ]
        return pd.concat(transformed, ignore_index=True)

    def transform_group(self, df):
        pass

    def make_layer(self):
        return Layer(aes=self.aes, data=self.data, stat=self,
                     geom=self.params.get('geom', self.default_geom),
                     params=self.params)

class StatIdentity(Stat):
    def transform(self, df):
        return df
identity = StatIdentity

class StatSmooth(Stat):
    default_geom = 'smooth'

    def transform_group(self, df):
        sorted = df.sort_values('x')
        y = sorted['y'].rolling(5, center=True).mean()
        std = sorted['y'].rolling(5, center=True).std()
        return pd.DataFrame({'x': sorted['x'], 'y': y,
                             'ymin': y - std, 'ymax': y + std})

smooth = StatSmooth

class StatBin(Stat):
    default_geom = 'hist'
    default_aes = Aes(stat_y='weight')

    def transform_group(self, df):
        nbins = self.params.get('bins', 10)

        groups, bins = pd.cut(df.x, nbins, retbins=True)
        mids = pd.Series((bins[1:] + bins[:-1])/2,
                          index=groups.cat.categories)
        widths = pd.Series(bins[1:] - bins[:-1],
                           index=groups.cat.categories)
        counts = df.groupby(groups).x.count()

        return pd.DataFrame({'x': mids, 'weight': counts, 'width': widths})

bin = StatBin
