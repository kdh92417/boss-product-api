FROM python:3.11
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get -y update

ADD . /payhere
WORKDIR /payhere

RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
