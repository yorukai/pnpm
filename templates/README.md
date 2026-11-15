# pnpm Docker Image Sync

This repository automatically builds and publishes Docker images for the latest [pnpm](https://pnpm.io/) release using GitHub Actions. Images are based on Node.js (Debian and Alpine) and built for multiple Node.js versions.

## Features

- Automatically detects the latest `pnpm` release.
- Builds images for multiple Node.js versions in parallel ({{NODE_VERSIONS}}).
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
| `node{{EXAMPLE_NODE}}` / `node{{EXAMPLE_NODE}}-alpine` | latest | specified | Debian / Alpine |
| `{{PNPM_MAJOR}}-node{{EXAMPLE_NODE}}` / `{{PNPM_MAJOR}}-node{{EXAMPLE_NODE}}-alpine` | latest {{PNPM_MAJOR}}.x | specified | Debian / Alpine |
| `{{PNPM_VERSION}}-node{{EXAMPLE_NODE}}` / `{{PNPM_VERSION}}-node{{EXAMPLE_NODE}}-alpine` | `{{PNPM_VERSION}}` | specified | Debian / Alpine |
| `{{PNPM_MAJOR}}`, `{{PNPM_VERSION}}` (+ `-alpine`) | latest {{PNPM_MAJOR}}.x / exact | newest | Debian / Alpine |

### Example Usage

```bash
docker pull ghcr.io/yorukai/pnpm:latest
docker pull ghcr.io/yorukai/pnpm:node{{EXAMPLE_NODE}}-alpine
docker pull ghcr.io/yorukai/pnpm:{{PNPM_MAJOR}}-node{{EXAMPLE_NODE}}
docker pull ghcr.io/yorukai/pnpm:{{PNPM_VERSION}}-alpine
```

## Workflow Overview

1. Fetches the latest `pnpm` release tag from GitHub.
2. Fetches all non-EOL Node.js versions from <https://endoflife.date/api/nodejs.json>.
3. Builds Debian and Alpine images for each Node.js version in parallel (skipped if all tags already exist).
4. The newest Node.js version additionally gets the version-only tags (`latest`, `{{PNPM_MAJOR}}`, `{{PNPM_VERSION}}`, and `-alpine` variants).
5. Renders `README.md` from `templates/README.md` via `scripts/update-readme.py` and commits it.

## Supported Node.js Versions

Built for every non-EOL Node.js version ({{NODE_VERSIONS}}).

{{NODE_TABLE}}

## Migrating old tags

`scripts/migrate-alpine-tags.sh [--dry-run]` re-tags previously published Alpine images (e.g. `{{EXAMPLE_NODE}}` → `{{EXAMPLE_NODE}}-alpine`). Run it once before the first Debian build.

## Contributing

Contributions are welcome! Submit issues or pull requests to improve the workflow, update dependencies, or enhance documentation.
