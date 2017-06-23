from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import pandas as pd
import pandas.util.testing as pdtest
import pytest

from .context import gragrapy as gg
from . import assert_data_equal
Layer = gg.layer.Layer

def mklayer(geom='point', stat='identity', **kwargs):
    return Layer(geom=geom, stat=stat, **kwargs)

def mkdf(rows, cols, colnames, **kwargs):
    df = pdtest.makeCustomDataframe(rows, cols, **kwargs)
    df.columns = colnames.split()
    return df

def test_layer():
    assert Layer.find_geom('point') == gg.geom.point

def test_wrap_aes():
    class TestGeom(gg.geom.Geom):
        default_aes = gg.Aes(a='A1', c='C1', e='E1', g='G1')

    plot_aes = gg.Aes(b='B2', c='C2', f='F2', g='G2')

    layer = mklayer(geom=TestGeom(),
                    aes=gg.Aes(d='D3', e='E3', f='F3', g='G3'))


    assert layer.wrap_aes(plot_aes) \
        == gg.Aes(a='A1', b='B2', c='C2', d='D3', e='E3', f='F3', g='G3')

def test_default_data():
    df1 = mkdf(3, 1, 'x')
    df2 = mkdf(5, 1, 'y')

    layer = mklayer()
    pdtest.assert_frame_equal(layer.default_data(df1), df1)

    layer = mklayer(data=df2)
    pdtest.assert_frame_equal(layer.default_data(df1), df2)

def test_map_df():
    layer = mklayer()
    with pytest.raises(ValueError):
        layer.map_data(gg.Aes(x='foo'))

    data = mkdf(7, 2, 'foo bar')
    pdtest.assert_frame_equal(layer.map_data(gg.Aes(x='foo'), data),
                              pd.DataFrame({'x': data.foo}))

    layer = mklayer(data=data)
    pdtest.assert_frame_equal(layer.map_data(gg.Aes(x='foo')),
                              pd.DataFrame({'x': data.foo}))

    # ignore default data
    pdtest.assert_frame_equal(layer.map_data(gg.Aes(x='foo'),
                                             mkdf(5, 2, 'foo bar')),
                              pd.DataFrame({'x': data.foo}))

    # take layer aes into account
    layer = mklayer(data=data, aes=gg.Aes(y='bar'))
    pdtest.assert_frame_equal(layer.map_data(gg.Aes(x='foo')),
                              pd.DataFrame({'x': data.foo,
                                            'y': data.bar}))

def test_add_param_data():
    class TestLayerComponent(gg.layer.LayerComponent):
        default_params = gg.util.Params(color='black', alpha=1)
        data_params = {'color'}

    data = pd.DataFrame({'x': range(10), 'color': range(10, 20)})

    tlc = TestLayerComponent()
    assert_data_equal(data, tlc.add_param_data(data))

    tlc = TestLayerComponent(color='red', alpha=1)
    assert_data_equal(data.assign(color='red'), tlc.add_param_data(data))

    tlc = TestLayerComponent(alpha=1)
    assert_data_equal(data.assign(color='black'),
                      tlc.add_param_data(data.drop('color', axis=1)))
