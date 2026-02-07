#!/bin/bash
# Install all packages in the monorepo

set -e

echo "Installing ModPocket packages..."

for package in packages/*; do
    if [ -d "$package" ]; then
        echo "Installing $package..."
        pip install -e "$package[dev]"
    fi
done

echo "All packages installed successfully!"
