FROM python:2.7
MAINTAINER Marteinn
LABEL version="v1.0.0"

RUN apt-get update && apt-get install netcat -y

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
ADD . /app/

RUN pip install -r requirements/prod.txt

EXPOSE 8080

COPY ./docker-entrypoint.sh /app/
ENTRYPOINT ["/app/docker-entrypoint.sh"]
