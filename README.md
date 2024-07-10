# fastapi-template



## Add new model to database

```bash
alembic revision --autogenerate -m "Add new model"
alembic upgrade head
```