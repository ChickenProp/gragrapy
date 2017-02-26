from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import math

import pandas as pd

from . import util

class Faceter(object):
    """Split plots into several subplots, on the value of a data column."""
    def __init__(self, column, rows=None, cols=None):
        self.column = column
        self.rows = rows
        self.cols = cols

    def train(self, datasets):
        """Learn the features of all datasets, for later faceting."""
        cols = [ df[self.column] for df in datasets if self.column in df ]
        one_col = pd.concat(cols, ignore_index=True)
        self.facet_names = util.sorted_unique(one_col)

    def shape(self):
        """Return the shape of the facet grid as a (rows, cols) tuple.

        Assumes the Faceter has already been trained."""
        rows = self.rows
        cols = self.cols

        num_facets = len(self.facet_names)
        if rows is None and cols is None:
            rows = int(math.floor(math.sqrt(num_facets)))
            cols = int(math.ceil(num_facets/rows))
        elif rows is not None and cols is None:
            cols = int(math.ceil(num_facets/rows))
        elif cols is not None and rows is None:
            rows = int(math.ceil(num_facets/cols))

        return rows, cols

    def facet(self, data):
        """Facet a dataset.

        Each facet gets the subset of the data corresponding to the value in the
        facet column. If the dataset lacks the facet column, then every facet
        gets a copy of the data."""
        if self.column in data:
            return data.groupby(data[self.column])
        else:
            return [ (name, data) for name in self.facet_names ]

facet = Faceter

class NullFaceter(Faceter):
    """A Faceter that puts all datapoints into a single facet."""
    def __init__(self):
        self.facet_names = ['']

    def train(self, datasets):
        pass

    def shape(self):
        return 1, 1

    def facet(self, data):
        return [('', data)]
