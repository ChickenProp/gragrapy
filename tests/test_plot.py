from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import os

import pandas as pd
import pytest

from .context import gragrapy as gg

def plot_tester(plot):
    def tester(tmpdir, cache, accept_plots, show_plots):
        filename = tmpdir.join('test.png')
        cache_key = 'gragrapy/plot-hash-%s' % (plot.__name__,)
        old_hash = cache.get(cache_key, None)

        plt = plot()
        plt.save(str(filename))
        new_hash = filename.computehash()

        if old_hash != new_hash:
            if accept_plots:
                cache.set(cache_key, new_hash)
            else:
                plt.show()
        elif show_plots:
            plt.show()

    tester.plot = plot
    return tester

def test_show():
    # This is annoying to run every time. Ideally we'd have it only run if the
    # user specifically asks for all plots to be shown.
    return
    (gg.plot(gg.data.iris, gg.aes(x='Petal.Length', y='Petal.Width')) + [
        gg.geom.point
    ]).show()

def test_save(tmpdir):
    filename = tmpdir.join('test.png')
    (gg.plot(gg.data.iris, gg.aes(x='Petal.Length', y='Petal.Width')) + [
        gg.geom.point
    ]).save(str(filename))
    assert filename.check()

@plot_tester
def test_plot1():
    return gg.plot(gg.data.ChickWeight,
                   gg.aes(x='Time', y='weight', color='Diet')).geom('point') + [
        #gg.geom.line(gg.aes(group='Chick')),
        gg.stat.smooth,
        gg.title('Chick weights colored according to diet'
                 ' with smooth curves per diet'),
    ]

@plot_tester
def test_plot2():
    fake_data = pd.DataFrame({'Sepal.Length': [7.0, 7.3],
                              'Sepal.Width': [4, 5],
                              'FakeCol': ['Fake', 'Fake2']})
    return (gg.plot(gg.data.iris, gg.aes(x='Sepal.Length', y='Sepal.Width'))
              .geom('line', color='r')
              .geom(gg.geom.point(gg.aes(color='Species')))
              .stat('smooth')
              .geom('point', gg.aes(color='FakeCol'), data=fake_data)
              .title('irises colored by species with a red line and a smooth\n'
                     'curve, plus two fake datapoints'))

@pytest.mark.xfail
@plot_tester
def test_plot3():
    return test_plot2.plot() + [
        gg.title('irises colored and faceted by species with a red line\n'
                 'and a smooth curve, plus two fake datapoints'),
        gg.facet('Species'),
    ]

@plot_tester
def test_plot4():
    plot = gg.plot(gg.data.iris, gg.aes(x='Sepal.Length', y='Sepal.Width',
                                color='Sepal.Length'))
    return plot + [
        gg.geom.line,
        gg.geom.point,
        gg.stat.smooth,
        gg.scale.x.sqrt(limits=(3, 9)),
        gg.scale.y.continuous(limits=(1, 8)),
        gg.title('irises colored by sepal length with lots of margin'),
    ]

@plot_tester
def test_plot5():
    data = pd.DataFrame({'xpos': 'a b c d e'.split(),
                         'height': [1, 7, 2, 5, 3],
                         'color': [True, True, False, False, True]})
    return (gg.plot(data, gg.aes(x='xpos', y='height', fill='color'))
              .geom('bar', stat='identity')
              .scale('x', 'discrete', labels='foo bar baz bletch quux'.split())
              .scale('y', 'sqrt')
              .title('fake data, discrete x axis, sqrt y axis'))

@plot_tester
def test_plot6():
    return gg.plot(gg.data.diamonds_small, gg.aes(x='price')) + [
        gg.geom.hist(bins=100),
        gg.title('histogram of diamond prices'),
    ]

@plot_tester
def test_plot7():
    return (gg.plot(gg.data.anscombe, gg.aes(x='x', y='y'))
              .geom('point')
              .stat('smooth', method='lm', geom='line', color='red')
              .facet('dataset')
              .title("Anscombe's quartet with linear regression lines"))

@pytest.mark.xfail
@plot_tester
def test_plot8():
    return gg.plot(gg.data.diamonds_small, gg.aes(x='carat', y='price')) + [
        # This is fundamentally unsupported by plotnine
        #gg.stat.smooth(gg.aes(y='..ymax..'), color='red'),

        # I think this should work, but apparently doesn't
        gg.stat.smooth(gg.aes(ymax='..y..'), color='red'),

        gg.geom.point(alpha=0.01),
        gg.title('low-alpha diamond prices by carat;'
                 ' smooth curve at top of error bars'),
    ]

@plot_tester
def test_plot9():
    return gg.plot(gg.data.diamonds_small, gg.aes(x='color', y='price')) \
        + gg.geom.boxplot + gg.coord.flip
