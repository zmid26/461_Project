FROM python:3.10-slim-buster
WORKDIR /flask-app
COPY src/APIs/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 8080
ENV PORT 8080
COPY src/. .
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app