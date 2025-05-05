# Makefile для управления проектом

PORT ?= 8000

install:
	uv sync

build:
	chmod +x ./build.sh
	./build.sh

render-start:
	gunicorn task_manager.wsgi:application --workers 4 -b 0.0.0.0:$(PORT)

runserver:
	python manage.py runserver

lint:
	uv run ruff check task_manager users statuses tasks labels .

test:
	uv run pytest

collectstatic:
	python manage.py collectstatic --noinput

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

makemessages:
	django-admin makemessages -l ru

compilemessages:
	django-admin compilemessages

clean:
	find . -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -r {} +
	find . -name '*.mo' -delete
	rm -rf .pytest_cache

.PHONY: install build render-start runserver lint test collectstatic migrate makemigrations clean makemessages compilemessages