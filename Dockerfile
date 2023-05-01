FROM python:3.10-slim-buster
WORKDIR /flask-app
COPY src/. src/.
COPY Cargo.toml .
COPY requirements.txt .
COPY run .
RUN pip3 install -r src/APIs/requirements.txt
RUN apt-get update && apt-get install -y default-libmysqlclient-dev
EXPOSE 8080
ENV PORT 8080
ENV PYTHONPATH "${PYTHONPATH}:/flask-app"
CMD exec gunicorn --chdir /flask-app/src/APIs --bind :$PORT --workers 1 --threads 8 --timeout 0 __init__:app
