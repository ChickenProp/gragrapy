from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import pandas as pd
import numpy as np

from .context import gragrapy as gg
from . import assert_data_equal

def test_stat_identity():
    stat = gg.stat.identity()
    iris = gg.data.iris
    assert_data_equal(iris, stat.transform(iris))

def test_stat_smooth():
    x = sorted(np.random.randn(50)*4)
    y = sorted(np.random.randn(50))
    df = pd.DataFrame({'x': x, 'y': y})
    stat = gg.stat.smooth()
    trans = stat.transform_group(df)

    assert trans.x.isnull().sum() == 0
    assert trans.y.isnull().sum() == 4
    assert trans.ymin.isnull().sum() == 4
    assert trans.ymax.isnull().sum() == 4

    # Check the error bars surround the smoothed curve
    assert (trans.y.isnull()
            | ((trans.ymin < trans.y) & (trans.y < trans.ymax))).all()

    # The smoothed curve should be monotonically increasing
    diffs = trans.diff()[['x', 'y']]
    assert (diffs.isnull() | (diffs > 0)).all().all()

def test_stat_bin():
    df = pd.DataFrame({'x': [ 1,1,1,2,2,3 ]})
    trans = gg.stat.bin(bins=3).transform_group(df)
    assert set(trans.weight) == {1,2,3}

def test_grouping():
    class ToyStat(gg.stat.Stat):
        def transform_group(self, df):
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
