"""
datum_io
========

This module provides utility functions for working with DatumProto, a protocol buffer
used by TensorFlow and DELG to serialize tensors of arbitrary shape. It allows reading
data from DatumProto files, parsing serialized DatumProto strings, and converting these
data into NumPy arrays for downstream processing in the DELG feature extraction pipeline.

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

# pyright: reportAttributeAccessIssue=false
# pylint: disable=no-member

import numpy as np
import tensorflow as tf


def DatumToArray(datum):
    """
    Converts a DatumProto object to a NumPy array.

    Converts the contents of a DatumProto object—either a float_list or
    uint32_list—into a NumPy array with the shape specified in the DatumProto.

    Args:
      datum: DatumProto object containing either 'float_list' or 'uint32_list'
        and a 'shape' field.

    Returns:
      numpy.ndarray: A NumPy array with the shape specified in datum.shape.dim.

    Raises:
      ValueError: If the DatumProto does not contain a float_list or uint32_list.
    """

    if datum.HasField("float_list"):
        return (
            np.array(datum.float_list.value).astype("float32").reshape(datum.shape.dim)
        )
    elif datum.HasField("uint32_list"):
        return (
            np.array(datum.uint32_list.value).astype("uint32").reshape(datum.shape.dim)
        )
    else:
        raise ValueError("Input DatumProto does not have float_list or uint32_list")


def ParseFromString(string):
    """
    Converts a serialized DatumProto string to a NumPy array.

    Parses a DatumProto string and converts it to a NumPy array using the DatumToArray function.

    Args:
      string: Serialized DatumProto string.

    Returns:
      numpy.ndarray: A NumPy array representation of the data.
    """

    datum = datum_pb2.DatumProto()
    datum.ParseFromString(string)

    return DatumToArray(datum)


def ReadFromFile(file_path):
    """
    Reads data from a DatumProto-formatted file and returns a NumPy array.

    Opens a file containing a serialized DatumProto object, parses it, and converts
    it to a NumPy array using ParseFromString.

    Args:
      file_path: Path to the file containing the serialized DatumProto object.

    Returns:
      numpy.ndarray: A NumPy array representation of the data.
    """

    with tf.io.gfile.GFile(file_path, "rb") as f:
        return ParseFromString(f.read())
