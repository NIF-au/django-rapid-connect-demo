FROM debian:jessie
MAINTAINER Carlo Hamalainen <carlo@carlo-hamalainen.net>

ADD         sources.list /etc/apt/sources.list
RUN         apt-get -qq update
RUN         apt-get -qqy dist-upgrade
RUN         apt-get -qqy install python python-dev ipython python-pip git screen htop vim

RUN         mkdir -p /opt
WORKDIR     /opt

RUN         pip install Django==1.5.1
RUN         pip install PyJWT
RUN         pip install pwgen

ADD         mysite /opt/mysite

WORKDIR     /opt/mysite
ENV         DJANGO_SETTINGS_MODULE mysite.settings
RUN         python manage.py syncdb --noinput
RUN         python create_admin.py

EXPOSE      8000

CMD         python manage.py runserver 0.0.0.0:8000
