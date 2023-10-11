# Docker-команда FROM вказує базовий образ контейнера
FROM python:3.10.5-slim-buster

# Встановимо робочу директорію усередині контейнера
WORKDIR /app

# Якщо не змінювались то не завантажує
COPY ./requirements.txt /app

# Встановимо залежності усередині контейнера
RUN pip install -r requirements.txt  # pip freeze > requirements.txt
COPY . /app

# Позначимо порт де працює програма всередині контейнера
EXPOSE 8000

# Вказуємо том для даних
VOLUME /app/data

# Запустимо нашу програму всередині контейнера
CMD ["python", "doc_X_chat/manage.py", "runserver", "0.0.0.0:8000"]
