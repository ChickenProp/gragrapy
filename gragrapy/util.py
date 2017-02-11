from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import pandas as pd

def sorted_unique(series):
    # This handles Categorical data types, which sorted(series.unique()) fails
    # on. series.drop_duplicates() is slower than Series(series.unique()).
    return list(pd.Series(series.unique()).sort_values())
