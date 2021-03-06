from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import os

import numpy as np
import pandas as pd

_dataset_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            'datasets')

class Data(object):
    """A collection of datasets.

    Datasets are loaded lazily. Most of them come through R, and require the
    python module `r2py`.
    """
    def __getattr__(self, name):
        from rpy2.robjects import pandas2ri, r
        r.data(name)
        dataset = pandas2ri.ri2py(r[name])
        setattr(self, name, dataset)
        return dataset

    @staticmethod
    def datasets():
        """Return a partial list of the datasets available from `gg.data`.

        Note that not all datasets are pandas DataFrames."""
        from rpy2.robjects import pandas2ri, r
        datasets = np.reshape(r.data()[2], (4, -1)).T
        return pd.DataFrame(datasets[:, 2:], columns=['name', 'description'])

    _diamonds = None
    @property
    def diamonds(self):
        if self._diamonds is not None:
            return self._diamonds

        diamonds_path = os.path.join(_dataset_dir, 'diamonds.csv')
        result = self._diamonds = pd.read_csv(diamonds_path,
                                              dtype={'cut': 'category',
                                                     'color': 'category',
                                                     'clarity': 'category'})
        result.cut.cat.reorder_categories(['Fair', 'Good', 'Very Good',
                                           'Premium', 'Ideal'],
                                          ordered=True, inplace=True)
        result.color.cat.reorder_categories(list('DEFGHIJ'),
                                            ordered=True, inplace=True)
        result.clarity.cat.reorder_categories(['I1', 'SI2', 'SI1', 'VS2', 'VS1',
                                               'VVS2', 'VVS1', 'IF'],
                                              ordered=True, inplace=True)
        return result

    _diamonds_small = None
    @property
    def diamonds_small(self):
        if self._diamonds_small is not None:
            return self._diamonds_small

        self._diamonds_small = self.diamonds.sample(frac=1/10, random_state=42)
        return self._diamonds_small

    _anscombe = None
    @property
    def anscombe(self):
        if self._anscombe is not None:
            return self._anscombe

        anscombe_path = os.path.join(_dataset_dir, 'anscombe.csv')
        result = self._anscombe = pd.read_csv(anscombe_path)
        return result

data = Data()
