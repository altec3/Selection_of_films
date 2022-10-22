FROM python:3.10-slim

ENV FLASK_APP=run \
    FLASK_ENV=production

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt && pip install -U pip
COPY project.db .
COPY run.py .
COPY project project

# Команда,которая будет выполнятся при запуске образа - docker run
CMD flask run -h 0.0.0.0 -p 80
