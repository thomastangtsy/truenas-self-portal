FROM python:3.8-alpine

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP=app
ENV HOST=0.0.0.0
ENV PORT=5000
CMD flask run --host $HOST --port $PORT
