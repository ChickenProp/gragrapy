from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm

from . import layer, scale, faceter

class Plot(object):
    def __init__(self, data, aes):
        self.data = data
        self.aes = aes

        self.layers = []
        self.scales = {}
        self.faceter = faceter.NullFaceter()

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

            scales = self.scales

            all_datasets = [ layer.default_data(self.data)
                             for layer in self.layers ]
            self.faceter.train(all_datasets)
            fig, ax_map = self._get_fig_axmap()

            all_statted = []
            for dataset, layer in zip(all_datasets, self.layers):
                for name, facet in self.faceter.facet(dataset):
                    mapped = layer.wrap_aes(self.aes).map_df(facet)
                    scales.update(scale.guess_default_scales(mapped, scales))

                    scaled1 = scale.Scale.transform_scales(mapped, scales)
                    statted = layer.stat.transform(scaled1)
                    all_statted.append((ax_map[name], layer, statted))

            for scl in scales.values():
                scl.apply()

            scale.Scale.train_scales([x[2] for x in all_statted], scales)

            for (ax, layer, statted) in all_statted:
                scaled2 = scale.Scale.map_scales(statted, scales)
                layer.draw(ax, scaled2)

                # We need this for geom.bar, which doesn't scale the view
                # itself. When x and y scales work properly, we probably want to
                # do something with those instead.
                ax.autoscale_view()

            # Haven't implemented legends yet
            # plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

    def _get_fig_axmap(self):
        rows, cols = self.faceter.shape()

        fig, axs = plt.subplots(nrows=rows, ncols=cols)

        if rows == cols == 1:
            # subplots doesn't return a list
            axs = [axs]

        if rows > 1 and cols > 1:
            # subplots returns a nested list
            axs = [a for b in axs for a in b]

        ax_map = dict(zip(self.faceter.facet_names, axs))
        for name, ax in ax_map.items():
            ax.set_title(name, fontdict={'fontsize': 10})

        return fig, ax_map

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
        elif isinstance(other, faceter.Faceter):
            copy.faceter = other

        return copy
