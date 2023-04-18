FROM python:3.10-slim-buster

WORKDIR /app

COPY src/APIs/requirements.txt .

RUN pip3 install -r requirements.txt

EXPOSE 8080

COPY src/APIs/app.py app.py

CMD [ "python3", "app.py"]
