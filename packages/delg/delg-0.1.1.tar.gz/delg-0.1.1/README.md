# **delg**

![Author](https://img.shields.io/badge/Author-Duje_Giljanović-green)
![Version](https://img.shields.io/badge/Version-0.1.0-green)
![License](https://img.shields.io/badge/License-Apache%202.0-green)\
![Python Version](https://img.shields.io/badge/Python-3.7%2B-blue)
![Docker](https://img.shields.io/badge/Requires-Docker-blue)



**delg** is a Python package that containerizes Google’s DELG (Deep Local and Global features) model for image feature extraction. It provides a seamless interface for extracting both global and local image features through a Dockerized FastAPI server and a Python client.

Originally developed by Google Research, DELG is a state-of-the-art model for large-scale image retrieval, offering both fine-grained local features and holistic global descriptors. This package simplifies the usage by providing a fully containerized, PyPI-compatible solution with automatic model downloading, container management, and easy integration into your Python code.

In addition, this package extends DELG’s original design by implementing **parallel image processing**, allowing you to process multiple images in parallel, even though the DELG model itself does not natively support batch inference. This is accomplished through asynchronous client requests that emulate batch processing for increased efficiency.

&nbsp;

## Features

- **Containerized Server**: Fully Dockerized DELG feature extraction server using FastAPI. Automatically manages Docker images, container lifecycle, and server health checks.
- **Automatic Server Orchestration**: Package automatically starts and stops the Docker container, ensuring a seamless user experience without manual Docker management.
- **Pre-trained Model Management**: Automatically downloads and extracts DELG model weights from Google Cloud Storage if not already available, storing them in the installed package directory for local use.
- **Global Feature Extraction**: Functions to extract global image descriptors using DELG, suitable for image retrieval and similarity search.
- **Local Feature Extraction**: Functions to extract local keypoints and descriptors with attention scores using DELG, enabling fine-grained image matching.
- **Parallel Image Processing**: The client supports processing multiple images in parallel using asynchronous requests, making it possible to efficiently process batches of images even though DELG itself doesn’t natively support batch inference.
- **REST API Endpoints**: Exposes FastAPI endpoints for:
  - Health check (`/healthz`)
  - Global feature extraction (`/extract/global`)
  - Local feature extraction (`/extract/local`)
  - Updating local configuration (`/config/local`)
- **Python Client Functions**: Easy-to-use Python functions to:
  - Extract global and local features (single or multiple images).
  - Compare global features using cosine similarity.
  - Match local features with RANSAC geometric verification.
  - Update Docker runtime settings and local feature extraction configuration at runtime.
- **Dynamic Configuration**: Runtime updates of local feature extraction parameters (`max_feature_num`, `score_threshold`) and Docker container settings (`image name`, `container name`, `port`).
- **Server-side Local Configuration Update**: Allows dynamic reconfiguration of local feature extraction thresholds without restarting the container.
- **Efficient Image Processing**: Includes internal utilities for image loading, resizing, and configuration file parsing to ensure compatibility with DELG’s input requirements.
- **Testing and Logging**: Incorporates automatic logging and error handling for robust feature extraction and server health monitoring.

&nbsp;

## Prerequisites

You must have **Docker** installed and properly set up on your machine. Below are some helpful tips:
  - **macOS**:
    - For Intel-based Macs, Docker Desktop typically installs at `/Applications/Docker.app`, and it automatically adds Docker to your PATH.
    - For Apple Silicon (M1/M2), Docker Desktop also handles PATH configuration automatically.
  - **Windows**:
    - Docker Desktop usually handles PATH setup automatically. If needed, verify that the Docker executable is in your PATH by checking your environment variables.
  - **Linux and other Unix-based systems**:
    - Docker is generally installed via your package manager (e.g., `apt`, `yum`, `dnf`). Make sure the `docker` binary is accessible in your PATH.
    - Common installation paths include `/usr/bin/docker` or `/usr/local/bin/docker`.

> **Important!**  
> After installing Docker, verify that it is accessible from the command line by running:


> ```sh
> docker --version
> ```
>
> You should see the Docker version information displayed.

&nbsp;

## Installation

>
> If you are installing delg in a virtual environment, make sure that PATH has been correctly updated to point to Docker install location! 
>

To install delg simply run

> ```sh
> pip install delg
> ```

&nbsp;

## Usage

Below is a minimal example for using the package to extract both global and local features:

&nbsp;

```python
from delg.client import extract_global_features, extract_local_features
from delg.similarity import local_feature_match, cosine_similarity
import os

from delg.config import update_local_config, set_docker_config

# Define supported image extensions
image_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff", ".webp")


# Load image paths for the first set
images_path_1 = "<path_to_first_image_set>"
image_paths_1 = sorted(
    [
        os.path.join(images_path_1, fname)
        for fname in os.listdir(images_path_1)
        if fname.lower().endswith(image_extensions)
    ]
)

# Load image paths for the second set
images_path_2 = "<path_to_second_image_set>"
image_paths_2 = sorted(
    [
        os.path.join(images_path_2, fname)
        for fname in os.listdir(images_path_2)
        if fname.lower().endswith(image_extensions)
    ]
)

# Extract global features in parallel (preserves order)
global_features_1 = extract_global_features(image_paths_1, parallel=True, max_workers=20)
global_features_2 = extract_global_features(image_paths_2, parallel=True, max_workers=20)

for img1_path, descriptor1 in zip(image_paths_1, global_features_1):
    if descriptor1 is None:
        continue  # Skip images that failed processing

    for img2_path, descriptor2 in zip(image_paths_2, global_features_2):
        if descriptor2 is None:
            continue

        cos_sim = cosine_similarity(descriptor1, descriptor2)

        if cos_sim > <global_similarity_threshold>:
            print(f"Cosine similarity: {cos_sim:.4f}")
            continue

        if cos_sim > <local_similarity_trigger>:
            local_features_1 = extract_local_features(img1_path)
            local_features_2 = extract_local_features(img2_path)

            match = local_feature_match(
                local_features_1,
                local_features_2,
                ransac_residual_threshold=15,
                min_inliers=8,
                ratio_thresh=0.9,
            )

            print(f"Cosine similarity: {cos_sim:.4f}")
            print(f"Local match score: {match}")
```
&nbsp;

If needed, one can modify configuration for local feature extraction and/or Docker runtime settings using the following two functions:

``` python
update_local_config(max_feature_num=1000, score_threshold=454.6)
set_docker_config(image="delg-server", container="delg-server-container", port=8080)
```

&nbsp;

>
> Note: values above are used by default if left unspecified.
>