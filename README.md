# pnpm Docker Image Sync

This repository automatically builds and publishes a Docker image for the latest [pnpm](https://pnpm.io/) release using GitHub Actions. The image is based on Node.js Alpine and comes pre-installed with the latest `pnpm`.

## Features

- Automatically detects the latest `pnpm` release.
- Builds a Docker image tagged with the `pnpm` version (e.g., `10.15.0`) and `latest`.
- Pushes the image to GitHub Container Registry (GHCR).
- Scheduled daily updates via GitHub Actions.

## Docker Image

- Registry: `ghcr.io/pm-dennis/pnpm`
- Tags:
  - `<pnpm-version>` (e.g., `10.15.0`)
  - `latest`

### Example Usage

```bash
docker pull ghcr.io/pm-dennis/pnpm:latest
docker run --rm ghcr.io/pm-dennis/pnpm:latest pnpm --version
```

## Workflow Overview

The GitHub Actions workflow:

1. Detects the latest `pnpm` release.
2. Checks if the corresponding Docker image already exists in GHCR.
3. Builds and pushes the Docker image if it’s not already available.
4. Tags the image with both the release version and `latest`.

## Contributing

Contributions are welcome! Submit issues or pull requests to improve the workflow, update dependencies, or enhance documentation.
