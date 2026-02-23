FROM python:3.13.12-trixie

ENV TZ=America/Sao_Paulo

ENV LANG=pt_BR.UTF-8
ENV LANGUAGE=pt_BR.UTF-8
ENV LC_ALL=pt_BR.UTF-8

RUN apt-get update -y && \
    apt-get install git fish vim curl ca-certificates locales locales-all -y && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir uv rust-just

RUN curl -fsSL https://bun.com/install | bash
