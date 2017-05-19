from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

from .context import gragrapy as gg
from . import assert_data_equal
import pandas.util.testing as pdtest

import pandas as pd

def mkfacetdf(groups):
    return pd.DataFrame({'Group': list(groups) * 3,
                         'Val': range(len(groups) * 3)})

def test_facet():
    faceter = gg.facet('Group')
    df1 = mkfacetdf(range(4))
    df2 = mkfacetdf(range(3, 10)) # these deliberately overlap
    faceter.train([df1, df2])

    # Takes all group values as names
    assert len(faceter.facet_names) == 10

    faceted = faceter.facet(df1)
    pdtest.assert_series_equal(faceted['facet'], df1['Group'],
                               check_names=False)
    assert_data_equal(faceted.drop('facet', axis=1), df1)

    df3 = pd.DataFrame({'Val': range(5)})
    faceted = faceter.facet(df3)
    assert len(faceted) == len(df3) * len(faceter.facet_names)
    for name, data in faceted.groupby('facet'):
        data = data.drop('facet', axis=1).reset_index(drop=True)
        assert_data_equal(data, df3)

def test_shape():
    df = mkfacetdf(range(11))

    def shape(rows=None, cols=None):
        faceter = gg.facet('Group', rows=rows, cols=cols)
        faceter.train([df])
        return faceter.shape()

    assert shape() == (3, 4)
    assert shape(2) == (2, 6)
    assert shape(5) == (5, 3)
    assert shape(cols=2) == (6, 2)
    assert shape(cols=5) == (3, 5)
    assert shape(1, 2) == (1, 2)
    assert shape(5, 4) == (5, 4)
