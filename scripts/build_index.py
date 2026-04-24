#!/usr/bin/env python3
"""Fetch caniemail.com data and split it into agent-friendly files.

Outputs (under references/data/):
    index.md            one line per feature for discovery
    features/<slug>.json    one small file per feature for detail lookups
    support.tsv         flat compat table for cross-cutting greps
    nicenames.json      canonical key -> display-name map

Python 3.9+, stdlib only.
"""

import json
import sys
import urllib.request
from pathlib import Path

DATA_URL = "https://www.caniemail.com/api/data.json"


def main() -> None:
    out_dir = (
        Path(__file__).resolve().parent.parent
        / "skills"
        / "caniemail-for-agents"
        / "references"
        / "data"
    )
    features_dir = out_dir / "features"
    features_dir.mkdir(parents=True, exist_ok=True)

    # Wipe previous feature files so deleted slugs don't linger.
    for p in features_dir.glob("*.json"):
        p.unlink()

    print(f"Fetching {DATA_URL}...", file=sys.stderr)
    with urllib.request.urlopen(DATA_URL) as resp:
        data = json.load(resp)

    api_version = data["api_version"]
    last_update = data["last_update_date"]
    features = data["data"]
    nicenames = data["nicenames"]

    print(
        f"Got {len(features)} features (api v{api_version}, updated {last_update})",
        file=sys.stderr,
    )

    for feature in features:
        slug = feature["slug"]
        with (features_dir / f"{slug}.json").open("w", encoding="utf-8") as f:
            json.dump(feature, f, indent=2, ensure_ascii=False)

    index_lines = [
        "# caniemail feature index",
        "",
        f"Snapshot: {last_update} (api v{api_version})",
        f"Total features: {len(features)}",
        "Rebuild: `python scripts/build_index.py`",
        "",
        "Format: `<slug> — <title> (<category>) — <keywords>`",
        "Full detail per feature is in `features/<slug>.json`.",
        "",
    ]
    for feature in sorted(features, key=lambda f: f["slug"]):
        slug = feature["slug"]
        title = feature["title"]
        category = feature["category"]
        keywords = feature.get("keywords") or ""
        index_lines.append(f"- `{slug}` — {title} ({category}) — {keywords}")

    (out_dir / "index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    tsv_lines = ["slug\tclient\tplatform\tversion\tsupport\tnotes"]
    for feature in features:
        slug = feature["slug"]
        stats = feature.get("stats") or {}
        for client, platforms in stats.items():
            for platform, versions in platforms.items():
                for version, raw_support in versions.items():
                    # raw_support looks like "y", "n", "a", "u", or "y #1 #2"
                    parts = raw_support.split()
                    code = parts[0] if parts else ""
                    notes = " ".join(p.lstrip("#") for p in parts[1:])
                    tsv_lines.append(
                        f"{slug}\t{client}\t{platform}\t{version}\t{code}\t{notes}"
                    )

    (out_dir / "support.tsv").write_text(
        "\n".join(tsv_lines) + "\n", encoding="utf-8"
    )

    with (out_dir / "nicenames.json").open("w", encoding="utf-8") as f:
        json.dump(nicenames, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(features)} features to {features_dir}", file=sys.stderr)
    print(f"Index:   {out_dir / 'index.md'}", file=sys.stderr)
    print(f"TSV:     {out_dir / 'support.tsv'} ({len(tsv_lines) - 1} rows)", file=sys.stderr)
    print(f"Nicenames: {out_dir / 'nicenames.json'}", file=sys.stderr)


if __name__ == "__main__":
    main()
