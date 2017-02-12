from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import pandas as pd
import pandas.util.testing as pdtest
import pytest

from .context import gragrapy as gg
Layer = gg.layer.Layer

def test_layer():
    assert Layer.find_geom('point') == gg.geom.point

def test_wrap_aes():
    class TestGeom(gg.geom.Geom):
        default_aes = gg.Aes(a='A1', c='C1', e='E1', g='G1')

    plot_aes = gg.Aes(b='B2', c='C2', f='F2', g='G2')

    layer = Layer(geom=TestGeom(), stat='identity',
                  aes=gg.Aes(d='D3', e='E3', f='F3', g='G3'))


    assert layer.wrap_aes(plot_aes) \
        == gg.Aes(a='A1', b='B2', c='C2', d='D3', e='E3', f='F3', g='G3')

def test_map_df():
    layer = Layer(geom='point', stat='identity')
    with pytest.raises(ValueError):
        layer.map_data(gg.Aes(x='foo'))

    iris = gg.data('iris')
    pdtest.assert_frame_equal(layer.map_data(gg.Aes(x='Petal.Width'), iris),
                              pd.DataFrame({'x': iris['Petal.Width']}))

    layer = Layer(geom='point', stat='identity', data=iris)
    pdtest.assert_frame_equal(layer.map_data(gg.Aes(x='Petal.Width')),
                              pd.DataFrame({'x': iris['Petal.Width']}))

    pdtest.assert_frame_equal(layer.map_data(gg.Aes(x='Petal.Width'),
                                             iris.iloc[:10]),
                              pd.DataFrame({'x': iris['Petal.Width']}))

    layer = Layer(geom='point', stat='identity', data=iris,
                  aes=gg.Aes(y='Petal.Length'))
    pdtest.assert_frame_equal(layer.map_data(gg.Aes(x='Petal.Width')),
                              pd.DataFrame({'x': iris['Petal.Width'],
                                            'y': iris['Petal.Length']}))
