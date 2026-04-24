# Changelog

## 2026-04-24

- feat: Initial release of the `caniemail-for-agents` Claude Code skill, giving coding agents grep-friendly access to caniemail.com email-client compatibility data without loading the full 10,000-line upstream JSON into context.

- feat: Bundled a snapshot of caniemail.com data split into three agent-friendly artifacts — `index.md` (one line per feature for discovery), per-feature JSON files under `features/<slug>.json` (detail lookups), and a flat `support.tsv` table (cross-cutting queries like "everything Outlook 2019 breaks") — plus `nicenames.json` to map canonical keys to display names.

- feat: Added `scripts/build_index.py`, a stdlib-only Python 3.9+ script that fetches the upstream JSON and regenerates all bundled artifacts, so consumers never need to hit the network or run Python to use the skill.

- feat: Added a weekly GitHub Actions workflow (`.github/workflows/refresh-data.yml`) that rebuilds the data every Monday and opens a PR when caniemail.com has changed, keeping the `main` branch within a week of upstream.

- feat: Shipped a Claude Code plugin marketplace manifest (`.claude-plugin/marketplace.json`) so the skill can be installed via `/plugin marketplace add` in addition to manual git clone.
