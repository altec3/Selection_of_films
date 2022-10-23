FROM python:3.10-slim

ENV FLASK_APP=run \
    FLASK_ENV=production

WORKDIR /code
# Для заполнения таблиц БД
COPY fixtures.json .
COPY load_fixtures.py .

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY run.py .
COPY migrations migrations
COPY project project

# Команда,которая будет выполняться при запуске образа - docker run
CMD flask run -h 0.0.0.0 -p 80
