from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

from . import aes

class Layer(object):
    def __init__(self, geom, stat):
        if isinstance(geom, basestring):
            geom = Layer.find_geom(geom)()
        if isinstance(stat, basestring):
            stat = Layer.find_stat(stat)()

        self.geom = geom
        self.stat = stat
        self.aes = aes.Aes()

    def draw(self, ax, data):
        self.geom.draw(ax, data)

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
    def __eq__(self, other):
        return type(self) is type(other) and other.__dict__ == self.__dict__
    def __ne__(self, other):
        return not self == other
