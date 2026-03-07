FROM astral/uv:0.10.9-python3.13-trixie

COPY --from=oven/bun:1.3.10-slim /usr/local/bin/bun /usr/local/bin/bun

ARG TZ=America/Sao_Paulo
ARG LANG=pt_BR.UTF-8
ARG LOCALE=pt_BR.UTF-8
ARG LC_ALL=pt_BR.UTF-8

ENV TZ=${TZ}
ENV LANG=${LANG}
ENV LOCALE=${LOCALE}
ENV LC_ALL=${LC_ALL}

RUN apt-get update -y && \
    apt-get install vim just starship curl locales locales-all \
            libgl1 libegl1 libglib-2.0 libdbus-1-3 libxcb-xinerama0 \
            libxcb-cursor0 libxcb-keysyms1 libxcb-image0 libxcb-shm0 \
            libxcb-icccm4 libxcb-sync1 libxcb-xfixes0 libxcb-shape0 \
            libxcb-randr0 libxcb-render-util0 libxcb-render0 libxcb-xkb1 \
            libxkbcommon-x11-0 -y --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*
