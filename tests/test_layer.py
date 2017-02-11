from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

from .context import gragrapy as gg

def test_layer():
    assert gg.layer.Layer.find_geom('point') == gg.geom.point
