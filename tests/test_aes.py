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
    aes = gg.aes(x='foo', y='bar', stat_x='baz')
    assert_data_equal(aes.map_data(df),
                      pd.DataFrame({'x': x, 'y': y}))

    assert_data_equal(gg.aes().map_data(df), pd.DataFrame({}))

def test_map_stat():
    x = range(10)
    y = range(10, 20)
    z = range(20, 30)
    df = pd.DataFrame({'x': x, 'y': y, 'z': z})
    aes = gg.aes(x='foo', stat_x='y', stat_w='x')

    assert_data_equal(aes.map_stat(df),
                      pd.DataFrame({'x': y, 'y': y, 'z': z, 'w': x}))

    assert_data_equal(gg.aes().map_stat(df), df)

def test_eq():
    assert gg.aes() == gg.aes()
    assert gg.aes(x='foo') == gg.aes(x='foo')
    assert gg.aes(x='foo', stat_x='bar') == gg.aes(x='foo', stat_x='bar')
    assert gg.aes(x='foo') != gg.aes(x='bar')
    assert gg.aes(x='foo') != gg.aes(y='foo')
    assert gg.aes(x='foo', stat_x='bar') == gg.aes(x='foo', stat_x='baz')

    # Check ne is implemented
    assert not gg.aes(x='foo') != gg.aes(x='foo')

    assert gg.aes(x=gg.aes.const('black')) == gg.aes(x=gg.aes.const('black'))
    assert gg.aes(x=gg.aes.const('black')) != gg.aes(x=gg.aes.const('red'))

def test_union():
    a = gg.aes(x='foo', y='bar', stat_x='FOO', stat_y='BAR')
    b = gg.aes(y='baz', z='bletch', stat_y='BAZ', stat_z='BLETCH')
    c = gg.aes(z='quux', w='zorb', stat_z='QUUX', stat_w='ZORB')
    assert gg.aes.union(a, b, c) \
        == gg.aes(x='foo', y='baz', z='quux', w='zorb',
                  stat_x='FOO', stat_y='BAZ', stat_z='QUUX', stat_w='ZORB')
