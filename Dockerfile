FROM ubuntu
COPY . /app
WORKDIR /app

RUN ./run install
RUN ./run build

CMD ./run Sample.txt
