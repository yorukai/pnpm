# pnpm Docker Image Sync

This repository automatically builds and publishes Docker images for the latest [pnpm](https://pnpm.io/) release using GitHub Actions. Images are based on Node.js (Debian and Alpine) and built for multiple Node.js versions.

## Features

- Automatically detects the latest `pnpm` release.
- Builds images for multiple Node.js versions in parallel (22, 24, 26).
- Publishes a comprehensive set of tags covering every pnpm × Node.js combination.
- Scheduled daily updates via GitHub Actions.

## Docker Image

- Registry: `ghcr.io/yorukai/pnpm`
- Two variants per Node.js version: Debian (default) and Alpine (`-alpine` suffix).

### Tag Reference

| Tag | pnpm version | Node.js version | Base |
|-----|-------------|-----------------|------|
| `latest` | latest | newest | Debian |
| `latest-alpine` | latest | newest | Alpine |
| `node26` / `node26-alpine` | latest | specified | Debian / Alpine |
| `12-node26` / `12-node26-alpine` | latest 12.x | specified | Debian / Alpine |
| `12.18.0-node26` / `12.18.0-node26-alpine` | `12.18.0` | specified | Debian / Alpine |
| `12`, `12.18.0` (+ `-alpine`) | latest 12.x / exact | newest | Debian / Alpine |

### Example Usage

```bash
docker pull ghcr.io/yorukai/pnpm:latest
docker pull ghcr.io/yorukai/pnpm:node26-alpine
docker pull ghcr.io/yorukai/pnpm:12-node26
docker pull ghcr.io/yorukai/pnpm:12.18.0-alpine
```

## Workflow Overview

1. Fetches the latest `pnpm` release tag from GitHub.
2. Fetches all non-EOL Node.js versions from <https://endoflife.date/api/nodejs.json>.
3. Builds Debian and Alpine images for each Node.js version in parallel (skipped if all tags already exist).
4. The newest Node.js version additionally gets the version-only tags (`latest`, `12`, `12.18.0`, and `-alpine` variants).
5. Renders `README.md` from `templates/README.md` via `scripts/update-readme.py` and commits it.

## Supported Node.js Versions

Built for every non-EOL Node.js version (22, 24, 26).

| Node.js (cycle) | Latest | Status |
|-----------------|--------|--------|
| 26 | 26.13.0 | ![LTS](https://img.shields.io/badge/LTS-blue) |
| 25 | 25.9.0 | ![EOL](https://img.shields.io/badge/EOL-red) |
| 24 | 24.22.2 | ![LTS](https://img.shields.io/badge/LTS-lightgrey) |
| 23 | 23.11.1 | ![EOL](https://img.shields.io/badge/EOL-red) |
| 22 | 22.23.4 | ![LTS](https://img.shields.io/badge/LTS-lightgrey) |
| 21 | 21.7.3 | ![EOL](https://img.shields.io/badge/EOL-red) |
| 20 | 20.20.2 | ![EOL](https://img.shields.io/badge/EOL-red) |

## Migrating old tags

`scripts/migrate-alpine-tags.sh [--dry-run]` re-tags previously published Alpine images (e.g. `26` → `26-alpine`). Run it once before the first Debian build.

## Contributing

Contributions are welcome! Submit issues or pull requests to improve the workflow, update dependencies, or enhance documentation.
