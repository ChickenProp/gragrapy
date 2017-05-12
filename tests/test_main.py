from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

from .context import gragrapy as gg
from gragrapy.__main__ import parse_kwargs

def test_parse_kwargs():
    assert parse_kwargs([]) == {}
    assert parse_kwargs(['a=b', 'c=d']) == {'a': 'b', 'c': 'd'}
    assert parse_kwargs(['a=b=c', 'c=d']) == {'a': 'b=c', 'c': 'd'}
