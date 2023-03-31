FROM ubuntu
COPY . /app
WORKDIR /app
CMD ./run Sample.txt
