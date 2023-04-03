FROM python:3.10-slim-buster

WORKDIR /app

ENV PORT 8080

COPY requirements_gcp.txt requirements_gcp.txt

RUN pip3 install -r requirements_gcp.txt

EXPOSE 8080

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0"]
