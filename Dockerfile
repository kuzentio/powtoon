FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN apt-get update -q -y

RUN mkdir /powtoon
WORKDIR /powtoon
ADD . .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 8000
