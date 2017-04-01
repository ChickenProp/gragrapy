from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

from .context import gragrapy as gg

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
    # Faceting a df gives only the groups in that df
    assert len(faceted) == 4

    # Each group is (name, data)
    for x in faceted:
        assert isinstance(x, tuple)
        assert len(x) == 2
        assert x[0] in faceter.facet_names
        assert isinstance(x[1], pd.DataFrame)

    # if the df doesn't have a group col, it goes in every facet group
    assert len(faceter.facet(pd.DataFrame({'Val': range(5)}))) == 10

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
