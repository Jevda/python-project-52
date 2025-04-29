#!/usr/bin/env bash
# Exit on error
set -o errexit

# Установка зависимостей
echo "Installing dependencies..."
make install

# Сбор статических файлов Django
echo "Collecting static files..."
make collectstatic

# Применение миграций базы данных
echo "Applying database migrations..."
make migrate

echo "Build completed successfully!"