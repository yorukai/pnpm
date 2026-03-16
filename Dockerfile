ARG NODE_VERSION=25

FROM node:${NODE_VERSION}-alpine

ARG PNPM_VERSION=10.32.1

WORKDIR /app

ENV PS1="\[\e[31m\]\h\[\e[0m\] \[\e[33m\]\w\[\e[0m\] \[\e[36m\]>\[\e[0m\] "
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
ENV COREPACK_ENABLE_DOWNLOAD_PROMPT=0
ENV PNPM_NO_UPDATE_NOTIFIER=true

RUN apk add --no-cache bash \
    npm uninstall -g yarn pnpm \
    npm install -g pnpm@${PNPM_VERSION} \
    npm cache clean --force

SHELL ["/bin/bash", "-c"]
