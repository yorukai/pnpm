#!/usr/bin/env python3
"""Renders README.md from templates/README.md.

Usage: scripts/update-readme.py [pnpm_version]   (defaults to the latest pnpm release)
"""
import json
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


REGISTRY = "https://ghcr.io/v2/yorukai/pnpm"
MANIFEST_TYPES = ", ".join([
    "application/vnd.oci.image.index.v1+json",
    "application/vnd.oci.image.manifest.v1+json",
    "application/vnd.docker.distribution.manifest.list.v2+json",
    "application/vnd.docker.distribution.manifest.v2+json",
])


def fetch(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": "pnpm-image-readme", **(headers or {})})
    with urllib.request.urlopen(req) as res:
        return json.load(res)


def active(value, today):
    return value is not False and value is not None and (value is True or value <= today)


def status(cycle, today):
    if active(cycle["eol"], today):
        return "EOL"
    if active(cycle["lts"], today):
        return "LTS"
    return "Current"


def image_node_versions():
    """Maps Node.js cycle -> full version for every nodeN tag published on GHCR."""
    token = fetch("https://ghcr.io/token?scope=repository:yorukai/pnpm:pull")["token"]
    auth = {"Authorization": f"Bearer {token}"}
    tags = fetch(f"{REGISTRY}/tags/list?n=1000", auth)["tags"]
    versions = {}
    for tag in tags:
        m = re.fullmatch(r"node(\d+)", tag)
        if not m:
            continue
        manifest = fetch(f"{REGISTRY}/manifests/{tag}", {**auth, "Accept": MANIFEST_TYPES})
        if "manifests" in manifest:
            entry = next(
                x for x in manifest["manifests"]
                if x.get("platform", {}).get("os") == "linux" and x["platform"].get("architecture") == "amd64"
            )
            manifest = fetch(f"{REGISTRY}/manifests/{entry['digest']}", {**auth, "Accept": MANIFEST_TYPES})
        config = fetch(f"{REGISTRY}/blobs/{manifest['config']['digest']}", auth)
        env = {k: v for k, _, v in (e.partition("=") for e in config["config"]["Env"])}
        versions[m.group(1)] = env["NODE_VERSION"]
    return versions


today = date.today().isoformat()
pnpm = sys.argv[1] if len(sys.argv) > 1 else fetch("https://api.github.com/repos/pnpm/pnpm/releases/latest")["tag_name"]
pnpm = pnpm.lstrip("v")

api = {c["cycle"]: c for c in fetch("https://endoflife.date/api/nodejs.json")}
built = image_node_versions()
cycles = sorted(built, key=lambda c: -int(c))
supported = [c for c in cycles if c in api and not active(api[c]["eol"], today)]
lts = [c for c in supported if status(api[c], today) == "LTS"]
example = (lts or supported or cycles)[0]

rows = ["| Node.js (cycle) | Latest | Status |", "|-----------------|--------|--------|"]
for cycle in sorted(set(api) | set(built), key=lambda c: -int(c)):
    if int(cycle) < 20:
        continue
    latest = built.get(cycle) or api[cycle]["latest"]
    if cycle not in api or active(api[cycle]["eol"], today):
        label, color = "EOL", "red"
    elif cycle == supported[0]:
        label, color = ("LTS" if status(api[cycle], today) == "LTS" else "Current"), "blue"
    else:
        label, color = status(api[cycle], today), "lightgrey"
    badge = f"![{label}](https://img.shields.io/badge/{label}-{color})"
    rows.append(f"| {cycle} | {latest} | {badge} |")

values = {
    "NODE_VERSIONS": ", ".join(reversed(supported)),
    "EXAMPLE_NODE": example,
    "PNPM_VERSION": pnpm,
    "PNPM_MAJOR": pnpm.split(".")[0],
    "NODE_TABLE": "\n".join(rows),
}

text = (ROOT / "templates" / "README.md").read_text()
text = re.sub(r"{{(\w+)}}", lambda m: values[m.group(1)], text)
(ROOT / "README.md").write_text(text)
