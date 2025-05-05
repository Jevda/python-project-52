#!/usr/bin/env bash
set -o errexit

echo "Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
echo "uv installed successfully."

echo "Installing dependencies..."
make install

echo "Compiling translation files..."
django-admin compilemessages

echo "Collecting static files..."
make collectstatic

echo "Applying database migrations..."
make migrate

echo "Build completed successfully!"