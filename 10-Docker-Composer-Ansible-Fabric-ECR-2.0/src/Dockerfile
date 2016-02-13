FROM python:2.7
MAINTAINER Marteinn
LABEL version="v1.0.0"

RUN apt-get update && apt-get install netcat -y

ENV PYTHONUNBUFFERED 1

ADD / /src
WORKDIR /src

RUN pip install -r requirements.txt

EXPOSE 8080

COPY ./docker-entrypoint.sh /src/
ENTRYPOINT ["/src/docker-entrypoint.sh"]
