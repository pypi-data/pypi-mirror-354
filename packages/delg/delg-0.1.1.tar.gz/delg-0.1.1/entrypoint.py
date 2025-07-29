"""
entrypoint
==========

This module defines the FastAPI application and its HTTP endpoints for the DELG
feature extractor server. It includes endpoints for server health checks, global
feature extraction, local feature extraction, and dynamic local configuration updates.

Public endpoints:
-----------------
- health_check: GET endpoint that returns the server health status.
- extract_global: POST endpoint that extracts global features from an uploaded image.
- extract_local: POST endpoint that extracts local features from an uploaded image.
- update_local_config_api: POST endpoint to update local feature extraction configuration.

At server startup, this module also initializes the DELG extractors by loading the
required configurations and models.

For more information on the endpoints, refer to their individual docstrings.

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

from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
from typing_extensions import Literal
import numpy as np
from io import BytesIO
from PIL import Image

from delg import extractor
from delg.utils import _load_config, _default_config_path
from typing import Dict

from google.protobuf import text_format

app = FastAPI()


@app.get("/healthz")
def health_check():
    """
    Health check endpoint for the DELG server.

    Returns:
      dict: JSON object with status "ok" to indicate the server is healthy.
    """

    return {"status": "ok"}


@app.on_event("startup")
def load_models():
    """
    Loads the DELG extractors once at server startup and stores them in app state.

    Initializes the global and local feature extractors by loading their
    configuration files and creating extractor functions. Stores the extractors
    in the FastAPI app state for reuse across requests.

    Raises:
      Exception: If any extractor fails to load.
    """

    app.state.extractors = {}
    for mode in ["global", "local"]:
        try:
            config_path = _default_config_path(mode)
            config = _load_config(config_path)
            app.state.extractors[mode] = extractor._MakeExtractor(config)
        except Exception as e:
            print(f"❌ Failed to load {mode} extractor: {e}")
            raise


def _extract_features(image_bytes: bytes, mode: Literal["global", "local"]) -> Dict:
    """
    Runs DELG feature extraction on raw image bytes.

    Converts the raw image bytes to an RGB image, passes it through the appropriate
    extractor (global or local), and returns the extracted features.

    Args:
      image_bytes: Raw bytes representing the image file.
      mode: String indicating the type of features to extract ('global' or 'local').

    Returns:
      dict: JSON-serializable dictionary containing the extracted features.

    Raises:
      HTTPException: If the image cannot be processed or if feature extraction fails.
    """

    try:
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid image file") from exc

    image_np = np.array(image)
    extractor_fn = app.state.extractors[mode]
    features = extractor_fn(image_np)

    if mode == "global":
        vector = features.get("global_descriptor")
        if vector is None:
            raise HTTPException(
                status_code=500, detail="Failed to compute global features"
            )
        return {"global_descriptor": vector.tolist()}

    local = features.get("local_features")
    if local is None:
        raise HTTPException(status_code=500, detail="Failed to compute local features")
    return {
        "local_features": {
            "locations": local["locations"].tolist(),
            "descriptors": local["descriptors"].tolist(),
            "scales": local["scales"].tolist(),
            "attention": local["attention"].tolist(),
        }
    }


@app.post("/extract/global")
async def extract_global(image: UploadFile = File(...)):
    """
    POST endpoint to extract global features from an image.

    Accepts an uploaded image file, reads it, and returns its global feature
    descriptor as a JSON response.

    Args:
      image: Uploaded image file.

    Returns:
      JSONResponse: JSON-encoded dictionary containing the global descriptor.
    """

    image_bytes = await image.read()
    result = _extract_features(image_bytes, mode="global")
    return JSONResponse(content=result)


@app.post("/extract/local")
async def extract_local(image: UploadFile = File(...)):
    """
    POST endpoint to extract local features from an image.

    Accepts an uploaded image file, reads it, and returns its local feature
    descriptors as a JSON response.

    Args:
      image: Uploaded image file.

    Returns:
      JSONResponse: JSON-encoded dictionary containing the local features.
    """

    image_bytes = await image.read()
    result = _extract_features(image_bytes, mode="local")
    return JSONResponse(content=result)


@app.post("/config/local")
async def update_local_config_api(request: Request):
    """
    Updates the local DELG configuration inside the container.

    Accepts a JSON payload containing the 'max_feature_num' and 'score_threshold'
    parameters, validates their presence, updates the local configuration file,
    and persists the changes. If successful, returns a status message indicating
    the update was applied.

    Args:
      request (Request): The FastAPI Request object containing the JSON payload.

    Returns:
      dict: A dictionary containing a 'status' key indicating the update result.

    Raises:
      HTTPException:
        - status_code=400 if any required parameter is missing from the payload.
        - status_code=500 if any unexpected error occurs during processing.
    """

    try:
        data = await request.json()
        max_feature_num = data.get("max_feature_num")
        score_threshold = data.get("score_threshold")

        if max_feature_num is None or score_threshold is None:
            raise HTTPException(status_code=400, detail="Missing parameters")

        config_path = _default_config_path("local")
        config = _load_config(config_path)

        config.delf_local_config.max_feature_num = max_feature_num
        config.delf_local_config.score_threshold = score_threshold

        with open(config_path, "w", encoding="utf-8") as f:
            f.write(text_format.MessageToString(config))

        return {"status": "updated"}

    except OSError as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update config file: {e}"
        )
