# fastapi-template

## Overview

This repository provides a template for building web applications using FastAPI with MariaDB as the database. It includes a basic project structure, configuration files, and examples to help you get started quickly.

## Applications Included

- **FastAPI Application**: A basic FastAPI application example endpoints.
- **Database Integration**: Configuration for integrating with a MariaDB database using SQLAlchemy and Alembic for migrations.
- **Docker Support**: Dockerfile and docker-compose configuration for containerization.
- **Devcontainer Support**: Configuration for Visual Studio Code Dev Containers.
- **GitHub Actions**: Automated testing using GitHub Actions.
- **mypy**: Type checking with mypy.
- **ruff**: Linting with ruff.

## How to Use This Template

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/fastapi-template.git
   cd fastapi-template
   ```

2. **Open in Visual Studio Code**
   * Open the repository in Visual Studio Code.
   * When prompted, reopen in the container.

3. **Set Up the Database**
   * Update the `DATABASE_URL` in the `.env` file with your MariaDB connection string.
   * Run the initial database migrations:
     ```
     alembic upgrade head
     ```

4. **Run the Application**
   ```
   uvicorn app.main:app --reload
   ```

5. **Add New Model to Database**
   * Create a new Alembic revision and apply the migration:
     ```
     alembic revision --autogenerate -m "Add new model"
     alembic upgrade head
     ```

6. **Run Tests**
   * Install test dependencies:
     ```
     pip install -r requirements-test.txt
     ```
   * Run the tests:
     ```
     pytest
     ```

7. **Build and Run with Docker**
   ```
   docker-compose up --build
   ```

## Developing with Docker

1. **Build the Docker Image**
   ```
   docker build -t fastapi-template .
   ```

2. **Run the Docker Container**
   ```
   docker run -d --name fastapi-template-container -p 8000:8000 fastapi-template
   ```

3. **Access the Application**
   * Open your browser and navigate to `http://localhost:8000` to access the FastAPI application.

4. **Stop the Docker Container**
   ```
   docker stop fastapi-template-container
   ```
