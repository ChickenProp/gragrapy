from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import numpy as np
import pandas as pd
import pandas.util.testing as pdtest

from .context import gragrapy as gg
Level = gg.scale.Level

def test_guess_level():
    # This doesn't test the 'unknown dtype' code branch. How could that be
    # tested?

    a = pd.Series([1, 2, 3])
    assert Level.guess_series_level(a) == Level.CONTINUOUS

    a = pd.Series([1.2, 2.1, 3])
    assert Level.guess_series_level(a) == Level.CONTINUOUS

    a = pd.Series('foo bar baz'.split())
    assert Level.guess_series_level(a) == Level.DISCRETE

def test_color_div():
    s1 = pd.Series(np.linspace(1, 10, 15), index=list('abcdefghijklmno'))
    s2 = pd.Series(np.linspace(15, 20, 10))
    scl = gg.scale.color.div()
    scl.train_map([s1, s2])
    mapped = scl.map(s1)

    pdtest.assert_index_equal(mapped.index, s1.index)
    for c in mapped:
        assert isinstance(c, tuple)
