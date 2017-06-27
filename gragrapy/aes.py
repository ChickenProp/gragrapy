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
    """Aesthetic mapping.

    An Aes takes data supplied to a Layer, and makes it suitable for passing to
    a Geom or Stat."""
    const = AesConstCol

    def __init__(self, **kwargs):
        """Args that start with 'stat_' will be used by `map_stat`. Others will
        be used by `map_data`."""
        self.mappings = { k: v for k,v in kwargs.items()
                          if not k.startswith('stat_') }
        self.stat_mappings = { k[5:]: v for k,v in kwargs.items()
                               if k.startswith('stat_') }

    def map_col(self, df, col):
        if isinstance(col, AesConstCol):
            return col.val
        else:
            return df[col]

    def map_data(self, data):
        """Convert a DataFrame using the standard mappings.

        Only mapped columns are preserved; e.g. if `self.mappings` is empty,
        then this returns an empty DataFrame.
        """
        # If the aes has a constant, that gets treated the same as if the
        # dataframe has a constant value. Might scales want to treat it
        # differently? If so, we'll need to distinguish those results somehow
        # (not necessarily in this method).

        # For example, Aes(color='col') where df.col has only one value 'black'.
        # Should that be different from Aes(color=Aes.const('black'))?
        # Maybe that second one should be handled with geom(color='black')
        # instead?
        return pd.DataFrame({ k: self.map_col(data, v)
                              for k, v in self.mappings.items() })

    def map_stat(self, stat):
        """Convert a DataFrame using the stat mappings.

        The original DataFrame's columns are preserved; e.g. if
        `self.stat_mappings` is empty, then this returns the original DataFrame.
        """
        if not self.stat_mappings:
            return stat

        copy = stat.copy()
        for k,v in self.stat_mappings.items():
            copy[k] = self.map_col(stat, v)
        return copy

    def scale_names(self):
        d = dict(self.mappings)
        d.update(self.stat_mappings)
        return d

    def __eq__(self, other):
        return type(self) is type(other) and other.mappings == self.mappings
    def __ne__(self, other):
        return not self == other

    @staticmethod
    def union(*aess):
        """Return an Aes whose mappings are the union of the arguments'
        mappings.

        If a mapping is found in both arguments, the one from the second is
        kept."""
        mappings = dict()
        stat_mappings = dict()
        ret = Aes()

        for aes in aess:
            ret.mappings.update(aes.mappings)
            ret.stat_mappings.update(aes.stat_mappings)

        return ret
aes = Aes
