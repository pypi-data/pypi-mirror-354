FROM python:3.6-slim

# Install TF 2.2.0 (CPU-only) and strict dependency versions
RUN pip install --no-cache-dir \
    'typing_extensions==3.10.0.2' \
    'tensorflow-cpu==2.2.0' \
    'protobuf==3.11.3' \
    'fastapi==0.63.0' \
    'python-multipart==0.0.5' \
    'uvicorn==0.13.4' \
    'pillow==7.2.0' \
    'numpy==1.18.5' \
    'requests==2.24.0' \
    'scikit-learn==0.24.2' \
    'scikit-image==0.17.2'

# Set working directory
WORKDIR /app

# Copy your already-prepared DELG package (with precompiled *_pb2.py files)
COPY delg/ ./delg/
COPY entrypoint.py .

# Expose FastAPI port
EXPOSE 8080

# Run the FastAPI server
CMD ["uvicorn", "entrypoint:app", "--host", "0.0.0.0", "--port", "8080"]
