FROM python:3.10-slim-buster

WORKDIR /app

COPY requiraments.txt requiraments.txt

RUN pip3 install -r requiraments.txt

COPY .. 

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0"]
