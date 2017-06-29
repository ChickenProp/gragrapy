from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import os

import plotnine as p9

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

    @staticmethod
    def _from_p9(p9plot):
        plt = Plot.__new__(Plot)
        plt.p9plot = p9plot
        return plt

plot = Plot
