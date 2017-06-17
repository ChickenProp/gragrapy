from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import numpy as np
import pandas as pd

from .layer import Layer, LayerComponent
from .aes import Aes
from . import util, scale

class Stat(LayerComponent):
    default_geom = 'point'
    default_aes = Aes()

    def transform(self, df, scales=None):
        grouped = df.groupby('group')

        oneval_cols = { gname: util.single_value_columns(group)
                        for gname, group in grouped }
        oneval_col_names = [ set(cols) for cols in oneval_cols.values() ]
        restore_cols = set.intersection(*oneval_col_names)

        def transform_group(gname, group):
            transformed = self.transform_group(group, scales)
            for col in restore_cols:
                if col not in transformed:
                    transformed[col] = oneval_cols[gname][col]
            return transformed

        transformed = [ transform_group(gname, group)
                        for gname,group in grouped ]
        return pd.concat(transformed, ignore_index=True)

    def transform_group(self, df, scales=None):
        pass

    def make_layer(self):
        return Layer(aes=self.aes, data=self.data, stat=self,
                     geom=self.params.get('geom', self.default_geom),
                     params=self.params)

class StatIdentity(Stat):
    def transform(self, df, scales=None):
        return df
identity = StatIdentity

class StatSmooth(Stat):
    default_geom = 'smooth'

    def transform_group_mavg(self, df):
        window = self.params.get('window', 5)
        sorted = df.sort_values('x')
        y = sorted['y'].rolling(window, center=True).mean()
        std = sorted['y'].rolling(window, center=True).std()
        return pd.DataFrame({'x': sorted['x'], 'y': y,
                             'ymin': y - std, 'ymax': y + std})

    def transform_group_lm(self, df):
        import statsmodels.api as sm
        from statsmodels.sandbox.regression.predstd import wls_prediction_std

        sorted = df.sort_values('x')
        fit = sm.OLS(sorted.y, sm.add_constant(sorted.x)).fit()
        # wls_prediction_std respects indexes, so no need to reindex
        std, low, high = wls_prediction_std(fit, alpha=0.05)
        return pd.DataFrame({'x': sorted.x, 'y': fit.fittedvalues,
                             'ymin': low, 'ymax': high})

    def transform_group(self, df, scales=None):
        method = self.params.get('method', 'mavg')
        if method == 'lm':
            return self.transform_group_lm(df)
        elif method == 'mavg':
            return self.transform_group_mavg(df)
        else:
            raise ValueError('No such smooth method: %r. Use "lm" or "mavg".'
                             % (method,))

smooth = StatSmooth

class StatBin(Stat):
    default_geom = 'hist'
    default_aes = Aes(stat_y='weight')

    def transform_group(self, df, scales=None):
        if scales is not None:
            x_scale = next(s for s in scales.values() if 'x' in s.aes)
        else:
            x_scale = None

        if x_scale and x_scale.level == scale.Level.DISCRETE:
            counts = df.x.value_counts()
            return pd.DataFrame({'x': counts.index,
                                 'weight': counts, 'width': 0.9})
        else:
            nbins = self.params.get('bins', 10)
            groups, bins = pd.cut(df.x, nbins, retbins=True)

        mids = pd.Series((bins[1:] + bins[:-1])/2,
                          index=groups.cat.categories)
        widths = pd.Series(bins[1:] - bins[:-1],
                           index=groups.cat.categories)
        counts = df.groupby(groups).x.count()

        return pd.DataFrame({'x': mids, 'weight': counts, 'width': widths})

bin = StatBin

class StatBoxplot(Stat):
    default_geom = 'boxplot'

    def transform_group(self, df, scales=None):
        quants = df.y.quantile([0, 0.25, 0.5, 0.75, 1])
        quants.index = 'ymin lower ymid upper ymax'.split()
        quants['x'] = df.x.mean()

        coef = self.params.get('outlier_coef', 1.5)

        if coef > 0:
            iqr = quants.upper - quants.lower
            bound_low = quants.lower - iqr*coef
            bound_high = quants.upper + iqr*coef

            inliers = (bound_low <= df.y) & (df.y <= bound_high)
            quants.ymin, quants.ymax = df.y[inliers].quantile([0, 1])

        frame = quants.to_frame().T

        outliers = df.y[~inliers].rename('youtlier').to_frame()
        outliers['x'] = quants.x

        frame = frame.append(outliers)
        frame.reset_index(drop=True, inplace=True)

        return frame

boxplot = StatBoxplot
