docker-compose build --no-cache --progress=plain && docker-compose up --wait -d
docker compose run --rm web python manage.py loaddata symm/pgsql/backup_users_and_groups.json
docker compose run --rm web python manage.py create_user_profiles
docker compose run --rm web python manage.py populate_db
docker compose run --rm web python manage.py populate_db_data
docker compose run --rm web cat b11_1/version.txt
