from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import pytest
import pandas as pd

from .context import gragrapy as gg

def test_make_layer():
    g = gg.geom.Geom()
    assert g.make_layer() == gg.layer.Layer(geom=g, stat='identity')

    # stat=smooth gets passed to the stat on LHS
    g = gg.geom.Geom(stat='smooth')
    assert g.make_layer() == gg.layer.Layer(geom=g, stat='smooth',
                                            params={'stat': 'smooth'})

    g = gg.geom.Geom(gg.Aes(x='foo'))
    assert g.make_layer() == gg.layer.Layer(aes=gg.Aes(x='foo'), geom=g,
                                            stat='identity')

def test_draw_inheritance():
    df1 = pd.DataFrame({'group': [1], 'x': [1]})
    df2 = pd.DataFrame({'x': [1]})

    class Geom2(gg.geom.Geom):
        def draw(self, ax, data):
            raise ValueError('called draw')

    class Geom3(gg.geom.Geom):
        def draw_group(self, ax, data):
            raise ValueError('called draw_group')

    g = gg.geom.Geom()
    with pytest.raises(NotImplementedError):
        g.draw(None, pd.DataFrame({'group': [1], 'x': [1]}))
    with pytest.raises(NotImplementedError):
        g.draw_group(None, pd.DataFrame({'x': [1]}))

    g = Geom2()
    with pytest.raises(ValueError) as exc:
        g.draw(None, df1)
    assert str(exc.value) == 'called draw'

    with pytest.raises(ValueError) as exc:
        g.draw_group(None, df2)
    assert str(exc.value) == 'called draw'

    g = Geom3()
    with pytest.raises(ValueError) as exc:
        g.draw(None, df1)
    assert str(exc.value) == 'called draw_group'

    with pytest.raises(ValueError) as exc:
        g.draw_group(None, df2)
    assert str(exc.value) == 'called draw_group'
