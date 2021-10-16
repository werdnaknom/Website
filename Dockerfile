FROM python:3.8

WORKDIR /app

# We copy just the requirements.txt first to leverage Docker cache
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./ .

ENTRYPOINT [ "python" ]

CMD [ "flask_web/app.py" ]
