FROM ubuntu:16.04

MAINTAINER Roland Oviol "rolandoviol@gmail.com"
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y python3-pip pdftk

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip3 install --upgrade "pip < 21.0"
RUN pip3 install -U setuptools
RUN pip3 install -r requirements.txt
COPY ./src /app
ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]