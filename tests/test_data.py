from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import pandas as pd

from .context import gragrapy as gg

def test_data():
    iris = gg.data.iris
    assert isinstance(iris, pd.DataFrame)
    assert len(iris) == 150

def test_diamonds():
    diamonds = gg.data.diamonds
    assert isinstance(diamonds, pd.DataFrame)
    assert len(diamonds) == 53940
    assert diamonds.cut.dtype == 'category'
    assert diamonds.color.dtype == 'category'
    assert diamonds.clarity.dtype == 'category'

def test_anscombe():
    anscombe = gg.data.anscombe
    assert isinstance(anscombe, pd.DataFrame)
    assert len(anscombe) == 44

def test_datasets():
    datasets = gg.data.datasets()
    assert isinstance(datasets, pd.DataFrame)
    assert len(datasets) > 0
