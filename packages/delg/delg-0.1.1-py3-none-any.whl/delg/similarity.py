"""
similarity
==========

This module provides functions to compare global and local features between
images, including cosine similarity for global descriptors and a two-stage
approach for local features using descriptor matching (via KD-trees and Lowe’s
ratio test) followed by RANSAC geometric verification.

Public functions:
-----------------
- cosine_similarity: Computes cosine similarity between two global descriptor vectors.
- local_feature_match: Determines whether two images match based on their local features
  using descriptor matching and RANSAC geometric verification.

These functions are standalone utilities that can be used independently from the
server-based feature extraction pipeline.

For more information on the functions, refer to their docstrings.

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

from typing import List, Dict
import numpy as np

from scipy.spatial import cKDTree  # type: ignore
from skimage import measure
from skimage import transform


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Computes cosine similarity between two global descriptor vectors.

    Calculates the cosine similarity score between two input vectors, indicating
    their similarity based on their direction in space.

    Args:
      vec1: List of floats representing the first vector.
      vec2: List of floats representing the second vector.

    Returns:
      float: A similarity score between -1 and 1, where 1 means identical vectors,
        0 means orthogonal vectors, and -1 means opposite vectors.
    """

    a = np.array(vec1)
    b = np.array(vec2)
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def local_feature_match(
    f1: Dict,
    f2: Dict,
    ratio_thresh: float = 0.8,
    ransac_residual_threshold: float = 10.0,
    min_inliers: int = 10,
) -> bool:
    """
    Determines whether two images match based on their local features.

    Uses descriptor matching, Lowe's ratio test, and RANSAC geometric verification
    to evaluate whether two images can be considered a match based on their local
    features.

    Args:
      f1: Dictionary containing 'locations' and 'descriptors' for image 1.
      f2: Dictionary containing 'locations' and 'descriptors' for image 2.
      ratio_thresh: Threshold for Lowe's ratio test.
      ransac_residual_threshold: Residual threshold for RANSAC geometric verification.
      min_inliers: Minimum number of inliers required to consider images as matching.

    Returns:
      bool: True if the images match, False otherwise.
    """

    # Extract descriptors and locations from both images
    desc1 = np.array(f1["descriptors"])
    loc1 = np.array(f1["locations"])
    desc2 = np.array(f2["descriptors"])
    loc2 = np.array(f2["locations"])

    # Early exit if there are too few local features.
    if desc1.shape[0] < 3 or desc2.shape[0] < 3:
        return False

    # Match descriptors using KD-tree and Lowe's ratio test
    index_tree = cKDTree(desc2)
    distances, indices = index_tree.query(desc1, k=2, workers=-1)

    matched_query_points = []
    matched_index_points = []

    for i, row in enumerate(distances):
        if row[0] < ratio_thresh * row[1]:
            matched_query_points.append(loc1[i])
            matched_index_points.append(loc2[indices[i][0]])

    # Run RANSAC to find an affine transformation and count inliers
    matched_query_points = np.array(matched_query_points)
    matched_index_points = np.array(matched_index_points)

    # Early exit if not enough putative matches
    if matched_query_points.shape[0] < 3:
        return False

    _, inliers = measure.ransac(
        (matched_index_points, matched_query_points),
        transform.AffineTransform,
        min_samples=3,
        residual_threshold=ransac_residual_threshold,
        max_trials=1000,
    )

    num_inliers = np.sum(inliers)

    # Decision based on inliers
    if num_inliers >= min_inliers:
        return True

    return False
