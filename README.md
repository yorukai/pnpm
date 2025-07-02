# pnpm-dockerfile

A lightweight Dockerfile for Node.js 23 on Alpine Linux with [pnpm](https://pnpm.io/) 10.2.0 preinstalled using Corepack.

---

## Features

- Uses official `node:23-alpine` base image for minimal size.
- Installs `pnpm` 10.2.0 via Node’s Corepack.
- Adds `bash` shell for scripting convenience.
- Sets up environment variables for pnpm to work seamlessly.
- Working directory set to `/app` for easy mounting and running your Node.js projects.

---

## Usage

Build the Docker image:

```bash
docker build -t ghcr.io/pm-dennis/pnpm:latest .
```

Run a container with your current directory mounted:

```bash
docker run --rm -it -v "\$PWD":/app ghcr.io/pm-dennis/pnpm:latest sh
```

Inside the container, you can use \`pnpm\` commands directly:

```sh
pnpm install
pnpm run build
```
