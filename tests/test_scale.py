from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import pandas as pd

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
