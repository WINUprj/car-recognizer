FROM python:3.8.3-alpine
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
RUN export 'FLASK_ENV'='development'
RUN export 'FLASK_APP'='app.py'