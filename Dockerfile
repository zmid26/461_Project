FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements_gcp.txt requirements_gcp.txt

RUN pip3 install -r requirements_gcp.txt

EXPOSE 8080

CMD [ "python3", "app.py"]
