FROM python:3.10-alpine
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt ./requirements.txt

RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
            gcc python3-dev libpq-dev musl-dev zlib-dev 

RUN pip install -r ./requirements.txt

RUN apk del .tmp-build-deps

RUN mkdir /api
WORKDIR /api
COPY ./api /api

RUN adduser -D user
USER user