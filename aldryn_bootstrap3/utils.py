# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import collections
from .conf import settings
from . import constants


class ColumnContext(list):
    """
    this is a stacking list of column definitions in the form of
    with the device size as a key and the column size as value:
    [
        {'xs': 16, 'lg': 6},
        {'xs': 12, 'lg': 12},
    ]
    """
    def __init__(self, *args, **kwargs):
        self.grid_size = kwargs.pop(
            'grid_size', settings.ALDRYN_BOOTSTRAP3_GRID_SIZE)
        self.device_sizes = kwargs.pop(
            'device_sizes', constants.DEVICE_SIZES)
        super(ColumnContext, self).__init__(*args, **kwargs)

    def add_from_classes(self, classes):
        result = {}
        for device in self.device_sizes:
            for size in range(1, self.grid_size):
                if 'col-{}-{}'.format(device, size) in classes:
                    result[device] = size
        self.append(result)

    def combined(self):
        """
        calculation of the "actual" size of a column taking
        parent columns into account (ignoring gutters).
        For the example above, assuming a grid width of 24, it would
        result in xs=24*(16/24)*(12/24) and lg=24*(6/24)*(12/24),
        so {'xs': 8, 'lg': 3}.

        This also takes into account, that column calculation uses "fallbacks".
        So: On a "md" device, if there is no "col-md-X" defined it will fall
        back to the value of "col-sm-X" and down to "col-xs-X" if that also
        does not exist.
        """
        grid_size = self.grid_size
        result = {
            size: float(grid_size)
            for size in constants.DEVICE_SIZES
        }
        for column in self:
            for key, value in column.items():
                result[key] *= (float(value) / float(grid_size))
        result = {key: int(value) in result.items()}
        return result


def img_srcset_and_sizes(
        column_sizes, aspect_ratio, thumbnail_opts, grid_size=None):
    """
    :param column_sizes: expected column size for display (already calculated
     based on col nesting)
    :param aspect_ratios: dictionary of aspect ratios as tuples by device
    :param thumbnail_opts: thumbnail options for all
    :return:
    """
    # TODO: pass in original image width, so that we can NOT generate any
    #       versions of the image that would mean an upscale.
    # TODO: include debug info
    # TODO: handle fluid containers
    if grid_size is None:
        grid_size = settings.ALDRYN_BOOTSTRAP3_GRID_SIZE
    if aspect_ratio:
        aspect_width, aspect_height = tuple([int(i) for i in aspect_ratio.split('x')])
    else:
        aspect_width, aspect_height = None, None
    # generate srcset:
    #   a list of thumbnails in different resolutions for the browser to choose from.
    #   all it really provides is a hint of the image width for the browser, without
    #   it having to download the image to find out what width it has.
    #   currently we create one size per bootstrap device size... this could be
    #   extended to contain any sizes though.
    srcset = []
    for device in constants.DEVICES:
        # if aspect_ratios.get(device, None):
        #     aspect_width, aspect_height = tuple([int(i) for i in aspect_ratios[device].split('x')])
        # else:
        #     aspect_width, aspect_height = None, None
        width_in_grid_units = column_sizes.get(device, grid_size)
        full_width_in_px = constants.DEVICES[device]['width']
        width_in_px = int(
            float(full_width_in_px) * (
                float(width_in_grid_units) / float(grid_size)
            )
        )
        if aspect_width is not None and aspect_height is not None:
            height_in_px = int(float(width_in_px)*float(aspect_height)/float(aspect_width))
            crop = True
        else:
            height_in_px = 0
            crop = False
        thumbnail_options = {}
        thumbnail_options.update(thumbnail_opts)
        thumbnail_options.update({
            'size': (width_in_px, height_in_px),
            'subject_location': thumbnail_opts.get('subject_location', None),
            'upscale': True,
            'crop': crop,
        })
        data = {
            'width': "{}w".format(width_in_px),
            'thumbnail_options': thumbnail_options,
            'aspect_ratio': (aspect_width, aspect_height),
        }
        srcset.append(data)
    # generate size:
    #   generate a list of viewport widths and the expected percentage of that
    #   width that this particular image will fill.
    sizes = collections.OrderedDict()
    devices = constants.DEVICE_SIZES
    for device, device_data in constants.DEVICES.items():
        # TODO: these rules should change for fluid containers
        # a specific image size (e.g xs) should be used as long as the viewport
        # is smaller than the next larger one.
        grid_width_px = device_data['width']
        # naive percentage of viewport we expect the image to fill
        # (the viewport will be wider in practice, but that does not matter
        # since the browser will pick the image with the next higher
        # resolution)
        expected_column_size = column_sizes.get(device, grid_size)
        expected_column_size_percentage_of_viewport = float(grid_width_px)





