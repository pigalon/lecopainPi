
FROM ubuntu:18.04

#MAINTANER Your Name "pigalon@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip locales \
    && localedef -i fr_FR -c -f UTF-8 -A /usr/share/locale/locale.alias fr_FR.UTF-8

ENV LANG fr_FR.UTF-8
RUN mkdir /home/python_app
# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /home/python_app

RUN pip3 install -r /home/python_app/requirements.txt

RUN export LC_ALL=C

EXPOSE 5000


