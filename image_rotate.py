################################################################################
# Filename: image_rotate.py
#
# Description: Provides a method to rotate images in the clockwise direction.
#
# Author: Hans Goldman
# Create Date: 2/16/2016
# Last Modified by: Hans Goldman
# Last Modified Date: 2/16/2016
################################################################################

import os
from PIL import Image


def roate_image_by_degrees(source_path, degrees):
    """
    Rotates an image by the specified degrees in the clockwise direction.
    :param source_path: Full path to the image to be rotated
    :param degrees: Integer amount to rotate the image by (clockwise)
    :return: None
    """
    # Only continue if any rotation is needed
    if degrees != 0:
        original_image = Image.open(source_path)
        original_image.load()

        # Input is measured clockwise, rotate method is counter clockwise, so we need to convert
        rotate_amount = int(degrees) * -1

        rotated_image = original_image.rotate(rotate_amount, resample=Image.BICUBIC, expand=True)
        rotated_image.save(source_path, quality=80)
