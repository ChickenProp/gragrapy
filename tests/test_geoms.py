from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

from .context import gragrapy as gg

def test_make_layer():
    g = gg.geom.Geom()
    assert g.make_layer() == gg.layer.Layer(geom=g, stat='identity')

    g = gg.geom.Geom(stat='smooth')
    assert g.make_layer() == gg.layer.Layer(geom=g, stat='smooth')
