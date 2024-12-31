docker-compose build --no-cache --progress=plain && docker-compose up -d
sleep 20
docker compose run --rm web python manage.py loaddata b11_1/pgsql/backup_users_and_groups.json
docker compose run --rm web python manage.py create_user_profiles
docker compose run --rm web python manage.py populate_db
docker compose run --rm web python manage.py populate_db_data
docker compose run --rm web cat b11_1/version.txt
