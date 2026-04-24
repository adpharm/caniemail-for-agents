# caniemail-for-agents

A [Claude Code skill](https://docs.claude.com/en/docs/claude-code/skills) that gives coding agents fast, grep-friendly access to email-client compatibility data from [caniemail.com](https://www.caniemail.com).

Built for people who write HTML email with an agent in the loop (Claude Code, Cursor, etc.) and want the agent to actually *know* what breaks in Outlook before suggesting it.

## Why

caniemail.com publishes its data as a single JSON file — ~10,000 lines, deeply nested. That shape is great for a web UI, but it's the wrong shape for an agent:

- Too large to load into context wholesale.
- Grep-hostile: the per-client support matrix is nested three levels deep.
- No natural "index" for feature discovery from a human word like "flexbox".

This repo ships a tiny Python script that downloads the JSON and splits it into three agent-friendly artifacts:

- **`index.md`** — one line per feature (`slug — title — category — keywords`), for discovery.
- **`features/<slug>.json`** — one small file per feature, for detail lookups.
- **`support.tsv`** — a flat `slug | client | platform | version | support | notes` table, for cross-cutting queries ("everything Outlook 2019 breaks").

Plus a `SKILL.md` that teaches the agent the three query patterns.

## Install

### Option A — Claude Code plugin marketplace (recommended)

```
/plugin marketplace add adpharm/caniemail-for-agents
/plugin install caniemail-for-agents@caniemail-for-agents
```

### Option B — manual git clone

```bash
# per-user (available in every project)
git clone https://github.com/adpharm/caniemail-for-agents ~/.claude/skills/caniemail-for-agents

# or per-project (scoped to one repo)
git clone https://github.com/adpharm/caniemail-for-agents .claude/skills/caniemail-for-agents
```

Either way, the skill triggers automatically when the agent is working on HTML email and a compatibility question comes up.

## Example triggers

- "does Outlook 2019 support `accent-color`?"
- "will this flexbox layout break in Gmail mobile?"
- "what email clients don't render AMP?"
- "I'm about to ship this template — anything that won't render in Apple Mail 15?"

The agent greps the bundled index, reads the relevant per-feature file, and answers with a snapshot date attached so you know how fresh the data is.

## Refreshing the data

The snapshot date is at the top of `references/data/index.md`. A GitHub Actions workflow (`.github/workflows/refresh-data.yml`) rebuilds the data every Monday and opens a PR if anything changed — so if you're consuming the `main` branch, you'll generally be within a week of upstream.

To rebuild locally:

```bash
python scripts/build_index.py
```

Python 3.9+, stdlib only. No dependencies.

## Repo layout

```
caniemail-for-agents/
├── SKILL.md                           # what the agent reads
├── README.md                          # this file
├── LICENSE                            # MIT
├── .claude-plugin/
│   └── marketplace.json               # Claude Code plugin marketplace manifest
├── .github/workflows/
│   └── refresh-data.yml               # weekly cron → PR if caniemail changed
├── scripts/
│   └── build_index.py                 # fetch + split
└── references/
    └── data/                          # generated output (checked in)
        ├── index.md
        ├── support.tsv
        ├── nicenames.json
        └── features/
            └── <slug>.json            # 300+ files
```

The generated output is checked in on purpose — consumers shouldn't need to run Python or hit the network to use the skill.

## Credits

All compatibility data comes from [caniemail.com](https://www.caniemail.com), maintained by [Rémi Parmentier](https://www.hteumeuleu.com/) and contributors. This project just reshapes their data for agents; credit and thanks for the underlying work go to them.

## License

[MIT](./LICENSE).
