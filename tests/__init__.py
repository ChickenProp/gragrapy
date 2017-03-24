from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import pandas as pd
import pandas.util.testing as pdtest
import pytest

def assert_data_equal(l, r):
    """Check whether DataFrames l and r are equal for gragrapy's purposes."""
    # pandas bug: assert_frame_equal doesn't check shapes properly.
    # Fixed upstream, but not released as of 2017-03-14.
    # (Fixed in pandas commit 55eccd9 on 2017-02-27.)
    assert l.shape == r.shape

    # check_like allows columns to be reordered, and inferred column types to be
    # different (needed in case of str/unicode ambiguity).
    pdtest.assert_frame_equal(l, r, check_like=True)
