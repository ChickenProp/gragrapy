from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import numpy as np
import pandas as pd

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
        """Return a list of the datasets available from `gg.data`.

        Note that not all datasets are pandas DataFrames."""
        from rpy2.robjects import pandas2ri, r
        datasets = np.reshape(r.data()[2], (4, -1)).T
        return pd.DataFrame(datasets[:, 2:], columns=['name', 'description'])

data = Data()
