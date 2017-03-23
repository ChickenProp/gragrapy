from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import pandas as pd

from .context import gragrapy as gg
util = gg.util

def test_sorted_unique():
    s = pd.Series([5, 5, 8, 3, 1, 2])
    assert util.sorted_unique(s) == [1, 2, 3, 5, 8]

    s = pd.Series('Bravo Charlie Alpha Delta Delta Echo'.split())
    assert util.sorted_unique(s) == 'Alpha Bravo Charlie Delta Echo'.split()

    s = pd.Series(pd.Categorical('Wed Mon Thu Thu Fri Wed'.split(),
                                 categories='Mon Tue Wed Thu Fri'.split(),
                                 ordered=True))
    assert util.sorted_unique(s) == 'Mon Wed Thu Fri'.split()

    s = pd.Series(pd.Categorical('Wed Mon Thu Thu Fri Wed'.split(),
                                 categories='Mon Tue Wed Thu Fri'.split(),
                                 ordered=False))
    assert sorted(util.sorted_unique(s)) == sorted('Mon Wed Thu Fri'.split())

def test_single_value_columns():
    df = pd.DataFrame([[1, 2, 3, 4, 5],
                       [1, 0, 3, 0, 5],
                       [1, 2, 3, 0, 0]],
                      columns='A B C D E'.split())
    assert util.single_value_columns(df) == {'A': 1, 'C': 3}

    # Make sure the index doesn't need to contain 0
    df.index = 'foo bar baz'.split()
    assert util.single_value_columns(df) == {'A': 1, 'C': 3}
