# foodgram-fastapi


alembic revision --autogenerate -m 'initial'
alembic upgrade head
alembic downgrade head
python main.py

сменить в settings .env-local на .env при тестировании в докере

http://localhost:8000/api/fastapi-docs/  - сваггер