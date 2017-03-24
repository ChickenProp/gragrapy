from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import pandas as pd
import pandas.util.testing as pdtest
import pytest

from .context import gragrapy as gg
from . import assert_data_equal

def test_map_data():
    x = range(10)
    y = range(10, 20)
    df = pd.DataFrame({'foo': x, 'bar': y})
    aes = gg.Aes(x='foo', y='bar', stat_x='baz')
    assert_data_equal(aes.map_data(df),
                      pd.DataFrame({'x': x, 'y': y}))

    assert_data_equal(gg.Aes().map_data(df), pd.DataFrame({}))

def test_map_stat():
    x = range(10)
    y = range(10, 20)
    z = range(20, 30)
    df = pd.DataFrame({'x': x, 'y': y, 'z': z})
    aes = gg.Aes(x='foo', stat_x='y', stat_w='x')

    assert_data_equal(aes.map_stat(df),
                      pd.DataFrame({'x': y, 'y': y, 'z': z, 'w': x}))

    assert_data_equal(gg.Aes().map_stat(df), df)

def test_eq():
    assert gg.Aes() == gg.Aes()
    assert gg.Aes(x='foo') == gg.Aes(x='foo')
    assert gg.Aes(x='foo', stat_x='bar') == gg.Aes(x='foo', stat_x='bar')
    assert gg.Aes(x='foo') != gg.Aes(x='bar')
    assert gg.Aes(x='foo') != gg.Aes(y='foo')
    assert gg.Aes(x='foo', stat_x='bar') == gg.Aes(x='foo', stat_x='baz')

    # Check ne is implemented
    assert not gg.Aes(x='foo') != gg.Aes(x='foo')

    assert gg.Aes(x=gg.Aes.const('black')) == gg.Aes(x=gg.Aes.const('black'))
    assert gg.Aes(x=gg.Aes.const('black')) != gg.Aes(x=gg.Aes.const('red'))

def test_union():
    a = gg.Aes(x='foo', y='bar', stat_x='FOO', stat_y='BAR')
    b = gg.Aes(y='baz', z='bletch', stat_y='BAZ', stat_z='BLETCH')
    c = gg.Aes(z='quux', w='zorb', stat_z='QUUX', stat_w='ZORB')
    assert gg.Aes.union(a, b, c) \
        == gg.Aes(x='foo', y='baz', z='quux', w='zorb',
                  stat_x='FOO', stat_y='BAZ', stat_z='QUUX', stat_w='ZORB')
