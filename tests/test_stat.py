from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import pytest
import pandas as pd
import numpy as np

from .context import gragrapy as gg
from . import assert_data_equal

def test_stat_identity():
    stat = gg.stat.identity()
    iris = gg.data.iris
    assert_data_equal(iris, stat.transform(iris))

@pytest.mark.parametrize('window', [5, 25])
def test_stat_smooth_mavg(window):
    x = sorted(np.random.randn(50)*4)
    y = sorted(np.random.randn(50))
    df = pd.DataFrame({'x': x, 'y': y})
    stat = gg.stat.smooth(method='mavg', window=window)
    trans = stat.transform_group(df)

    assert trans.x.isnull().sum() == 0
    assert trans.y.isnull().sum() == window-1
    assert trans.ymin.isnull().sum() == window-1
    assert trans.ymax.isnull().sum() == window-1

    # Check the error bars surround the smoothed curve
    assert (trans.y.isnull()
            | ((trans.ymin < trans.y) & (trans.y < trans.ymax))).all()

    # The smoothed curve should be monotonically increasing
    diffs = trans.diff()[['x', 'y']]
    assert (diffs.isnull() | (diffs > 0)).all().all()

def test_stat_smooth_lm():
    x = sorted(np.random.randn(50)*4)
    y = sorted(np.random.randn(50))
    df = pd.DataFrame({'x': x, 'y': y})
    stat = gg.stat.smooth(method='lm')
    trans = stat.transform_group(df)

    # Check the error bars surround the smoothed curve
    assert ((trans.ymin < trans.y) & (trans.y < trans.ymax)).all()

    # The smoothed curve should be monotonically increasing
    diffs = trans.diff()[['x', 'y']]
    assert (diffs.isnull() | (diffs > 0)).all().all()

def test_stat_bin():
    df = pd.DataFrame({'x': [ 1,1,1,2,2,3 ]})
    trans = gg.stat.bin(bins=3).transform_group(df)
    assert set(trans.weight) == {1,2,3}

def test_stat_boxplot():
    df = pd.DataFrame({'x': 1, 'y': np.random.randn(100)})
    df = df.append(pd.DataFrame({'x': 1, 'y': [-10, -50, 300]}))
    trans = gg.stat.boxplot().transform_group(df)

    inliers = trans.youtlier.isnull()
    assert len(trans[inliers]) == 1

    stats = trans[inliers].iloc[0]
    assert stats.ymin < stats.lower < stats.ymid < stats.upper < stats.ymax
    assert stats.x == 1

    outliers = trans[~inliers]
    assert len(outliers) >= 3
    assert outliers['ymin lower ymid upper ymax'.split()].isnull().all().all()
    assert set(outliers.youtlier).issuperset({-10, -50, 300})


def test_grouping():
    class ToyStat(gg.stat.Stat):
        def transform_group(self, df, scales=None):
            return pd.DataFrame([[2,3],[5,7]], columns='a b'.split())

    df = pd.DataFrame([[1, 11, 21, 31, 41],
                       [1, 11, 21, 31, 40],
                       [1, 11, 21, 31, 41],
                       [2, 12, 22, 32, 42],
                       [2, 12, 22, 30, 42],
                       [2, 12, 22, 30, 42],
                       [3, 13, 23, 33, 43],
                       [3, 13, 23, 33, 43]],
                      columns='group a x y z'.split())
    expect = pd.DataFrame([[1, 2, 3, 21],
                           [1, 5, 7, 21],
                           [2, 2, 3, 22],
                           [2, 5, 7, 22],
                           [3, 2, 3, 23],
                           [3, 5, 7, 23]],
                          columns='group a b x'.split())

    assert_data_equal(ToyStat().transform(df), expect)
