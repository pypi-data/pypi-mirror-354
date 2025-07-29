"""
feature_extractor
=================

This module defines internal helper functions for post-processing features
in the DELG pipeline, including keypoint center calculation and descriptor
post-processing. These functions are used by the DELG feature extractor to
prepare features for downstream tasks such as feature comparison and matching.

Note:
- While some legacy code exists for PCA and whitening transformations, these
  are not actually used in the DELG implementation. They remain in the code
  for potential future extensions but are not active in the current workflow.

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

import tensorflow as tf


def _CalculateKeypointCenters(boxes):
    """
    Computes the centers of feature boxes.

    Calculates the center points of receptive field (RF) boxes based on their
    corner coordinates, returning a [N, 2] tensor of centers.

    Args:
      boxes: [N, 4] float tensor representing box coordinates.

    Returns:
      [N, 2] float tensor containing center points of the boxes.
    """

    return tf.divide(
        tf.add(tf.gather(boxes, [0, 1], axis=1), tf.gather(boxes, [2, 3], axis=1)), 2.0
    )


def _ApplyPcaAndWhitening(
    data, pca_matrix, pca_mean, output_dim, use_whitening=False, pca_variances=None
):
    """
    Applies PCA and optional whitening to feature data.

    Performs dimensionality reduction and optional whitening transformation
    on the input data using the given PCA parameters.

    Args:
      data: [N, dim] float tensor containing the data to transform.
      pca_matrix: [dim, dim] float tensor PCA projection matrix (row-major).
      pca_mean: [dim] float tensor representing the mean to subtract before projection.
      output_dim: Integer specifying the number of dimensions in the output data.
      use_whitening: Boolean indicating whether to apply whitening.
      pca_variances: [dim] float tensor containing PCA variances, required if
        use_whitening is True.

    Returns:
      [N, output_dim] float tensor containing the transformed data.
    """

    output = tf.matmul(
        tf.subtract(data, pca_mean),
        tf.slice(pca_matrix, [0, 0], [output_dim, -1]),
        transpose_b=True,
        name="pca_matmul",
    )

    # Apply whitening if desired.
    if use_whitening:
        output = tf.divide(
            output,
            tf.sqrt(tf.slice(pca_variances, [0], [output_dim])),
            name="whitening",
        )

    return output


def _PostProcessDescriptors(descriptors, use_pca, pca_parameters=None):
    """Post-process descriptors.

    Args:
      descriptors: [N, input_dim] float tensor.
      use_pca: Whether to use PCA.
      pca_parameters: Only used if `use_pca` is True. Dict containing PCA
        parameter tensors, with keys 'mean', 'matrix', 'dim', 'use_whitening',
        'variances'.

    Returns:
      final_descriptors: [N, output_dim] float tensor with descriptors after
        normalization and (possibly) PCA/whitening.
    """
    # L2-normalize, and if desired apply PCA (followed by L2-normalization).
    final_descriptors = tf.nn.l2_normalize(descriptors, axis=1, name="l2_normalization")

    if use_pca:
        # Apply PCA, and whitening if desired.
        final_descriptors = _ApplyPcaAndWhitening(
            final_descriptors,
            pca_parameters["matrix"],
            pca_parameters["mean"],
            pca_parameters["dim"],
            pca_parameters["use_whitening"],
            pca_parameters["variances"],
        )

        # Re-normalize.
        final_descriptors = tf.nn.l2_normalize(
            final_descriptors, axis=1, name="pca_l2_normalization"
        )

    return final_descriptors


def _DelfFeaturePostProcessing(boxes, descriptors, use_pca, pca_parameters=None):
    """
    Post-processes feature descriptors using normalization and optional PCA.

    Applies L2-normalization and, if enabled, PCA and whitening to the input
    descriptors, returning processed feature vectors ready for downstream tasks.

    Args:
      descriptors: [N, input_dim] float tensor containing raw descriptors.
      use_pca: Boolean indicating whether to apply PCA.
      pca_parameters: Optional dictionary of PCA parameter tensors (required
        if use_pca is True), with keys 'mean', 'matrix', 'dim', 'use_whitening',
        and 'variances'.

    Returns:
      [N, output_dim] float tensor containing post-processed descriptors.
    """

    # Get center of descriptor boxes, corresponding to feature locations.
    locations = _CalculateKeypointCenters(boxes)
    final_descriptors = _PostProcessDescriptors(descriptors, use_pca, pca_parameters)

    return locations, final_descriptors
