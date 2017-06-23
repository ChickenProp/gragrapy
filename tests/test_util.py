from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import pandas as pd
import pytest

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

def test_params():
    def _test_params(params, data, own):
        for k, v in data.items():
            assert params.get(k) == v
            assert params.get(k, -1) == v
            assert params[k] == v

            assert params.get('nonexistant') is None
            assert params.get('nonexistant', -1) == -1
            with pytest.raises(KeyError):
                params['nonexistent']

        assert set(params) == own
        assert set(params.items()) == set({ k:v for k,v in data.items()
                                            if k in own }.items())

    p1 = util.Params(a=0, b=1)
    _test_params(p1, {'a': 0, 'b': 1}, {'a', 'b'})

    p2 = util.Params(p1, b=2, c=3)
    _test_params(p2, {'a': 0, 'b': 2, 'c': 3}, {'b', 'c'})
