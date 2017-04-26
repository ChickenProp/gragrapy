from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import os

import pandas as pd

from .context import gragrapy as gg

iris = gg.data.iris

def plot_tester(plot):
    def tester():
        plot().show()
    return tester

def test_save(tmpdir):
    filename = tmpdir.join('test.png')
    (gg.Plot(gg.data.iris, gg.Aes(x='Petal.Length', y='Petal.Width')) + [
        gg.geom.point
    ]).save(str(filename))
    assert filename.check()

@plot_tester
def test_plot1():
    return (gg.Plot(gg.data.ChickWeight,
                    gg.Aes(x='Time', y='weight', color='Diet')) + [
        gg.geom.point,
        #gg.geom.line(gg.Aes(group='Chick')),
        gg.stat.smooth,
        gg.title('Chick weights colored according to diet with a smooth curve'),
    ])

def test_plot():
    fake_data = pd.DataFrame({'Sepal.Length': [7.0, 7.3],
                              'Sepal.Width': [4, 5],
                              'FakeCol': ['Fake', 'Fake2']})
    plot = (gg.Plot(iris, gg.Aes(x='Sepal.Length', y='Sepal.Width')) + [
        gg.geom.line(color='r'),
        gg.geom.point(gg.Aes(color='Species')),
        gg.stat.smooth,
        gg.geom.point(gg.Aes(color='FakeCol'), data=fake_data),
        gg.title('irises colored by species with a red line and a smooth\n'
                 'curve, plus two fake datapoints'),
    ])
    plot.show()
    (plot + [
        gg.facet('Species'),
        gg.title('previous plot faceted by species'),
    ]).show()

    plot = gg.Plot(iris, gg.Aes(x='Sepal.Length', y='Sepal.Width',
                                color='Sepal.Length'))
    (plot + [
        gg.geom.line,
        gg.geom.point,
        gg.stat.smooth,
        gg.scale.x.sqrt((3, 9)),
        gg.scale.y.continuous((1, 8)),
        gg.title('irises colored by sepal length with lots of margin'),
    ]).show()

    data = pd.DataFrame({'xpos': 'a b c d e'.split(),
                         'height': [1, 7, 2, 5, 3]})
    (gg.Plot(data, gg.Aes(x='xpos', y='height')) + [
        gg.geom.bar,
        gg.scale.x.discrete(labels='foo bar baz bletch quux'.split()),
        gg.scale.y.sqrt,
        gg.title('fake data, discrete x axis, sqrt y axis'),
    ]).show()

    import numpy as np
    data = pd.DataFrame({'foo': np.random.randn(10000)})
    (gg.Plot(data, gg.Aes(x='foo')) + [
        gg.geom.hist(bins=100),
        gg.title('approximately normal histogram'),
    ]).show()
