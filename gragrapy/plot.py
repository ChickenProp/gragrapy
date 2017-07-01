from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import os

import plotnine as p9
from . import geom, stat, scale, coord

class Plot(object):
    def __init__(self, *args, **kwargs):
        self.p9plot = p9.ggplot(*args, **kwargs)

    def show(self):
        repr(self.p9plot)

    def save(self, *args, **kwargs):
        self.p9plot.save(*args, **kwargs)

    def __str__(self):
        return '<gragrapy.plot.Plot>'

    def __repr__(self):
        self.show()
        return str(self)

    def __iadd__(self, other):
        if isinstance(other, list):
            for x in other:
                self += x
        elif isinstance(other, type):
            self += other()
        else:
            self.p9plot += other

        return self

    def __add__(self, other):
        if isinstance(other, list):
            plt = self
            for x in other:
                plt = plt + x
            return plt
        elif isinstance(other, type):
            return self + other()
        else:
            return Plot._from_p9(self.p9plot + other)

    def aes(self, *args, **kwargs):
        return self + p9.aes(*args, **kwargs)

    def geom(self, *args, **kwargs):
        return self + geom._make_geom(*args, **kwargs)

    def stat(self, *args, **kwargs):
        return self + stat._make_stat(*args, **kwargs)

    def scale(self, *args, **kwargs):
        return self + scale._make_scale(*args, **kwargs)

    def facet(self, *args, **kwargs):
        return self + p9.facet_wrap(*args, **kwargs)

    def facet_grid(self, *args, **kwargs):
        return self + p9.facet_grid(*args, **kwargs)

    def coord(self, *args, **kwargs):
        return self + coord._make_coord(*args, **kwargs)

    def title(self, title):
        return self + p9.ggtitle(title)

    def labels(self, title=None, x=None, y=None):
        labs = [
            p9.ggtitle(title) if title is not None else None,
            p9.xlab(x) if x is not None else None,
            p9.ylab(y) if y is not None else None
        ]
        return self + [ l for l in labs if l is not None ]

    @staticmethod
    def _from_p9(p9plot):
        plt = Plot.__new__(Plot)
        plt.p9plot = p9plot
        return plt

plot = Plot
