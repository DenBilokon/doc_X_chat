# Docker-команда FROM вказує базовий образ контейнера
ARG PYTHON_VERSION=3.10-slim-buster

FROM python:${PYTHON_VERSION}

# Встановимо робочу директорію усередині контейнера
WORKDIR .

# Якщо не змінювались то не завантажує
COPY ./requirements.txt .

# Встановимо залежності усередині контейнера
RUN pip install -r requirements.txt  # pip freeze > requirements.txt
COPY . .

# Позначимо порт де працює програма всередині контейнера
EXPOSE 8000

# Запустимо нашу програму всередині контейнера
CMD ["python", "doc_X_chat/manage.py", "runserver", "0.0.0.0:8000"]


