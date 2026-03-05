#!/bin/bash

echo "Starting setup..."

if ! command -v gdown &> /dev/null
then
    pip install gdown
fi

echo "Downloading images from Google Drive..."

python3 -m gdown --id 15XXgrPT6Zj96JWoiiFxDu-9OQGRtpl3G -O images.zip

echo "Extracting images..."

unzip images.zip -d images

echo "Cleaning up..."

rm images.zip

echo "Setup complete!"
