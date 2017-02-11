from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import os

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm

from . import layer, geom, scale, stat
from .aes import Aes

class Plot(object):
    def __init__(self, data, aes):
        self.data = data
        self.aes = aes

        self.layers = []
        self.scales = {}

    def show(self):
        self.make()
        if not os.getenv('GRAGRAPY_NOSHOW'):
            plt.show()

    def __str__(self):
        self.show()
        return repr(self)

    def __repr__(self):
        return '<gragrapy.Plot>'

    def apply_theme(self):
        plt.style.use('ggplot')

        mpl.rc('patch', facecolor='k')
        from cycler import cycler
        mpl.rc('axes', prop_cycle=cycler(color=['k']))

    def get_theme(self):
        with mpl.rc_context():
            self.apply_theme()
            return mpl.rcParams

    def make(self):
        with mpl.rc_context():
            self.apply_theme()

            fig, ax = plt.subplots()

            for scl in self.scales.values():
                scl.apply()

            for layer in self.layers:
                aes = Aes.union(layer.geom.default_aes, self.aes, layer.aes)

                # If the aes has a constant, do the scales want to treat it
                # differently to if the data just has only one value? For
                # example, Aes(color='col') where data.col has only one value
                # "black", should maybe be different from
                # Aes(color=Aes.const('black'))? But maybe that second one
                # should actually be handled with geom(color='black') instead?

                mapped = aes.map_df(self.data)
                scaled = scale.Scale.apply_scales(mapped, self.scales)

                statted = layer.stat.transform(scaled)
                layer.draw(ax, statted)

            # Haven't implemented legends yet
            # plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

    def _copy(self):
        copy = Plot(self.data, self.aes)
        copy.layers = list(self.layers)
        copy.scales = dict(self.scales)

        return copy

    def __add__(self, other):
        copy = self._copy()

        if isinstance(other, list):
            for x in other:
                copy += x
        elif isinstance(other, type):
            copy += other()
        elif isinstance(other, layer.LayerComponent):
            copy.layers.append(other.make_layer())
        elif isinstance(other, layer.Layer):
            copy.layers.append(other)
        elif isinstance(other, scale.Scale):
            copy.scales[other.aes] = other

        return copy


def data(name):
    from rpy2.robjects import pandas2ri, r
    r.data(name)
    return pandas2ri.ri2py(r[name])

def datasets():
    """Return a list of the datasets available from `gg.data()`"""
    from rpy2.robjects import pandas2ri, r
    datasets = np.asarray(r.data()[2])
    return pd.DataFrame(datasets[:, 2:], columns=['name', 'description'])
