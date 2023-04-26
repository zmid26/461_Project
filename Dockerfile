FROM python:3.10-slim-buster
WORKDIR /flask-app
COPY src/. .
RUN pip3 install -r APIs/requirements.txt
EXPOSE 8080
ENV PORT 8080
CMD exec gunicorn --chdir /flask-app/APIs --bind :$PORT --workers 1 --threads 8 --timeout 0 __init__:app