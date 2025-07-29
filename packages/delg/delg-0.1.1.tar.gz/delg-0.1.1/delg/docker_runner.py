"""
docker_runner
=============

This module provides internal helper functions for managing the DELG Docker container,
including checking Docker image availability, building the Docker image, starting and
stopping the container, and ensuring the server is running before feature extraction.

These functions are intended for internal use only and are orchestrated automatically
by the package. The container is started when needed and automatically shut down when
the Python process that imported this package exits, ensuring resources are cleaned up
properly.

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
import subprocess
import time
import atexit
import requests
from . import config

_docker_process = None


def _docker_image_exists() -> bool:
    """
    Checks whether the specified DELG Docker image exists locally.

    Runs a Docker command to verify whether the Docker image specified in the
    configuration exists on the local machine. Also indirectly confirms that
    Docker is installed, raising an error if it is not.

    Returns:
      bool: True if the Docker image exists locally, False otherwise.

    Raises:
      RuntimeError: If Docker is not installed on the system.
    """

    try:
        result = subprocess.run(
            ["docker", "images", "-q", config.docker_image],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        return result.stdout.strip() != ""
    except FileNotFoundError as exc:
        raise RuntimeError(
            "Docker not found. Please install Docker and try again."
        ) from exc


def _build_docker_image():
    """
    Builds the DELG Docker image locally.

    Runs the Docker build command using the image name specified in the configuration,
    building the Docker image from the directory containing the Dockerfile.

    Raises:
      subprocess.CalledProcessError: If the Docker build process fails.
    """
    # Find the directory containing this module (__file__) and move one level up
    PACKAGE_DIR = os.path.dirname(__file__)
    PROJECT_ROOT = os.path.abspath(os.path.join(PACKAGE_DIR, ".."))

    dockerfile_path = os.path.join(PROJECT_ROOT, "Dockerfile")
    if not os.path.exists(dockerfile_path):
        raise FileNotFoundError(f"Dockerfile not found at {dockerfile_path}")

    subprocess.run(
        ["docker", "build", "-t", config.docker_image, PROJECT_ROOT], check=True
    )


def _wait_for_server(timeout=60):
    """
    Blocks until the DELG server responds on the /healthz endpoint.

    Periodically checks the server's /healthz endpoint to ensure that the
    Docker container has started successfully and is ready to accept requests.
    Times out if the server does not respond within the specified timeout period.

    Args:
      timeout: Maximum time in seconds to wait for the server to become ready.

    Raises:
      RuntimeError: If the server does not become available in time.
    """

    url = f"http://localhost:{config.docker_port}/healthz"
    for _ in range(timeout * 2):
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                return  # Only return when server is ready
        except requests.exceptions.RequestException:
            pass
        time.sleep(0.5)
    raise RuntimeError("Server did not become available in time.")


def _start_docker_container():
    """
    Starts the DELG Docker container in a separate process.

    Launches the Docker container in the background, binding the configured port
    and using the configured image and container name. Registers an automatic
    shutdown hook to ensure the container is stopped when the main process exits.

    Notes:
      Uses subprocess.Popen to start the container in its own process group.
    """

    global _docker_process

    _docker_process = subprocess.Popen(
        [
            "docker",
            "run",
            "--rm",
            "-p",
            f"{config.docker_port}:8080",
            "--name",
            config.docker_container,
            config.docker_image,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,  # ensures separate process group
    )

    # Register automatic shutdown hook
    atexit.register(_stop_docker_container)


def _stop_docker_container():
    """
    Stops the running DELG Docker container if it is active.

    Attempts to stop the Docker container specified in the configuration. Handles
    errors related to missing Docker installation, insufficient permissions, or
    unexpected subprocess issues.

    Raises:
      RuntimeError: If Docker is not installed, permissions are insufficient, or
        any other subprocess error occurs.
    """

    try:
        subprocess.run(
            ["docker", "stop", config.docker_container],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(
            "Docker not found. Please install Docker and try again."
        ) from exc
    except PermissionError as exc:
        raise RuntimeError(
            "Permission denied. Try running with elevated privileges."
        ) from exc
    except subprocess.SubprocessError as exc:
        raise RuntimeError(
            "An unexpected error occurred while stopping the Docker container."
        ) from exc


def _ensure_server_running():
    """
    Ensures that the DELG server is running and ready for requests.

    Checks whether the Docker image exists locally, builds it if necessary,
    starts the Docker container, and waits until the server responds on /healthz.
    """

    if not _docker_image_exists():
        _build_docker_image()

    _start_docker_container()
    _wait_for_server()
