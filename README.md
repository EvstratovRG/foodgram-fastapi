# foodgram-fastap
сменить в settings .env-local на .env при тестировании в докере

http://localhost:8000/api/fastapi-docs/  - сваггер

cd docker_nginx

docker compose up --build   -поднять компоуз

docker exec docker_nginx-backend alembic upgrade head 

 -накатить миграции

чтобы войти в админку, нужно зарегестрировать пользователя и напрямую в базе данных изменить флаг is_superuser в True

после используя email!! и password можно войти в админку (в стандартной форме указан username и password)

импортировать тестовые данные (теги, ингредиенты и тестовых пользователей можно с помощью экшенов реализованных в админке)