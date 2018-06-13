################################################################################
# Filename: image_resize.py
#
# Description: Provides method to easily resize images to save on bandwidth.
#
# Author: Hans Goldman
# Create Date: 2/13/2015
# Last Modified by: 2/13/2015
# Last Modified Date: 2/13/2015
################################################################################

from PIL import Image     # For image processing
import os                 # For directory creation


def resize_image(source_path, destination_path, target_size):
    """
    Used to resize images to a target size/dimension.
    :param source_path: The full path to the image to be resized
    :param destination_path: The full path to where you would like the new resized image created
    :param target_size: The desired size of the largest dimension (width or height)
    :return: None
    """
    target_width    = 0
    target_height   = 0

    original_image = Image.open(source_path)
    original_image.load()

    # Get dimensions
    width, height = original_image.size

    # Scale the image, if needed
    if (width > height) and (width > target_size):
        aspect_ratio  = height / float(width)
        target_height = int(target_size * aspect_ratio)
        target_width  = target_size

    # Check if the image image is taller than it is wide
    elif (height > width) and (height > target_size):
        aspect_ratio  = width / float(height)
        target_width  = int(target_size * aspect_ratio)
        target_height = target_size

    # The image is square
    elif (height == width) and (height > target_size):
        target_width  = target_size
        target_height = target_size

    # Check for empty image. Don't save an empty image.
    if (target_width != 0) and (target_height != 0):
        # Save a square thumbnail of the image
        scaled_image = original_image.resize((target_width, target_height), Image.ANTIALIAS)

        # Create directory path, if it does not already exist
        if not os.path.exists(os.path.dirname(destination_path)):
            os.makedirs(os.path.dirname(destination_path))

        scaled_image.save(destination_path, quality=80)
