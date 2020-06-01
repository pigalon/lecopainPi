# Use the Python3.7.2 image
#FROM python:3.8.2-slim-buster
FROM alpine


ADD requirements /app/requirements
# Set the working directory to /app
WORKDIR /app
RUN mkdir /db

#RUN apt update && apt-get install --no-install-recommends -y locales locales-all \
#    libc-dev gcc libpq-dev &&\
#    python3 -m ensurepip && \
#    pip3 install --upgrade pip setuptools && \
#    pip3 install -r requirements/prod.txt && \
#    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apk add --virtual .build-deps && apk add --no-cache \
    libc-dev linux-headers libpq gcc musl-dev postgresql-dev \
    python3 python3-dev\
    bash \
    uwsgi \
    uwsgi-python3 \
    supervisor && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    pip3 install --no-cache-dir -r requirements/prod.txt && \
    rm -r /root/.cache

ENV LC_ALL fr_FR.UTF-8
ENV LANG fr_FR.UTF-8
ENV LANGUAGE fr_FR.UTF-8

# Copy the current directory contents into the container at /app
ADD lecopain /app/lecopain
ADD app.ini /app/app.ini

ADD run.py /app
ADD config.py /app

# Install the dependencies
#RUN /usr/local/bin/python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements/prod.txt

# run the command to start uWSGI
CMD ["uwsgi", "app.ini"]
