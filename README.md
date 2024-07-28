# FastAPI-Template

[![Lint Check](https://github.com/solufit/fastapi-template/actions/workflows/lint-python.yml/badge.svg)](https://github.com/solufit/fastapi-template/actions/workflows/lint-python.yml)
[![Python application test](https://github.com/solufit/fastapi-template/actions/workflows/test-python.yml/badge.svg)](https://github.com/solufit/fastapi-template/actions/workflows/test-python.yml)

## Overview

This FastAPI-Template is a public GitHub template designed to help developers quickly set up and develop APIs. It provides a solid foundation with various features and integrations to streamline the development process.

## Features

- **FastAPI Application**: A basic FastAPI application with example endpoints.
- **Database Integration**: Configuration for integrating with a MariaDB database using SQLAlchemy and Alembic for migrations.
- **Docker Support**: Dockerfile and docker-compose configuration for containerization.
- **Devcontainer Support**: Configuration for Visual Studio Code Dev Containers.
- **GitHub Actions**: Automated testing using GitHub Actions.
- **mypy**: Type checking with mypy.
- **ruff**: Linting with ruff.

## How to use this template

1. Click on the "Use this template" button on the GitHub repository page.
2. Clone your new repository to your local machine.
3. Follow the development instructions below to start building your API.

## How to develop

This template is optimized for use with Visual Studio Code.

### Develop with DevContainer

1. Ensure you have Docker and the Remote - Containers extension installed in VS Code.
2. Open the project folder in VS Code.
3. When prompted, click "Reopen in Container" or run the "Remote-Containers: Reopen in Container" command from the command palette.
4. VS Code will build and start the development container, providing you with a fully configured environment.

### Develop with Docker

1. Ensure you have Docker and Docker Compose installed on your system.
2. Run `docker-compose up -d` to start the development environment.
3. Use your preferred editor to make changes to the code.
4. The FastAPI application will be available at `http://localhost:8000`.

## Deploy

### Deploy with Docker Compose

1. Ensure you have Docker and Docker Compose installed on your production server.
2. Copy the `docker-compose.yml` file to your server.
3. Run `docker-compose up -d` to start the application in production mode.

## Directory Structure

```
fastapi-template
|-- LICENSE
|-- README.md
|-- alembic.ini
|-- database # Contains database-related files and migration scripts.
|   |-- README
|   |-- __init__.py
|   |-- env.py
|   |-- models.py # Defines SQLAlchemy ORM models.
|   |-- script.py.mako
|   `-- versions
|       |-- cbc697a95795_init_database.py
|       `-- fa9c8b7e809a_fix_type.py
|-- docker
|   `-- api
|       `-- dockerfile
|-- docker-compose-prod.yml
|-- docker-compose.yml
|-- example.env # Example environment variable file. Copy to .env and modify as needed
|-- log_config.yaml # Logging configuration files. 
|-- log_config_debug.yaml # Logging configuration files. Used for debugging.
|-- pyproject.toml
|-- requirements-test.txt
|-- requirements.txt -> ./src/requirements.txt
|-- src
|   |-- __init__.py
|   |-- app.py # Main FastAPI application file.
|   |-- endpoints # API endpoints.
|   |   |-- __init__.py
|   |   `-- v1 # Version 1 of the API endpoints.
|   |       |-- __init__.py
|   |       `-- version.py
|   |-- requirements.txt
|   |-- scheme # Pydantic schemas for request/response models.
|   |   |-- __init__.py
|   |   `-- version.py
|   `-- utils
|       |-- __init__.py
|       `-- database.py # Contains Database connection and session management Class.
|-- start.sh
|-- tests # Contains test files.
|   |-- __init__.py
|   |-- test_database.py
|   `-- test_version.py
`-- update_depends.sh
```

## Git rule

This repository follows the GitHub Flow workflow:

1. Create a new branch for each feature or bugfix.
2. Make changes and commit to the branch.
3. Open a pull request for review.
4. After approval, merge the branch into main.
5. Delete the feature branch after merging.

## CI

GitHub Actions are configured to run tests automatically on each pull request:

- Runs pytest for unit and integration tests
- Performs type checking with mypy
- Lints the code with ruff

## Configuring linting and type checking

### Ruff (Linting)

To modify ruff linting rules, edit the `pyproject.toml` file in the root directory. Adjust the `[tool.ruff]` section to customize ruff's behavior.

### Mypy (Type Checking)

To configure mypy type checking, add or modify the `[tool.mypy]` section in your `pyproject.toml` file. 

You can adjust these settings based on how strict you want the type checking to be. For more options, refer to the [mypy configuration file documentation](https://mypy.readthedocs.io/en/stable/config_file.html).

Remember to run `mypy` and `ruff` regularly during development to catch type errors and style issues early.
If you use Visual Studio Code, you can install the Python extension to get real-time feedback on type errors and linting issues.

## License

This project is licensed under the MIT License. See the LICENSE file for details.