################################################################################
# Filename: image_crop.py
#
# Description: Provides method(s) to allow the creation of images from existing
#   images that are cropped to meet size restrictions of the input parameters.
#
# Author: Hans Goldman
# Create Date: 4/23/2015
# Last Modified by: Hans Goldman
# Last Modified Date: 4/23/2015
################################################################################

from PIL import Image     # For image processing
import os                 # For directory creation


def create_cropped_image(source_path, destination_path, target_width, target_height):
    """
    Creates cropped images that match the dimensions given.
    :param source_path: The path to the source image file to be cropped
    :param destination_path: The full path to the location that the cropped image will be saved
    :param target_width: The new width for the image
    :param target_height: The new height for the image
    :return: None
    """
    original_image = Image.open(source_path)
    original_image.load()

    # Get dimensions
    width, height = original_image.size
    aspect_ratio  = width / float(height)
    target_ratio  = target_width / float(target_height)

    # Track how many pixels to remove from each side
    left_count   = 0
    right_count  = 0
    top_count    = 0
    bottom_count = 0

    # Is the image too wide?
    if aspect_ratio > target_ratio:
        count       = 0
        temp_width  = width

        # Alternate subtracting one pixel from right & left until target ratio is met
        while aspect_ratio > target_ratio:
            count += 1

            if count % 2 == 1:
                left_count += 1
            else:
                right_count += 1

            temp_width  -= 1
            aspect_ratio = temp_width / float(height)

    # Is the image too tall?
    elif aspect_ratio < target_ratio:
        count       = 0
        temp_height = height

        # Alternate subtracting one pixel from top & bottom until target ratio is met
        while aspect_ratio < target_ratio:
            count += 1

            if count % 2 == 1:
                top_count += 1
            else:
                bottom_count += 1

            temp_height -= 1
            aspect_ratio = width / float(temp_height)

    # Crop the image keeping the correct aspect ratio
    cropped_image = original_image.crop((left_count, top_count, width - right_count, height - bottom_count))

    # Scale the image, if needed
    if width > target_width:
        # Check for empty image. Don't save an empty image.
        if (target_width != 0) and (target_height != 0):
            # Save a square thumbnail of the image
            scaled_image = cropped_image.resize((target_width, target_height), Image.ANTIALIAS)

            # Create directory path, if it does not already exist
            if not os.path.exists(os.path.dirname(destination_path)):
                os.makedirs(os.path.dirname(destination_path))

            scaled_image.save(destination_path, quality=80)
