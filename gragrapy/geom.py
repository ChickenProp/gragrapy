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
        pass

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

    def draw(self, ax, data):
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
        color = self.params.get('color', data.get('color'), 'black')
        ax.fill_between(data['x'], data['ymin'], data['ymax'], color=color)
ribbon = GeomRibbon

class GeomSmooth(Geom):
    def draw(self, ax, data):
        ax.fill_between(data['x'], data['ymin'], data['ymax'], alpha=0.1)
        ax.plot(data['x'], data['y'])
smooth = GeomSmooth

class GeomBar(Geom):
    default_aes = Aes(width=Aes.const(1))
    def draw(self, ax, data):
        for _, row in data.iterrows():
            x = row.x - row.width/2
            ax.add_patch(patches.Rectangle((x, 0), row.width, row.y,
                                           fill='black'))
bar = GeomBar

class GeomHist(GeomBar):
    default_stat = 'bin'

hist = GeomHist
