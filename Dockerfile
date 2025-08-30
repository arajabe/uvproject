# Use lightweight Python
FROM python:3.11-slim

# Install system dependencies for OpenCV and Tesseract
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    libtesseract-dev \
    libgl1 \
    libglib2.0-0 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Optional: install extra language packs (Hindi + Tamil)
# RUN apt-get update && apt-get install -y tesseract-ocr-hin tesseract-ocr-tam
# Set working directory inside container

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Expose backend + frontend ports
EXPOSE 8000
EXPOSE 8501