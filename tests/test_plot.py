from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import pandas as pd

from .context import gragrapy as gg

iris = gg.data.iris

def test_plot():
    (gg.Plot(gg.data.ChickWeight,
             gg.Aes(x='Time', y='weight', color='Diet')) + [
        gg.geom.point,
        #gg.geom.line(gg.Aes(group='Chick')),
        gg.stat.smooth,
    ]).show()

    fake_data = pd.DataFrame({'Sepal.Length': [7.0, 7.3],
                              'Sepal.Width': [4, 5],
                              'FakeCol': ['Fake', 'Fake2']})
    plot = (gg.Plot(iris, gg.Aes(x='Sepal.Length', y='Sepal.Width')) + [
        gg.geom.line(color='r'),
        gg.geom.point(gg.Aes(color='Species')),
        gg.stat.smooth,
        gg.geom.point(gg.Aes(color='FakeCol'), data=fake_data)
    ])
    plot.show()
    (plot + gg.facet('Species')).show()

    plot = gg.Plot(iris, gg.Aes(x='Sepal.Length', y='Sepal.Width',
                                color='Sepal.Length'))
    (plot + [
        gg.geom.line,
        gg.geom.point,
        gg.stat.smooth,
        gg.scale.x.continuous((3, 9)),
        gg.scale.y.continuous((1, 8)),
    ]).show()

    data = pd.DataFrame({'xpos': 'a b c d e'.split(),
                         'height': [1, 7, 2, 5, 3]})
    (gg.Plot(data, gg.Aes(x='xpos', y='height')) + [
        gg.geom.bar,
        gg.scale.x.discrete(labels='foo bar baz bletch quux'.split())
    ]).show()

    import numpy as np
    data = pd.DataFrame({'foo': np.random.randn(10000)})
    (gg.Plot(data, gg.Aes(x='foo')) + gg.geom.hist(bins=100)).show()
