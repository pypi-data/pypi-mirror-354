"""
utils
=====

This module provides internal utility functions for handling images and configuration
files in the DELG feature extraction pipeline. It includes functions for
loading and resizing images (to match the model’s expected input sizes),
resolving configuration file paths, and parsing configuration files
(serialized in the .pbtxt format using Google’s protobuf).

These functions are intended for internal use only and are not part of the package’s
public API. They are used by other modules to support the DELG feature extraction
workflow.

Notes:
------
Author: Duje Giljanović (giljanovic.duje@gmail.com)
License: Apache License 2.0 (same as the official DELG implementation)

This package uses the DELG model originally developed by Google Research and published
in the paper "Unifying Deep Local and Global Features for Image Search" authored by Bingyi Cao,
Andre Araujo, and Jack Sim.

If you use this Python package in your research or any other publication, please cite both this
package and the original DELG paper as follows:

@software{delg,
    title = {delg: A Python Package for Dockerized DELG Implementation},
    author = {Duje Giljanović},
    year = {2025},
    url = {https://github.com/gilja/delg-feature-extractor}
}

@article{cao2020delg,
    title = {Unifying Deep Local and Global Features for Image Search},
    author = {Bingyi Cao and Andre Araujo and Jack Sim},
    journal = {arXiv preprint arXiv:2001.05027},
    year = {2020}
}
"""

import os
import numpy as np
from PIL import Image
from PIL import ImageFile
import tensorflow as tf

from google.protobuf import text_format
from google.protobuf.message import Message
from typing import cast
from . import delf_config_pb2

# To avoid PIL crashing for truncated (corrupted) images.
ImageFile.LOAD_TRUNCATED_IMAGES = True


def _read_image_to_uint8(path: str) -> np.ndarray:
    """
    Loads an image from disk and converts it to an RGB NumPy array of dtype uint8.

    Opens an image file using the Pillow library, converts it to RGB color mode,
    and returns the image as a NumPy array suitable for use with DELG feature
    extractors.

    Args:
      path: String path to the image file.

    Returns:
      numpy.ndarray: 3D array of shape (H, W, 3) representing the RGB image.
    """

    image = Image.open(path).convert("RGB")
    return np.array(image)


def _default_config_path(feature_type: str) -> str:
    """
    Resolves the default config file path for DELG feature extraction.

    Constructs the absolute path to the appropriate `.pbtxt` configuration file
    (either global or local) located in the same directory as this module.

    Args:
      feature_type: String indicating the type of feature to extract. Must be either 'global' or 'local'.

    Returns:
      str: Full path to the corresponding DELG configuration `.pbtxt` file.

    Raises:
      ValueError: If feature_type is not 'global' or 'local'.
    """

    if feature_type not in {"global", "local"}:
        raise ValueError("feature_type must be 'global' or 'local'.")
    filename = (
        "model_configs/config_global.pbtxt"
        if feature_type == "global"
        else "model_configs/config_local.pbtxt"
    )
    return os.path.join(os.path.dirname(__file__), filename)


def _load_config(config_path: str):
    """
    Loads and parses a DELG configuration file in `.pbtxt` format.

    Reads a text-based DELG configuration file, parses it into a DelfConfig
    protobuf object, and returns the configuration for use in extractor setup.

    Args:
      config_path: String path to the `.pbtxt` file containing the DELG config.

    Returns:
      delf_config_pb2.DelfConfig: Parsed configuration object.

    Raises:
      FileNotFoundError: If the specified config file does not exist.
    """

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    config = delf_config_pb2.DelfConfig()
    with open(config_path, "r") as f:
        text_format.Merge(f.read(), cast(Message, config))
    return config


def _RgbLoader(path):
    """
    Loads an image using PIL and converts it to RGB format.

    Opens an image file using TensorFlow's file I/O and PIL, then ensures the
    image is in RGB color mode.

    Args:
      path: String path to the image to be loaded.

    Returns:
      PIL.Image.Image: The loaded image in RGB format.
    """

    with tf.io.gfile.GFile(path, "rb") as f:
        img = Image.open(f)
        return img.convert("RGB")


def _ResizeImage(image, config, resize_factor=1.0):
    """
    Resizes an image according to the DELG configuration.

    Applies resizing rules from the DELG configuration, including maximum and minimum
    image sizes, optional resize factor, and optional square resizing. Returns the resized
    image along with scale factors for height and width.

    Args:
      image: Uint8 NumPy array of shape (height, width, 3) representing the RGB image.
      config: DelfConfig object containing the model configuration.
      resize_factor: Optional float scale factor applied to max/min image sizes.

    Returns:
      resized_image: Uint8 NumPy array containing the resized image.
      scale_factors: 1D float NumPy array containing height and width scale factors.

    Raises:
      ValueError: If image has incorrect number of dimensions or channels, or if
        resize_factor is negative.
    """

    if resize_factor < 0.0:
        raise ValueError(f"negative resize_factor is not allowed: {resize_factor}")
    if image.ndim != 3:
        raise ValueError(f"image has incorrect number of dimensions: {image.ndims}")
    height, width, channels = image.shape

    # Take into account resize factor.
    max_image_size = resize_factor * config.max_image_size
    min_image_size = resize_factor * config.min_image_size

    if channels != 3:
        raise ValueError(f"image has incorrect number of channels: {channels}")

    largest_side = max(width, height)

    if max_image_size >= 0 and largest_side > max_image_size:
        scale_factor = max_image_size / largest_side
    elif min_image_size >= 0 and largest_side < min_image_size:
        scale_factor = min_image_size / largest_side
    elif config.use_square_images and (height != width):
        scale_factor = 1.0
    else:
        # No resizing needed, early return.
        return image, np.ones(2, dtype=float)

    # Note that new_shape is in (width, height) format (PIL convention), while
    # scale_factors are in (height, width) convention (NumPy convention).
    if config.use_square_images:
        new_shape = (
            int(round(largest_side * scale_factor)),
            int(round(largest_side * scale_factor)),
        )
    else:
        new_shape = (
            int(round(width * scale_factor)),
            int(round(height * scale_factor)),
        )

    scale_factors = np.array([new_shape[1] / height, new_shape[0] / width], dtype=float)

    pil_image = Image.fromarray(image)
    resized_image = np.array(pil_image.resize(new_shape, resample=Image.BILINEAR))

    return resized_image, scale_factors
