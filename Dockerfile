FROM python:3.8.3-slim
RUN mkdir /code
ADD ./requirements.txt /code
WORKDIR /code
RUN pip install -r requirements.txt
RUN export FLASK_ENV=development
RUN export FLASK_APP='app.py'