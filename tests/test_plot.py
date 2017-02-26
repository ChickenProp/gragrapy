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

    fake_data = pd.DataFrame({'Sepal.Length': [7.0, 7.3],
                              'Sepal.Width': [4, 5],
                              'FakeCol': ['Fake', 'Fake2']})
    plot = (gg.Plot(iris, gg.Aes(x='Sepal.Length', y='Sepal.Width')) + [
        gg.geom.line(color='r'),
        gg.geom.point(gg.Aes(color='Species')),
        gg.scale.color_qual,
        gg.stat.smooth,
        gg.geom.point(gg.Aes(color='FakeCol'), data=fake_data)
    ])
    plot.show()
    (plot + gg.facet('Species')).show()
