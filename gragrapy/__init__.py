from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import pandas as pd
import numpy as np

from . import layer, geom, scale, stat
from .plot import Plot
from .aes import Aes
from .faceter import facet

def data(name):
    from rpy2.robjects import pandas2ri, r
    r.data(name)
    return pandas2ri.ri2py(r[name])

def datasets():
    """Return a list of the datasets available from `gg.data()`"""
    from rpy2.robjects import pandas2ri, r
    datasets = np.asarray(r.data()[2])
    return pd.DataFrame(datasets[:, 2:], columns=['name', 'description'])
