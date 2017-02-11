from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import numpy as np
import pandas as pd

from .layer import Layer, LayerComponent

class Stat(LayerComponent):
    default_geom = 'point'

    def __init__(self, **kwargs):
        self.params = kwargs

    def transform(self, df):
        pass

    def make_layer(self):
        return Layer(geom=self.params.get('geom', self.default_geom), stat=self)

class StatIdentity(Stat):
    def transform(self, df):
        return df
identity = StatIdentity

class StatSmooth(Stat):
    default_geom = 'smooth'

    def transform(self, df):
        sorted = df.sort_values('x')
        y = sorted['y'].rolling(5, center=True).mean()
        std = sorted['y'].rolling(5, center=True).std()
        return pd.DataFrame({'x': sorted['x'], 'y': y,
                             'ymin': y - std, 'ymax': y + std})

smooth = StatSmooth
