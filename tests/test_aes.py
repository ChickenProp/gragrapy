from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import pandas as pd
import pandas.util.testing as pdtest
import pytest

from .context import gragrapy as gg

def assert_data_equal(l, r):
    """Check whether DataFrames l and r are equal for gragrapy's purposes."""
    # pandas bug: assert_frame_equal doesn't check shapes properly.
    # Fixed upstream, but not released as of 2017-03-14.
    # (Fixed in pandas commit 55eccd9 on 2017-02-27.)
    assert l.shape == r.shape

    # check_like allows columns to be reordered, and inferred column types to be
    # different (needed in case of str/unicode ambiguity).
    pdtest.assert_frame_equal(l, r, check_like=True)

def test_assert_data_equal():
    x = range(10)
    y = range(10, 20)
    z = range(20, 30)

    assert_data_equal(pd.DataFrame(zip(x, y), columns=list('xy')),
                      pd.DataFrame(zip(x, y), columns=list('xy')))

    assert_data_equal(pd.DataFrame(zip(x, y), columns=list('xy')),
                      pd.DataFrame(zip(y, x), columns=list('yx')))

    with pytest.raises(AssertionError):
        assert_data_equal(pd.DataFrame(zip(x, y), columns=list('xy')),
                          pd.DataFrame(zip(x, y, z), columns=list('xyz')))

    with pytest.raises(AssertionError):
        l = pd.DataFrame(zip(x, y), columns=list('xy'))
        r = pd.DataFrame(zip(x), columns=list('x'))
        assert_data_equal(l, r)




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
