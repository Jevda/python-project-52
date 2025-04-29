#!/usr/bin/env bash
# Exit on error
set -o errexit

# Устанавливаем uv (пакетный менеджер)
echo "Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh
# Добавляем uv в PATH для текущей сессии
source $HOME/.local/bin/env
echo "uv installed successfully."

# Установка зависимостей Python через make (который вызовет uv sync)
echo "Installing dependencies..."
make install

# Сбор статических файлов Django
echo "Collecting static files..."
make collectstatic

# Применение миграций базы данных
echo "Applying database migrations..."
make migrate

echo "Build completed successfully!"