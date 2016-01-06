FROM ubuntu:trusty

RUN echo "deb http://us.archive.ubuntu.com/ubuntu/ trusty-updates main restricted" | sudo tee -a /etc/apt/sources.list.d/trusty-updates.list
RUN apt-get update
RUN apt-get install -y libpq-dev python python-dev python-setuptools
RUN apt-get install -y binutils libproj-dev gdal-bin
RUN easy_install pip

WORKDIR /app

ADD requirements /requirements
RUN pip install -r /requirements/base.txt

EXPOSE 8000

COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
