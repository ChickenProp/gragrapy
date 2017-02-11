from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import pandas as pd

class AesConstCol(object):
    def __init__(self, val):
        self.val = val

    def __eq__(self, other):
        return type(self) is type(other) and other.val == self.val
    def __ne__(self, other):
        return not self == other

class Aes(object):
    const = AesConstCol

    def __init__(self, **kwargs):
        self.mappings = kwargs

    def map_col(self, df, col):
        if isinstance(col, AesConstCol):
            return col.val
        else:
            return df[col]

    def map_df(self, df):
        return pd.DataFrame({ k: self.map_col(df, v)
                              for k, v in self.mappings.items() })

    def __eq__(self, other):
        return type(self) is type(other) and other.mappings == self.mappings
    def __ne__(self, other):
        return not self == other

    @staticmethod
    def union(*aess):
        """Return an Aes whose mappings are the union of the arguments' mappings.

        If a mapping is found in both arguments, the one from the second is kept.
        """
        mappings = dict()
        for aes in aess:
            mappings.update(aes.mappings)
        return Aes(**mappings)
