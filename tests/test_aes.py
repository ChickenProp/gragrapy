from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import pandas as pd
import pandas.util.testing as pdtest

from .context import gragrapy as gg

def test_map_df():
    x = range(10)
    y = range(10, 20)
    df = pd.DataFrame({'foo': x, 'bar': y})
    pdtest.assert_frame_equal(gg.Aes(x='foo', y='bar').map_df(df),
                              pd.DataFrame({'x': x, 'y': y}))

def test_eq():
    assert gg.Aes() == gg.Aes()
    assert gg.Aes(x='foo') == gg.Aes(x='foo')
    assert gg.Aes(x='foo') != gg.Aes(x='bar')
    assert gg.Aes(x='foo') != gg.Aes(y='foo')

    # Check ne is implemented
    assert not gg.Aes(x='foo') != gg.Aes(x='foo')

    assert gg.Aes(x=gg.Aes.const('black')) == gg.Aes(x=gg.Aes.const('black'))
    assert gg.Aes(x=gg.Aes.const('black')) != gg.Aes(x=gg.Aes.const('red'))

def test_union():
    a = gg.Aes(x='foo', y='bar')
    b = gg.Aes(y='baz', z='bletch')
    c = gg.Aes(z='quux', w='zorb')
    assert gg.Aes.union(a, b, c) == gg.Aes(x='foo', y='baz', z='quux', w='zorb')
