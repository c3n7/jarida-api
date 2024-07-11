# Jarida API

[![Tests](https://github.com/c3n7/jarida-api/actions/workflows/tests.yaml/badge.svg)](https://github.com/c3n7/jarida-api/actions/workflows/tests.yaml)
[![Deploy](https://github.com/c3n7/jarida-api/actions/workflows/deploy.yaml/badge.svg)](https://github.com/c3n7/jarida-api/actions/workflows/deploy.yaml)
[![Redoc Docs](https://img.shields.io/badge/API_Docs-Redoc-blue)](https://jaridaapi.c3n7.tech/api/schema/redoc/)
[![Swagger Docs](https://img.shields.io/badge/API_Docs-Swagger-blue)](https://jaridaapi.c3n7.tech/api/schema/swagger-ui/)

Part of the Jarida project. Built with Django.

## Installation

Prerequisites:

- Python Installation

Installation Steps:

1. Create virtual environment and activate it:

   ```shell
   python -m venv env
   source env/bin/activate
   ```

   If on windows, activate the environment with:

   ```shell
   env\Scripts\activate
   ```

2. Install requirements
   ```shell
   pip instal -r requirements.txt
   ```
3. Migrate DB (sqlite)
   ```shell
   python manage.py migrate
   ```

## Running the server

This is the easiest bit.

```shell
python manage.py runserver
```

You can view the schema at:

- http://localhost:8000/api/schema/redoc/
- http://localhost:8000/api/schema/swagger_ui/
