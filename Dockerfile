
FROM python:3.12.0-alpine


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV API_TOKEN=""

ENV DB_NAME=""
ENV DB_USER=""
ENV DB_PASSWORD=""
ENV DB_HOST=""
ENV DB_PORT='5432'


RUN apk add --update bash

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt



COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]