# praktikum_new_diplom

![example workflow](https://github.com/huli-net/foodgram-project-react/actions/workflows/main.yml/badge.svg)

# Описание проекта
Foodgram - сайт для публикации рецептов.
Пользователи могут создавать свои рецепты, читать рецепты других пользователей, подписываться на интересных авторов, добавлять лучшие рецепты в избранное, а также создавать список покупок и загружать его

# Установка проекта локально
Склонировать репозиторий на локальный компъютер:
```sh
git clone git@github.com:huli-net/foodgram-project-react.git
cd foodgram-project-react
``` 
Cоздать и активировать виртуальное окружение:
```sh
python -m venv env
source env/bin/activate
```
Cоздайте файл .env в директории /infra/ с содержанием:
```sh
SECRET_KEY=секретный ключ django
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
Перейти в директирию с файлом requirements.txt и установить зависимости
```sh
cd backend/foodgram
pip install -r requirements.txt
```
Выполнить миграции:
```sh
python manage.py migrate
```
Запустить сервер:
```sh
python manage.py runserver
```
# Запуск проекта в Docker контейнере
Установите Docker.
- Параметры запуска описаны в файлах docker-compose.yml и nginx.conf которые находятся в директории infra/.
При необходимости добавьте/измените адреса проекта в файле nginx.conf

Запустите docker compose:
```sh
docker-compose up -d --build
```
После сборки появляются 3 контейнера:
```sh
контейнер базы данных db
контейнер приложения backend
контейнер web-сервера nginx
```
Примените миграции:
```sh
docker-compose exec backend python manage.py migrate
```
Загрузите ингредиенты:
```sh
docker-compose exec backend python manage.py load_ingrs
```
Загрузите теги:
```sh
docker-compose exec backend python manage.py load_tags
```
Создайте администратора:
```sh
docker-compose exec backend python manage.py createsuperuser
```
Соберите статику:
```sh
docker-compose exec backend python manage.py collectstatic --noinput
```
# Сайт
- Готовый сайт доступен по ссылке: http://Ссылка

# Документация к API
- API документация доступна по ссылке (создана с помощью redoc): http://ссылка/docs/

# Авторы
Лосев Р.Р. https://github.com/huli-net - Python разработчик. Разработал бэкенд и деплой для проекта Foodgram.
Команда Яндекс.Практикум -  Фронтенд для сервиса Foodgram.