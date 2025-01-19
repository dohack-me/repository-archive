FROM ubuntu:18.04 as src

RUN apt-get update && apt-get install -y build-essential
RUN mkdir /workdir
COPY . /workdir
WORKDIR /workdir
RUN make
