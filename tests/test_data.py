from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import pandas as pd

from .context import gragrapy as gg

def test_data():
    iris = gg.data.iris
    assert isinstance(iris, pd.DataFrame)
    assert len(iris) == 150

def test_datasets():
    datasets = gg.data.datasets()
    assert isinstance(datasets, pd.DataFrame)
    assert len(datasets) > 0
