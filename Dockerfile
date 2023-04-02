FROM ubuntu
COPY . /app
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.5 \
    python3-pip \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN ./run install
RUN ./run build

CMD ./run Sample.txt
