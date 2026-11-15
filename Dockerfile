# NODE_SUFFIX is empty for Debian or "-alpine" for Alpine
ARG NODE_VERSION=26
ARG NODE_SUFFIX=""

FROM node:${NODE_VERSION}${NODE_SUFFIX}

ARG PNPM_VERSION=10.32.1

WORKDIR /app

ENV PS1="\[\e[31m\]\h\[\e[0m\] \[\e[33m\]\w\[\e[0m\] \[\e[36m\]>\[\e[0m\] "
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
ENV COREPACK_ENABLE_DOWNLOAD_PROMPT=0
ENV PNPM_NO_UPDATE_NOTIFIER=true

RUN if command -v apk >/dev/null; then \
      apk add --no-cache bash build-base g++ cairo-dev pango-dev giflib-dev librsvg; \
    else \
      apt-get update && \
      apt-get install -y --no-install-recommends bash build-essential g++ libcairo2-dev libpango1.0-dev libgif-dev librsvg2-dev && \
      rm -rf /var/lib/apt/lists/*; \
    fi && \
    npm uninstall -g yarn pnpm && \
    npm install -g pnpm@${PNPM_VERSION} && \
    npm cache clean --force

SHELL ["/bin/bash", "-c"]
