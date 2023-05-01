# First stage: build the Rust binary
FROM rust:1.69-slim-buster as rust-builder
WORKDIR /rust-app
COPY src/. src/.
COPY Cargo.toml .
RUN apt-get update && apt-get install -y pkg-config libssl-dev && rm -rf /var/lib/apt/lists/*
RUN cargo build --release

# Second stage: run the Flask app with the Rust binary
FROM python:3.10-slim-buster
WORKDIR /flask-app
COPY --from=rust-builder /rust-app/target/release/project_461 rater
COPY src/. src/.
COPY run .
RUN pip3 install -r src/APIs/requirements.txt
RUN apt-get update && apt-get install -y default-libmysqlclient-dev
EXPOSE 8080
ENV PORT 8080
ENV PYTHONPATH "${PYTHONPATH}:/flask-app"
CMD ./run https://github.com/jashkenas/underscore
# CMD exec gunicorn --chdir /flask-app/src/APIs --bind :$PORT --workers 1 --threads 8 --timeout 0 __init__:app
