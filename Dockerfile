FROM python:3.8-alpine

WORKDIR /code

COPY requirements.txt .

RUN apk update && \
    apk add --virtual build-deps gcc musl-dev && \
    apk add postgresql-dev tzdata&& \
    pip install -r requirements.txt && \
    apk del build-deps gcc musl-dev

COPY src/ .

CMD [ "python", "./main.py" ]