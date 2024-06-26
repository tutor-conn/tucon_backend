FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt gunicorn

ENV ENV prod
ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 tucon_backend:app
