"""
model_weights
=============

This module provides a helper function to download the pretrained DELG model
weights from Google Cloud Storage and extract them into the appropriate directory
for use during feature extraction. The model weights are stored in TensorFlow’s
SavedModel format and placed in the 'parameters' subdirectory located inside the
installed 'delg' package directory.

The download_weights function is idempotent, ensuring that the model is always
available for the extractor without redundant downloads. It is called automatically
at package initialization if the weights are not already present but can also be
called manually if needed.

Public functions:
-----------------
- download_weights: Downloads the DELG model weights and extracts them into
  the 'parameters' subdirectory within the installed 'delg' package directory.

For more information on the function, refer to its docstring.

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
import tempfile
import tarfile
import requests


MODEL_URL = "https://storage.googleapis.com/delf/r50delg_gldv2clean_20200914.tar.gz"


def download_weights():
    """
    Downloads the DELG model weights and extracts them into the appropriate directory.

    Retrieves the pretrained DELG model weights from a remote server and extracts
    them into the `delg/parameters` directory for use during feature extraction.

    Raises:
      RuntimeError: If the download or extraction process fails.
    """

    PACKAGE_DIR = os.path.dirname(__file__)
    destination_dir = os.path.join(PACKAGE_DIR, "parameters")

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    print(f"Downloading model weights from: {MODEL_URL}...")
    try:
        response = requests.get(MODEL_URL, stream=True, timeout=180)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to download weights: {e}") from e

    # save to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".tar.gz") as tmp_file:
        for chunk in response.iter_content(chunk_size=8192):
            tmp_file.write(chunk)
        tmp_file_path = tmp_file.name

    print("Download complete.")

    # extract the archive
    try:
        with tarfile.open(tmp_file_path, "r:gz") as tar:
            tar.extractall(path=destination_dir)
    except Exception as e:
        raise RuntimeError(f"Failed to extract weights: {e}") from e
    finally:
        os.remove(tmp_file_path)

    print("Model weights downloaded and extracted successfully.")
