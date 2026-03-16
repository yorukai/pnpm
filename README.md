# pnpm Docker Image Sync

This repository automatically builds and publishes Docker images for the latest [pnpm](https://pnpm.io/) release using GitHub Actions. Images are based on Node.js Alpine and built for multiple Node.js versions.

## Features

- Automatically detects the latest `pnpm` release.
- Builds images for multiple Node.js versions in parallel (20, 22, 24, 25).
- Publishes a comprehensive set of tags covering every pnpm × Node.js combination.
- Scheduled daily updates via GitHub Actions.

## Docker Image

- Registry: `ghcr.io/yorukai/pnpm`

### Tag Reference

| Tag | pnpm version | Node.js version |
|-----|-------------|-----------------|
| `latest` | latest | latest (25) |
| `node20`, `node22`, `node24`, `node25` | latest | specified |
| `10` | latest 10.x | latest (25) |
| `10-node20`, `10-node22`, `10-node24`, `10-node25` | latest 10.x | specified |
| `10.32.1` | `10.32.1` | latest (25) |
| `10.32.1-node20`, `10.32.1-node22`, … | `10.32.1` | specified |

> **Latest Node** is currently Node.js **25**. Tags without a `-nodeXX` suffix always use this version.

### Example Usage

```bash
# Latest pnpm on latest Node.js
docker pull ghcr.io/yorukai/pnpm:latest

# Latest pnpm on a specific Node.js version
docker pull ghcr.io/yorukai/pnpm:node22

# Latest pnpm v10.x on Node.js 22
docker pull ghcr.io/yorukai/pnpm:10-node22

# Exact pnpm version on latest Node.js
docker pull ghcr.io/yorukai/pnpm:10.32.1

# Exact pnpm version on a specific Node.js version
docker pull ghcr.io/yorukai/pnpm:10.32.1-node22

docker run --rm ghcr.io/yorukai/pnpm:latest pnpm --version
```

## Workflow Overview

The GitHub Actions workflow:

1. Fetches the latest `pnpm` release tag from GitHub.
2. Runs a build matrix over all supported Node.js versions in parallel.
3. For each Node.js version: checks if the image already exists in GHCR (idempotent).
4. Builds the image and pushes all applicable tags (see table above).
5. For the designated **latest** Node.js version, also pushes the node-version-agnostic tags (`latest`, `10`, `10.32.1`).

## Supported Node.js Versions

Currently built for: **20, 22, 24, 25**

To add or remove versions, update the `matrix.node_version` list and `LATEST_NODE` env var in `.github/workflows/sync-pnpm-image.yml`.

## Contributing

Contributions are welcome! Submit issues or pull requests to improve the workflow, update dependencies, or enhance documentation.
