from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import numpy as np
import matplotlib.ticker as ticker

class Transform(object):
    def transform(self, series):
        return series

    def invert(self, series):
        return series

    def major_breaks(self, limits):
        locator = ticker.AutoLocator()
        return locator.tick_values(*self.invert(np.asarray(limits)))

class TransformIdentity(Transform):
    pass
identity = TransformIdentity

class TransformSqrt(TransformIdentity):
    def transform(self, series):
        return np.sqrt(series)

    def invert(self, series):
        return series ** 2

sqrt = TransformSqrt
