################################################################################
# Filename: image_thumbnails.py
#
# Description: Provides method to easily allow the creation of thumbnail images
#   from existing images.
#
# Author: Hans Goldman
# Create Date: 2/9/2015
# Last Modified by: Hans Goldman
# Last Modified Date: 2/9/2015
################################################################################

from PIL import Image     # For image processing
import os                 # For directory creation


def create_thumbnail(source_path, destination_path, target_size):
    """
    Creates square thumbnail images.
    :param source_path: The path to the source image file to be cropped
    :param destination_path: The full path to the location that the cropped image will be saved
    :param target_size: The number of pixels of one side of the square image (all sides will be equal)
    :return: None
    """
    thumbnail_size = (target_size, target_size)

    original_image = Image.open(source_path)
    original_image.load()

    # Get dimensions
    width, height = original_image.size

    # Crop the image to make it a square, if needed
    if width > height:
        excess = width - height
        excess = int(excess / 2)

        left   = excess
        top    = 0
        right  = width - excess
        bottom = height

        # Crop the image
        cropped_image = original_image.crop((left, top, right, bottom))

    elif height > width:
        excess = height - width
        excess = int(excess / 2)

        left   = 0
        top    = excess
        right  = width
        bottom = height - excess

        # Crop the image
        cropped_image = original_image.crop((left, top, right, bottom))

    # Create directory path, if it does not already exist
    if not os.path.exists(os.path.dirname(destination_path)):
        os.makedirs(os.path.dirname(destination_path))

    # Save a square thumbnail of the image
    cropped_image.thumbnail(thumbnail_size, Image.ANTIALIAS)
    cropped_image.save(destination_path, quality=80)
