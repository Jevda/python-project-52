### Hexlet tests and linter status:
[![Actions Status](https://github.com/Jevda/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Jevda/python-project-52/actions)
[![CI](https://github.com/Jevda/python-project-52/actions/workflows/ci.yml/badge.svg)](https://github.com/Jevda/python-project-52/actions/workflows/ci.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Jevda_python-project-52&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Jevda_python-project-52)


[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=Jevda_python-project-52&metric=bugs)](https://sonarcloud.io/summary/new_code?id=Jevda_python-project-52)

[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=Jevda_python-project-52&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=Jevda_python-project-52)

[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=Jevda_python-project-52&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=Jevda_python-project-52)

[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=Jevda_python-project-52&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=Jevda_python-project-52)

[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=Jevda_python-project-52&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=Jevda_python-project-52)

[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=Jevda_python-project-52&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=Jevda_python-project-52)

[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=Jevda_python-project-52&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=Jevda_python-project-52)

[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=Jevda_python-project-52&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=Jevda_python-project-52)

[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=Jevda_python-project-52&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=Jevda_python-project-52)

## Мониторинг ошибок

Проект использует Rollbar для отслеживания ошибок в продакшене. Ошибки автоматически регистрируются и отправляются в систему мониторинга, что позволяет оперативно реагировать на проблемы.

# Менеджер задач / Task Manager (python-project-52)

Учебный проект на Hexlet: веб-приложение "Менеджер задач", разработанное на Django.

## Основные функции (Планируемые)
* Регистрация и аутентификация пользователей
* Управление задачами (создание, просмотр, изменение, удаление)
* Управление статусами задач
* Управление метками задач
* Назначение исполнителей
* Фильтрация задач

## Ссылка на развернутое приложение

Проект доступен по адресу: [https://python-project-52-tvt9.onrender.com](https://python-project-52-tvt9.onrender.com)

## Локальный запуск (для разработки)

1.  Клонировать репозиторий:
    `git clone https://github.com/Jevda/python-project-52.git`
2.  Перейти в директорию проекта:
    `cd python-project-52`
3.  Установить зависимости (uv создаст виртуальное окружение `.venv` и установит все из `pyproject.toml`):
    `make install`
    *(Или можно напрямую: `uv sync`)*
4.  Создать файл `.env` в корне проекта. Как минимум, он должен содержать:
    ```dotenv
    SECRET_KEY='ваш_сгенерированный_локальный_ключ'
    DATABASE_URL='sqlite:///db.sqlite3'
    DJANGO_DEBUG='True'
    ```
    *(Сгенерируйте новый ключ для локальной разработки или скопируйте тот, что вы задали в переменных окружения на Render)*
5.  Применить миграции базы данных (будет создан файл `db.sqlite3`):
    `make migrate`
    *(Или можно напрямую: `python manage.py migrate`)*
6.  Запустить сервер разработки:
    `make runserver`
    *(Или можно напрямую: `python manage.py runserver`)*
7.  Открыть `http://127.0.0.1:8000/` в браузере.