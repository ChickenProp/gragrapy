from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

# Test our testing framework itself

import pandas as pd
import pytest

from . import assert_data_equal

def test_assert_data_equal():
    x = range(10)
    y = range(10, 20)
    z = range(20, 30)

    assert_data_equal(pd.DataFrame(list(zip(x, y)), columns=list('xy')),
                      pd.DataFrame(list(zip(x, y)), columns=list('xy')))

    assert_data_equal(pd.DataFrame(list(zip(x, y)), columns=list('xy')),
                      pd.DataFrame(list(zip(y, x)), columns=list('yx')))

    with pytest.raises(AssertionError):
        assert_data_equal(pd.DataFrame(list(zip(x, y)), columns=list('xy')),
                          pd.DataFrame(list(zip(x, y, z)), columns=list('xyz')))

    with pytest.raises(AssertionError):
        l = pd.DataFrame(list(zip(x, y)), columns=list('xy'))
        r = pd.DataFrame(list(zip(x)), columns=list('x'))
        assert_data_equal(l, r)
