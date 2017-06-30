from __future__ import (absolute_import, print_function,
                        unicode_literals, division)

import plotnine as p9

class alpha(object):
    continuous = p9.scale_alpha_continuous
    discrete = p9.scale_alpha_discrete
    identity = p9.scale_alpha_identity
    manual = p9.scale_alpha_manual

class color(object):
    brewer = p9.scale_color_brewer
    cmap = p9.scale_color_cmap
    continuous = p9.scale_color_continuous
    desaturate = p9.scale_color_desaturate
    discrete = p9.scale_color_discrete
    distiller = p9.scale_color_distiller
    gradient = p9.scale_color_gradient
    gradient2 = p9.scale_color_gradient2
    gradientn = p9.scale_color_gradientn
    gray = p9.scale_color_gray
    grey = p9.scale_color_grey
    hue = p9.scale_color_hue
    identity = p9.scale_color_identity
    manual = p9.scale_color_manual

class fill(object):
    brewer = p9.scale_fill_brewer
    cmap = p9.scale_fill_cmap
    continuous = p9.scale_fill_continuous
    desaturate = p9.scale_fill_desaturate
    discrete = p9.scale_fill_discrete
    distiller = p9.scale_fill_distiller
    gradient = p9.scale_fill_gradient
    gradient2 = p9.scale_fill_gradient2
    gradientn = p9.scale_fill_gradientn
    gray = p9.scale_fill_gray
    grey = p9.scale_fill_grey
    hue = p9.scale_fill_hue
    identity = p9.scale_fill_identity
    manual = p9.scale_fill_manual

class linetype(object):
    continuous = p9.scale_linetype_continuous
    discrete = p9.scale_linetype_discrete
    identity = p9.scale_linetype_identity
    manual = p9.scale_linetype_manual

class shape(object):
    continuous = p9.scale_shape_continuous
    discrete = p9.scale_shape_discrete
    identity = p9.scale_shape_identity
    manual = p9.scale_shape_manual

class size(object):
    area = p9.scale_size_area
    continuous = p9.scale_size_continuous
    discrete = p9.scale_size_discrete
    identity = p9.scale_size_identity
    manual = p9.scale_size_manual
    radius = p9.scale_size_radius

class stroke(object):
    continuous = p9.scale_stroke_continuous
    discrete = p9.scale_stroke_discrete

class x(object):
    continuous = p9.scale_x_continuous
    date = p9.scale_x_date
    datetime = p9.scale_x_datetime
    discrete = p9.scale_x_discrete
    log10 = p9.scale_x_log10
    reverse = p9.scale_x_reverse
    sqrt = p9.scale_x_sqrt
    timedelta = p9.scale_x_timedelta

class y(object):
    continuous = p9.scale_y_continuous
    date = p9.scale_y_date
    datetime = p9.scale_y_datetime
    discrete = p9.scale_y_discrete
    log10 = p9.scale_y_log10
    reverse = p9.scale_y_reverse
    sqrt = p9.scale_y_sqrt
    timedelta = p9.scale_y_timedelta

def _make_scale(*args, **kwargs):
    aes = args[0]
    args = args[1:]

    if isinstance(aes, p9.scales.scale.scale):
        # returning an existing instance, can't pass it params
        assert not args and not kwargs
        return aes

    if isinstance(aes, type) and issubclass(name, p9.scales.scale.scale):
        cls = name
    else:
        name = args[0]
        args = args[1:]
        cls = getattr(globals()[aes], name)

    return cls(*args, **kwargs)
