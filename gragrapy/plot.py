from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import os

import pandas as pd
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

        self.title = None

    def show(self):
        self.make()
        if not os.getenv('GRAGRAPY_NOSHOW'):
            plt.show()

    def save(self, filename):
        self.make()
        plt.gcf().savefig(filename)

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
        plt.close()
        with mpl.rc_context():
            self.apply_theme()

            scales = { k: v.copy() for k, v in self.scales.items() }
            scale_names = {}

            all_datasets = [ layer.default_data(self.data)
                             for layer in self.layers ]
            self.faceter.train(all_datasets)
            fig, ax_map = self._get_fig_axmap()

            if self.title is not None:
                fig.suptitle(self.title)

            datasets = [ self.faceter.facet(d) for d in all_datasets ]

            def _map1(dataset, layer):
                aes = layer.wrap_aes(self.aes)
                scale_names.update(aes.scale_names())

                mapped1 = aes.map_data(dataset)
                mapped1['facet'] = dataset['facet']

                scales.update(scale.guess_default_scales(mapped1, scales))
                return mapped1

            datasets = map(_map1, datasets, self.layers)

            def _trans(mapped1):
                return scale.Scale.transform_scales(mapped1, scales)

            datasets = map(_trans, datasets)

            # python3 map objects can only be iterated once, so list()
            datasets = list(datasets)

            # color scales map to np.ndarray values, which causes problems when
            # the stat calls nunique(). That's probably fixable, but right now
            # stats only look at position and unscaled aesthetics anyway.
            #   So currently, we train and map position scales before applying
            # the stat, and we train and map all other scales afterwards. If the
            # stat introduces a position scale (e.g. stat.bin introduces y), we
            # train and map that afterwards too.

            position_scales = { k: v for k,v in scales.items()
                                if 'x' in v.aes or 'y' in v.aes }
            scale.Scale.train_scale_maps(datasets, position_scales)

            # python3 map objects are also lazy, so list() here too
            list(map(lambda df: self._add_group(df, scales), datasets))

            def _map_scales(scales):
                return lambda df: scale.Scale.map_scales(df, scales)

            datasets = map(_map_scales(position_scales), datasets)

            def _stat(scaled1, layer):
                groups = scaled1.groupby('facet')
                statted_groups = [ (name, layer.stat.transform(group, scales))
                                   for name, group in groups ]
                statted_groups = [ group.assign(facet=name)
                                   for name, group in statted_groups ]
                statted = pd.concat(statted_groups, ignore_index=True)

                aes = layer.wrap_aes(self.aes)
                mapped2 = aes.map_stat(statted)
                stat_cols = set(aes.stat_mappings)

                # We need to re-transform some columns. Consider geom.histogram
                # plus scale.y.sqrt: the y column wasn't in the original data,
                # so it hasn't been transformed, so we need to do so now.
                #   ggplot2's approach is to re-transform anything that comes
                # from a computed aes. That doesn't always work (consider:
                # aes(stat_ymin='y'), stat.smooth, scale.x.sqrt; ymin will get
                # sqrted twice), but it's a good start.
                #   In future, maybe let stats choose whether re-transformation
                # happens. I'm not sure if that has other edge cases. (It's what
                # ggplot2 looks like it's set up to do, but no scales disable
                # re-transformation.)

                scales.update(scale.guess_default_scales(mapped2, scales))
                scaled2 = scale.Scale.transform_scales(mapped2, scales,
                                                       columns=stat_cols)
                return scaled2

            datasets = map(_stat, datasets, self.layers)
            datasets = list(datasets)

            untrained_scales = { k:v for k,v in scales.items()
                                 if k not in position_scales }
            scale.Scale.train_scale_maps(datasets, untrained_scales)

            datasets = map(_map_scales(untrained_scales), datasets)
            datasets = list(datasets)

            scale.Scale.train_scale_guides(datasets, scales)

            def _draw(scaled3, layer):
                groups = scaled3.groupby('facet')
                for name, group in groups:
                    layer.draw(ax_map[name], group)

            list(map(_draw, datasets, self.layers))

            x_scale = next(s for s in scales.values() if 'x' in s.aes)
            y_scale = next(s for s in scales.values() if 'y' in s.aes)
            for ax in ax_map.values():
                x_scale.apply_ax(ax)
                y_scale.apply_ax(ax)

            # Names from the plot aes should take priority over others.
            scale_names.update(self.aes.scale_names())

            if 'color' in scales:
                plt.subplots_adjust(right=0.8)
                legend = scales['color'].get_legend()
                # This needs to consider aeses other than self.aes, and also
                # stat_mappings.
                scale_name = scale_names['color']
                blank = mpl.patches.Patch(fill=False, label=scale_name)
                plt.legend(handles=[blank] + legend,
                           loc='upper left',
                           bbox_to_anchor=(1, 1))

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

    def _add_group(self, data, scales):
        if 'group' in data:
            return

        disc_scales = [ s.aes for s in scales.values()
                        if s.level == scale.Level.DISCRETE]
        if disc_scales:
            cols = set.union(*disc_scales).intersection(set(data.columns))
        else:
            cols = None

        if not cols:
            data['group'] = '' # Can't use None because we later groupby() this
            return

        groups = data.apply(lambda row: repr(tuple(row[c] for c in cols)),
                            axis=1)
        data['group'] = groups

    def _copy(self):
        copy = Plot(self.data, self.aes)
        copy.layers = list(self.layers)
        copy.scales = dict(self.scales)
        copy.faceter = self.faceter
        copy.title = self.title

        return copy

    def __iadd__(self, other):
        if isinstance(other, list):
            for x in other:
                self += x
        elif isinstance(other, type):
            self += other()
        elif isinstance(other, PlotObj):
            other.apply(self)
        elif isinstance(other, layer.LayerComponent):
            self.layers.append(other.make_layer())
        elif isinstance(other, layer.Layer):
            self.layers.append(other)
        elif isinstance(other, scale.Scale):
            self.scales[other.__class__.__name__] = other
        elif isinstance(other, faceter.Faceter):
            self.faceter = other

        return self

    def __add__(self, other):
        copy = self._copy()
        copy += other
        return copy
plot = Plot

class PlotObj(object):
    def apply(self, plot):
        raise NotImplementedError()

class PlotTitle(PlotObj):
    def __init__(self, title):
        self.title = title

    def apply(self, plot):
        plot.title = self.title
title = PlotTitle
