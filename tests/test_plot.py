from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import pandas as pd

from .context import gragrapy as gg

iris = gg.data('iris')

def test_plot():
    # Good dataset for when group works
    # (gg.Plot(gg.data('ChickWeight'),
    #          gg.Aes(x='Time', y='weight', color='Diet', group='Chick'))) + [
    #     gg.geom.point,
    #     gg.geom.line,
    #     gg.scale.color_qual
    # ]).show()

    (gg.Plot(iris,
             gg.Aes(x='Sepal.Length', y='Sepal.Width', color='Species')) + [
        gg.geom.line(color='r'),
        gg.geom.point,
        gg.scale.color_qual,
        gg.stat.smooth,
    ]).show()
