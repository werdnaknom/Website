FROM python:3.8

WORKDIR /app

# We copy just the requirements.txt first to leverage Docker cache
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

COPY app app
COPY flaskweb.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP flaskweb.py

EXPOSE 5000

ENTRYPOINT [ "./boot.sh" ]

