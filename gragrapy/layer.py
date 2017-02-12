from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

from .aes import Aes

class Layer(object):
    def __init__(self, geom, stat, aes=None, data=None):
        if isinstance(geom, basestring):
            geom = Layer.find_geom(geom)()
        if isinstance(stat, basestring):
            stat = Layer.find_stat(stat)()

        self.aes = aes or Aes()
        self.data = data
        self.geom = geom
        self.stat = stat

    def draw(self, ax, data):
        self.geom.draw(ax, data)

    def wrap_aes(self, aes):
        """Wrap the `aes` in this layer's default and provided aesthetics."""
        return Aes.union(self.geom.default_aes, aes, self.aes)

    def map_data(self, aes, default_data=None):
        """Map the Layer's dataset using the aes.

        `aes` is first wrapped in this Layer's default and provided aes.

        If this Layer doesn't have its own data, map the the `default_data`
        instead."""
        aes = self.wrap_aes(aes)

        if self.data is not None:
            data = self.data
        else:
            data = default_data

        if data is None:
            raise ValueError('Layer.map_data: data must be provided either ' \
                             'in the layer or as an argument.')

        return aes.map_df(data)

    @staticmethod
    def find_geom(name):
        from . import geom
        return geom.__dict__[name]

    @staticmethod
    def find_stat(name):
        from . import stat
        return stat.__dict__[name]

    def __eq__(self, other):
        return type(self) is type(other) and other.__dict__ == self.__dict__
    def __ne__(self, other):
        return not self == other

class LayerComponent(object):
    def __init__(self, aes=None, data=None, **kwargs):
        self.aes = aes
        self.data = data
        self.params = kwargs

    def __eq__(self, other):
        return type(self) is type(other) and other.__dict__ == self.__dict__
    def __ne__(self, other):
        return not self == other
