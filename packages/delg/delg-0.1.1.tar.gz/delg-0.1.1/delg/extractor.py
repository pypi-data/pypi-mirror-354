"""
extractor
=========

This module defines the feature extractor for the DELG model, including support for
both global and local feature extraction. It provides a single entry point
(_MakeExtractor) for constructing a DELG feature extractor function that can
process images and output their global descriptors and/or local feature sets.

The extractor uses TensorFlow’s SavedModel format to load the trained DELG model
and dynamically configures it based on the provided configuration. It supports
preprocessing of images, resizing, and post-processing of extracted features.
While some legacy support code exists for PCA and whitening, these are not
utilized in the current DELG implementation.

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

from . import datum_io
from . import feature_extractor
from . import utils

# Minimum dimensions below which features are not extracted (empty
# features are returned). This applies after any resizing is performed.
_MIN_HEIGHT = 10
_MIN_WIDTH = 10


def _MakeExtractor(config):
    """
    Creates a feature extractor function based on a DELG configuration.

    Loads a trained DELG model from the provided configuration, sets up input
    and output tensors (including PCA parameters if enabled), and returns a
    function that performs global and/or local feature extraction on input images.

    Args:
      config: DelfConfig object containing model configuration and parameters.

    Returns:
      Function: A callable that receives an image and returns extracted features
        as a dictionary.

    Raises:
      ValueError: If neither local nor global features are enabled in the configuration.
    """

    # Assert the configuration.
    if not config.use_local_features and not config.use_global_features:
        raise ValueError(
            "Invalid config: at least one of "
            "{use_local_features, use_global_features} must be True"
        )

    # Load model.
    model = tf.saved_model.load(config.model_path)

    # Input image scales to use for extraction.
    image_scales_tensor = tf.convert_to_tensor(list(config.image_scales))

    # Input (feeds) and output (fetches) end-points. These are only needed when
    # using a model that was exported using TF1.
    feeds = ["input_image:0", "input_scales:0", "input_global_scales_ind:0"]
    fetches = []

    # Custom configuration needed when local features are used.
    if config.use_local_features:
        # Extra input/output end-points/tensors.
        feeds.append("input_abs_thres:0")
        feeds.append("input_max_feature_num:0")
        fetches.append("boxes:0")
        fetches.append("features:0")
        fetches.append("scales:0")
        fetches.append("scores:0")
        score_threshold_tensor = tf.constant(config.delf_local_config.score_threshold)
        max_feature_num_tensor = tf.constant(config.delf_local_config.max_feature_num)

        # If using PCA, pre-load required parameters.
        local_pca_parameters = {}
        if config.delf_local_config.use_pca:
            local_pca_parameters["mean"] = tf.constant(
                datum_io.ReadFromFile(
                    config.delf_local_config.pca_parameters.mean_path
                ),
                dtype=tf.float32,
            )
            local_pca_parameters["matrix"] = tf.constant(
                datum_io.ReadFromFile(
                    config.delf_local_config.pca_parameters.projection_matrix_path
                ),
                dtype=tf.float32,
            )
            local_pca_parameters["dim"] = (
                config.delf_local_config.pca_parameters.pca_dim
            )
            local_pca_parameters["use_whitening"] = (
                config.delf_local_config.pca_parameters.use_whitening
            )
            if config.delf_local_config.pca_parameters.use_whitening:
                local_pca_parameters["variances"] = tf.squeeze(
                    tf.constant(
                        datum_io.ReadFromFile(
                            config.delf_local_config.pca_parameters.pca_variances_path
                        ),
                        dtype=tf.float32,
                    )
                )
            else:
                local_pca_parameters["variances"] = None

    if config.delf_global_config.image_scales_ind:
        global_scales_ind_tensor = tf.constant(
            list(config.delf_global_config.image_scales_ind)
        )
    else:
        global_scales_ind_tensor = tf.range(len(config.image_scales))

    # Custom configuration needed when global features are used.
    if config.use_global_features:
        # Extra input/output end-points/tensors.
        fetches.append("global_descriptors:0")

        # If using PCA, pre-load required parameters.
        global_pca_parameters = {}
        if config.delf_global_config.use_pca:
            global_pca_parameters["mean"] = tf.constant(
                datum_io.ReadFromFile(
                    config.delf_global_config.pca_parameters.mean_path
                ),
                dtype=tf.float32,
            )
            global_pca_parameters["matrix"] = tf.constant(
                datum_io.ReadFromFile(
                    config.delf_global_config.pca_parameters.projection_matrix_path
                ),
                dtype=tf.float32,
            )
            global_pca_parameters["dim"] = (
                config.delf_global_config.pca_parameters.pca_dim
            )
            global_pca_parameters["use_whitening"] = (
                config.delf_global_config.pca_parameters.use_whitening
            )
            if config.delf_global_config.pca_parameters.use_whitening:
                global_pca_parameters["variances"] = tf.squeeze(
                    tf.constant(
                        datum_io.ReadFromFile(
                            config.delf_global_config.pca_parameters.pca_variances_path
                        ),
                        dtype=tf.float32,
                    )
                )
            else:
                global_pca_parameters["variances"] = None

    if not hasattr(config, "is_tf2_exported") or not config.is_tf2_exported:
        model = model.prune(feeds=feeds, fetches=fetches)

    def ExtractorFn(image, resize_factor=1.0):
        """
        Extracts DELG global and/or local features from an input image.

        Preprocesses the image, performs feature extraction using the loaded
        DELG model, and returns a dictionary of extracted features including
        global descriptors and/or local features.

        Args:
          image: Uint8 NumPy array with shape (height, width, 3) representing the RGB image.
          resize_factor: Optional float scale factor for resizing the image
            before extraction.

        Returns:
          dict: A dictionary containing:
            - 'global_descriptor' (if global features enabled): NumPy array of floats.
            - 'local_features' (if local features enabled): Dictionary containing
              'locations', 'descriptors', 'scales', and 'attention' arrays.
        """

        resized_image, scale_factors = utils._ResizeImage(
            image, config, resize_factor=resize_factor
        )

        # If the image is too small, returns empty features.
        if resized_image.shape[0] < _MIN_HEIGHT or resized_image.shape[1] < _MIN_WIDTH:
            extracted_features = {"global_descriptor": np.array([])}
            if config.use_local_features:
                extracted_features.update(
                    {
                        "local_features": {
                            "locations": np.array([]),
                            "descriptors": np.array([]),
                            "scales": np.array([]),
                            "attention": np.array([]),
                        }
                    }
                )
            return extracted_features

        # Input tensors.
        image_tensor = tf.convert_to_tensor(resized_image)

        # Extracted features.
        extracted_features = {}
        output = None

        if hasattr(config, "is_tf2_exported") and config.is_tf2_exported:
            predict = model.signatures["serving_default"]
            if config.use_local_features and config.use_global_features:
                output_dict = predict(
                    input_image=image_tensor,
                    input_scales=image_scales_tensor,
                    input_max_feature_num=max_feature_num_tensor,
                    input_abs_thres=score_threshold_tensor,
                    input_global_scales_ind=global_scales_ind_tensor,
                )
                output = [
                    output_dict["boxes"],
                    output_dict["features"],
                    output_dict["scales"],
                    output_dict["scores"],
                    output_dict["global_descriptors"],
                ]
            elif config.use_local_features:
                output_dict = predict(
                    input_image=image_tensor,
                    input_scales=image_scales_tensor,
                    input_max_feature_num=max_feature_num_tensor,
                    input_abs_thres=score_threshold_tensor,
                )
                output = [
                    output_dict["boxes"],
                    output_dict["features"],
                    output_dict["scales"],
                    output_dict["scores"],
                ]
            else:
                output_dict = predict(
                    input_image=image_tensor,
                    input_scales=image_scales_tensor,
                    input_global_scales_ind=global_scales_ind_tensor,
                )
                output = [output_dict["global_descriptors"]]
        else:
            if config.use_local_features and config.use_global_features:
                output = model(
                    input_image=image_tensor,
                    input_scales=image_scales_tensor,
                    input_abs_thres=score_threshold_tensor,
                    input_max_feature_num=max_feature_num_tensor,
                    input_global_scales_ind=global_scales_ind_tensor,
                )
            elif config.use_local_features:
                output = model(
                    input_image=image_tensor,
                    input_scales=image_scales_tensor,
                    input_abs_thres=score_threshold_tensor,
                    input_max_feature_num=max_feature_num_tensor,
                    input_global_scales_ind=global_scales_ind_tensor,  # required
                )
            else:
                output = model(
                    input_image=image_tensor,
                    input_scales=image_scales_tensor,
                    input_global_scales_ind=global_scales_ind_tensor,
                )

        # Post-process extracted features: normalize, PCA (optional), pooling.
        if config.use_global_features:
            raw_global_descriptors = output[-1]
            global_descriptors_per_scale = feature_extractor._PostProcessDescriptors(
                raw_global_descriptors,
                config.delf_global_config.use_pca,
                global_pca_parameters,
            )
            unnormalized_global_descriptor = tf.reduce_sum(
                global_descriptors_per_scale, axis=0, name="sum_pooling"
            )
            global_descriptor = tf.nn.l2_normalize(
                unnormalized_global_descriptor, axis=0, name="final_l2_normalization"
            )
            extracted_features.update(
                {
                    "global_descriptor": global_descriptor.numpy(),
                }
            )

        if config.use_local_features:
            boxes = output[0]
            raw_local_descriptors = output[1]
            feature_scales = output[2]
            attention_with_extra_dim = output[3]

            attention = tf.reshape(
                attention_with_extra_dim, [tf.shape(attention_with_extra_dim)[0]]
            )
            locations, local_descriptors = feature_extractor._DelfFeaturePostProcessing(
                boxes,
                raw_local_descriptors,
                config.delf_local_config.use_pca,
                local_pca_parameters,
            )
            if not config.delf_local_config.use_resized_coordinates:
                locations /= scale_factors

            extracted_features.update(
                {
                    "local_features": {
                        "locations": locations.numpy(),
                        "descriptors": local_descriptors.numpy(),
                        "scales": feature_scales.numpy(),
                        "attention": attention.numpy(),
                    }
                }
            )

        return extracted_features

    return ExtractorFn
