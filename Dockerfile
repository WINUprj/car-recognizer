FROM python:3.8.3-slim
# RUN apk update && \
#     apk add make automake gcc g++ subversion python3-dev
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
RUN export 'FLASK_APP'='app.py'
RUN export 'FLASK_ENV'='development'