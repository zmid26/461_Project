FROM ubuntu

#Check for Ubuntu update
RUN apt-get update

#Installs Ubuntu
RUN apt-get install -y \
    build-essential \
    curl

#Install Python and Rust
RUN apt-get install -y python3 python3-pip
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
EXPOSE 8080

WORKDIR /usr/src/app
COPY . .

RUN ./run install
RUN ./run build


CMD ./run 
