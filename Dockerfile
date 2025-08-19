ARG NODE_VERSION=23

FROM node:${NODE_VERSION}-alpine

ARG PNPM_VERSION=10.15.0

LABEL maintainer="Dennis <33402703+pm-dennis@users.noreply.github.com>"
LABEL version="${PNPM_VERSION}"
LABEL description="Node.js ${NODE_VERSION} alpine image with pnpm ${PNPM_VERSION}"

WORKDIR /app

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
ENV COREPACK_ENABLE_DOWNLOAD_PROMPT=0
ENV PNPM_NO_UPDATE_NOTIFIER=true

RUN apk add --no-cache bash \
    && npm install -g corepack \
    && npm cache clean --force \
    && corepack enable

RUN corepack prepare pnpm@${PNPM_VERSION} --activate

SHELL ["/bin/bash", "-c"]
