# Makefile для управления проектом

install:
	# Устанавливает/синхронизирует зависимости из pyproject.toml
	uv sync

build:
	# Запускает скрипт сборки для Render.com
	./build.sh

# Команда для запуска приложения на Render.com (использует Gunicorn)
render-start:
	gunicorn task_manager.wsgi --workers 4 # Запускаем gunicorn с 4 воркерами

# Команда для запуска локального сервера разработки Django
runserver:
	python manage.py runserver

# Команда для запуска линтера (пока не настроена полностью)
lint:
	# uv run ruff check . # Раскомментируем позже
	echo "Linting not configured yet"

# Команда для запуска тестов (пока не настроена полностью)
test:
	# python manage.py test # Или uv run pytest tests/
	echo "Testing not configured yet"

# Команда для сбора статических файлов (нужна для build.sh)
collectstatic:
	python manage.py collectstatic --noinput

# Команда для применения миграций (нужна для build.sh)
migrate:
	python manage.py migrate

.PHONY: install build render-start runserver lint test collectstatic migrate