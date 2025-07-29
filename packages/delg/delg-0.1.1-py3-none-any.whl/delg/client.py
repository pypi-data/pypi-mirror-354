"""
client
======

High-level client interface for interacting with the DELG feature extraction server.
This module allows users to extract global and local features from single or multiple
images by sending HTTP requests to the running FastAPI-based DELG server, supporting both
sequential and parallel processing.

Note:
- The DELG server is started automatically by the package upon import, so users do not
  need to start it manually.

Public functions:
-----------------
- extract_global_features: Extracts global features from one or more images by sending
  requests to the server.
- extract_local_features: Extracts local features from one or more images by sending
  requests to the server.

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
    url = {github.com/gilja/delg-feature-extractor}
}

@article{cao2020delg,
    title = {Unifying Deep Local and Global Features for Image Search},
    author = {Bingyi Cao and Andre Araujo and Jack Sim},
    journal = {arXiv preprint arXiv:2001.05027},
    year = {2020}
}
"""

import requests
from pathlib import Path
from typing import List, Dict, Union, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from . import config

SERVER_URL = f"http://localhost:{config.docker_port}"


def _post_image(image_path: str, endpoint: str) -> Dict:
    """Helper to post an image to the FastAPI server and return the parsed JSON.

    Posts an image file to the given FastAPI server endpoint and returns the
    server's JSON response.

    Args:
      image_path: Path to the image file to be posted.
      endpoint: Endpoint of the FastAPI server to which the image should be posted.

    Returns:
      dict: Parsed JSON response from the server.
    """

    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    with open(path, "rb") as f:
        files = {"image": f}
        response = requests.post(f"{SERVER_URL}/{endpoint}", files=files, timeout=60)
        response.raise_for_status()
        return response.json()


def extract_global_features(
    image_paths: Union[str, List[str]],
    parallel: bool = False,
    max_workers: Optional[int] = None,
) -> Union[List[float], List[Optional[List[float]]]]:
    """Extracts global features from one or more images.

    This function posts images to the FastAPI server and retrieves their global
    feature descriptors. It supports both single-image and "batch" processing
    with optional parallel execution.

    Args:
      image_paths: Path to a single image file or a list of image file paths.
      parallel: Whether to process images in parallel (only relevant for list input).
      max_workers: Maximum number of threads to use for parallel processing. Defaults
        to min(32, os.cpu_count() + 4).

    Returns:
      list of floats: If a single image path is given, returns its global descriptor
        as a list of floats.
      list of optional lists of floats: If a list of image paths is given, returns a
        list where each element is a descriptor (or None if extraction failed).
    """

    if isinstance(image_paths, str):
        return _post_image(image_paths, "extract/global")["global_descriptor"]

    if not parallel:
        return [
            _post_image(p, "extract/global").get("global_descriptor")
            for p in image_paths
        ]

    results: List[Optional[List[float]]] = [None] * len(image_paths)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_idx = {
            executor.submit(_post_image, path, "extract/global"): idx
            for idx, path in enumerate(image_paths)
        }

        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            try:
                result = future.result()
                results[idx] = result.get("global_descriptor")
            except (requests.RequestException, FileNotFoundError, ValueError, KeyError):
                results[idx] = None

    return results


def extract_local_features(
    image_paths: Union[str, List[str]],
    parallel: bool = False,
    max_workers: Optional[int] = None,
) -> Union[Dict, List[Optional[Dict]]]:
    """Extracts local features from one or more images.

    This function posts images to the FastAPI server and retrieves their local
    feature descriptors. It supports both single-image and batch processing
    with optional parallel execution.

    Args:
      image_paths: Path to a single image file or a list of image file paths.
      parallel: Whether to process images in parallel (only relevant for list input).
      max_workers: Maximum number of threads to use for parallel processing. Defaults
        to min(32, os.cpu_count() + 4).

    Returns:
      dict: If a single image path is given, returns a dictionary of local features.
      list of optional dicts: If a list of image paths is given, returns a list where
        each element is a dictionary of local features (or None if extraction failed).
    """

    if isinstance(image_paths, str):
        return _post_image(image_paths, "extract/local")["local_features"]

    if not parallel:
        return [
            _post_image(p, "extract/local").get("local_features") for p in image_paths
        ]

    results: List[Optional[Dict]] = [None] * len(image_paths)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_idx = {
            executor.submit(_post_image, path, "extract/local"): idx
            for idx, path in enumerate(image_paths)
        }

        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            try:
                result = future.result()
                results[idx] = result.get("local_features")
            except (requests.RequestException, FileNotFoundError, ValueError, KeyError):
                results[idx] = None

    return results
