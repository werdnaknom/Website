FROM python:3.8

ENV HTTP_PROXY "http://proxy.jf.intel.com:912"
ENV HTTPS_PROXY "http://proxy.jf.intel.com:912"

RUN adduser --disabled-password flaskweb
WORKDIR /home/flaskweb
#RUN apk add --no-cache bash

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

COPY app app
COPY database_functions database_functions
COPY flaskweb.py config.py boot.sh celery_worker.py ./
RUN chmod +x boot.sh

ENV FLASK_APP flaskweb.py

ENV MONGO_DOCKER_NAME "${MONGO_DOCKER_NAME}"
ENV UPLOAD_FOLDER "${UPLOAD_FOLDER}"

RUN mkdir "/uploads/"
RUN chown -R flaskweb:flaskweb "/uploads/"
RUN chown -R flaskweb:flaskweb ./
USER flaskweb

EXPOSE 5000

ENTRYPOINT ["./boot.sh"]

