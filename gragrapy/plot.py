from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import os

import plotnine as p9
from . import geom, stat, scale

class Plot(object):
    def __init__(self, *args, **kwargs):
        self.p9plot = p9.ggplot(*args, **kwargs)

    def show(self):
        repr(self.p9plot)

    def save(self, *args, **kwargs):
        self.p9plot.save(*args, **kwargs)

    def __str__(self):
        self.show()
        return repr(self)

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

    def geom(self, *args, **kwargs):
        return self + geom._make_geom(*args, **kwargs)

    def stat(self, *args, **kwargs):
        return self + stat._make_stat(*args, **kwargs)

    def scale(self, *args, **kwargs):
        return self + scale._make_scale(*args, **kwargs)

    def facet(self, *args, **kwargs):
        return self + p9.facet_wrap(*args, **kwargs)

    def title(self, title):
        return self + p9.ggtitle(title)

    @staticmethod
    def _from_p9(p9plot):
        plt = Plot.__new__(Plot)
        plt.p9plot = p9plot
        return plt

plot = Plot
