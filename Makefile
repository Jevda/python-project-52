# Makefile для управления проектом

# Определяем переменную для порта, используемого Gunicorn (по умолчанию 8000)
PORT ?= 8000

install:
	# Устанавливает/синхронизирует зависимости из pyproject.toml
	uv sync

build:
	# Запускает скрипт сборки для Render.com
	# Убедитесь, что скрипт build.sh существует и имеет права на выполнение
	chmod +x ./build.sh
	./build.sh

# Команда для запуска приложения на Render.com (использует Gunicorn)
# Запускаем gunicorn с 4 воркерами, слушаем на всех интерфейсах на порту из переменной PORT
render-start:
	gunicorn task_manager.wsgi:application --workers 4 -b 0.0.0.0:$(PORT)

# Команда для запуска локального сервера разработки Django
runserver:
	python manage.py runserver

# --- ИЗМЕНЕНИЯ ЗДЕСЬ ---
# Команда для запуска линтера ruff
lint:
	# Запускаем ruff check для основного пакета и всех приложений
	uv run ruff check task_manager users statuses tasks labels .

# Команда для запуска тестов pytest
test:
	# Запускаем pytest через uv run
	uv run pytest
# --- КОНЕЦ ИЗМЕНЕНИЙ ---

# Команда для сбора статических файлов (нужна для build.sh и развертывания)
collectstatic:
	# --noinput отключает интерактивные запросы
	python manage.py collectstatic --noinput

# Команда для применения миграций базы данных
migrate:
	python manage.py migrate

# Команда для создания файлов миграций
makemigrations:
	python manage.py makemigrations

# Команда для очистки временных файлов
clean:
	find . -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -r {} +
	rm -rf .pytest_cache

# Определение .PHONY для команд, которые не связаны с файлами
# Добавляем новые команды makemigrations и clean
.PHONY: install build render-start runserver lint test collectstatic migrate makemigrations clean