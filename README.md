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

### Option A — `npx skills` (works across every Agent-Skills-compatible client)

```bash
npx skills add adpharm/caniemail-for-agents
```

Works on Claude Code, Cursor, VS Code / Copilot, Codex, Gemini CLI, Amp, Goose, and [every other client that supports the Agent Skills standard](https://agentskills.io). The CLI detects which agent you're using and installs to the right location.

### Option B — Claude Code plugin marketplace

```
/plugin marketplace add adpharm/caniemail-for-agents
/plugin install caniemail-for-agents@caniemail-for-agents
```

Native Claude Code plugin install. Gives you versioned updates via `/plugin marketplace update`.

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
caniemail-for-agents/                       # repo root (human-facing)
├── README.md
├── LICENSE
├── .claude-plugin/
│   ├── marketplace.json                    # marketplace manifest (this repo is a marketplace)
│   └── plugin.json                         # plugin manifest (this repo is the plugin)
├── .github/workflows/
│   └── refresh-data.yml                    # weekly cron → PR if caniemail changed
├── scripts/
│   └── build_index.py                      # repo tooling: fetch + split
└── skills/
    └── caniemail-for-agents/               # the skill inside the plugin
        ├── SKILL.md
        └── references/
            └── data/                       # generated output (checked in)
                ├── index.md
                ├── support.tsv
                ├── nicenames.json
                └── features/
                    └── <slug>.json         # 300+ files
```

The skill is nested under `skills/caniemail-for-agents/` so that `npx skills add adpharm/caniemail-for-agents` only pulls the skill directory — not the repo's `README`, `LICENSE`, or CI files. The generated data is checked in on purpose: consumers shouldn't need to run Python or hit the network to use the skill.

## Credits

All compatibility data comes from [caniemail.com](https://www.caniemail.com), maintained by [Rémi Parmentier](https://www.hteumeuleu.com/) and contributors. This project just reshapes their data for agents; credit and thanks for the underlying work go to them.

## License

[MIT](./LICENSE).
