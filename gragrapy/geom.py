from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import numpy as np
import matplotlib.collections as collections
import matplotlib.patches as patches

from .layer import Layer, LayerComponent
from .aes import Aes

class Geom(LayerComponent):
    default_stat = 'identity'
    default_aes = Aes()

    def draw(self, ax, data):
        grouped = data.groupby('group')
        for name, group in grouped:
            self.draw_group(ax, group)

    def draw_group(self, ax, data):
        # If draw has been overridden but draw_group hasn't, then drawing a
        # single group probably works like drawing the whole dataset. This lets
        # callers not worry which to use.
        if self.__class__.draw != Geom.draw:
            self.draw(ax, data)
        else:
            raise NotImplementedError()

    def make_layer(self):
        return Layer(aes=self.aes, data=self.data, geom=self,
                     stat=self.params.get('stat', self.default_stat),
                     params=self.params)


class GeomPoint(Geom):
    def draw(self, ax, data):
        color = self.params.get('color', data.get('color', 'black'))
        ax.scatter(data['x'], data['y'], c=color, edgecolors='face')
point = GeomPoint

class GeomLine(Geom):
    # ax.plot doesn't support varying colors. To get that to work, I think I
    # need something like
    # http://matplotlib.org/examples/pylab_examples/multicolored_line.html

    def draw_group(self, ax, data):
        data = data.sort_values('x')
        color = self.params.get('color', data.get('color', 'black'))

        # We need segments to be a list of single-segment lines, i.e.
        # [ [p0, p1], [p1, p2], [p2, p3], ... ] where each pn is [xn, yn]
        points = np.array([data.x, data.y]).T.reshape(-1, 1, 2)
        segments = np.concatenate((points[:-1], points[1:]), axis=1)

        lc = collections.LineCollection(segments, colors=color)
        ax.add_collection(lc)
line = GeomLine

class GeomRibbon(Geom):
    def draw(self, ax, data):
        alpha = self.params.get('alpha', 1)
        color = self.params.get('color', data.get('color', 'black'))

        ax.fill_between(data['x'], data['ymin'], data['ymax'],
                        color=color, alpha=alpha)
ribbon = GeomRibbon

class GeomSmooth(Geom):
    default_stat = 'smooth'
    def __init__(self, aes=None, data=None, **params):
        Geom.__init__(self, aes, data, **params)

        self.geom_line = line(aes, data, **params)

        ribbon_params = dict(params, color='black', alpha=0.1)
        self.geom_ribbon = ribbon(aes, data, **ribbon_params)

    def draw_group(self, ax, data):
        self.geom_ribbon.draw_group(ax, data)
        self.geom_line.draw_group(ax, data)
smooth = GeomSmooth

class GeomBar(Geom):
    default_aes = Aes(width=Aes.const(1), ymin=Aes.const(0))
    def draw(self, ax, data):
        for _, row in data.iterrows():
            x = row.x - row.width/2
            height = row.y - row.ymin
            ax.add_patch(patches.Rectangle((x, row.ymin), row.width, height,
                                           fill='black'))
bar = GeomBar

class GeomHist(GeomBar):
    default_stat = 'bin'

hist = GeomHist
