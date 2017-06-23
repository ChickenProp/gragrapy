from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import pandas as pd

def sorted_unique(series):
    """Return a sorted list of the unique values in `series`."""
    # This handles Categorical data types, which sorted(series.unique()) fails
    # on. series.drop_duplicates() is slower than Series(series.unique()).
    return list(pd.Series(series.unique()).sort_values())

def single_value_columns(df):
    """Return a list of the columns in `df` that have only one value."""
    return { col: df[col].iloc[0] for col in df if df[col].nunique() == 1 }

class Params(dict):
    def __init__(self, *args, **kwargs):
        self.parent = args[0] if args else {}
        super(Params, self).__init__(**kwargs)

    def __getitem__(self, key):
        if key in self:
            return super(Params, self).__getitem__(key)
        else:
            return self.parent[key]

    def get(self, key, default=None):
        if key in self:
            return super(Params, self).__getitem__(key)
        else:
            return self.parent.get(key, default)
