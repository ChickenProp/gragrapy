from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import os

import numpy as np
import pandas as pd
import plotnine.data

_dataset_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            'datasets')

class Data(object):
    """A collection of datasets.

    Datasets are loaded lazily. Most of them come through R, and require the
    python module `r2py`.
    """
    def __getattr__(self, name):
        if hasattr(plotnine.data, name):
            dataset = getattr(plotnine.data, name)
        else:
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
