#!/bin/bash

echo "Starting setup..."

# Create images directory if not exists
mkdir -p images


if ! command -v gdown &> /dev/null
then
    pip install gdown
fi

echo "Downloading images from Google Drive..."

gdown --id 10TPhKE_95tTcHVZ0A498Be6M0Zvmzojn -O images.zip

echo "Extracting images..."

unzip images.zip -d images

echo "Cleaning up..."

rm images.zip

echo "Setup complete!"
