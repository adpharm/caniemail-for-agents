---
name: caniemail-for-agents
description: Look up email client compatibility for HTML/CSS/feature support using a bundled, grep-friendly snapshot of caniemail.com data. Use this skill whenever the user is writing, reviewing, or debugging HTML email and any question of "will this work in [client]?" comes up — e.g. "does Outlook 2019 support accent-color?", "what clients break flexbox?", "can I use AMP in Gmail?", "which Apple Mail versions render dark mode?". Also trigger proactively when reviewing an email template before shipping, when the user mentions an email client and a CSS/HTML feature in the same sentence, or when suggesting a technique that might not work everywhere. The data is a point-in-time snapshot — always cite the snapshot date in your answer so the user can judge staleness.
---

# caniemail-for-agents

A pre-split, grep-friendly mirror of [caniemail.com](https://www.caniemail.com) compatibility data, shipped under `references/data/`. Use it to answer email client compatibility questions without making a network call or parsing a 10,000-line JSON blob.

## Files

All paths are relative to this skill's directory.

- `references/data/index.md` — one line per feature (`slug — title — category — keywords`). Start here when the user names a feature but you don't know its slug.
- `references/data/features/<slug>.json` — full compatibility matrix for one feature, plus description, test URL, last-tested date, and footnotes. Small files, safe to read whole.
- `references/data/support.tsv` — flat table with columns `slug`, `client`, `platform`, `version`, `support`, `notes`. Use for cross-cutting queries ("everything unsupported in Outlook 2019").
- `references/data/nicenames.json` — canonical keys → display names. The user will say "Outlook"; the data keys it as `outlook`. Check here if a client or platform key doesn't match what you expect.

## Query patterns

### 1. User names a feature — find the slug

```
grep -i flex references/data/index.md
```

The keywords column covers aliases (e.g. `flexbox` is in the keywords for several `css-*` slugs), so grep on the human word, not the slug.

### 2. User asks "does X support Y?" — read the feature file

Once you have the slug:

```
cat references/data/features/css-accent-color.json
```

Each file is small (one feature's matrix). The `notes_by_num` field explains footnotes referenced by `#1`, `#2`, etc. in the support codes — read them when a support value has a footnote.

### 3. Cross-cutting question — grep the TSV

"What does Outlook 2019 break?":

```
awk -F'\t' '$2=="outlook" && $3=="windows" && $4=="2019" && $5=="n"' references/data/support.tsv
```

"Every client that doesn't support `accent-color`":

```
awk -F'\t' '$1=="css-accent-color" && $5=="n"' references/data/support.tsv
```

Prefer `awk -F'\t'` over `grep` when matching column values — grep can false-match across columns.

## Support codes

- `y` = supported
- `n` = not supported
- `a` = partially supported (mitigated)
- `u` = support unknown

If the TSV `notes` column has a number (e.g. `1`), look it up in the feature file's `notes_by_num`. Footnotes commonly flag things like "supported but only in certain browsers" or "renders but with visual bugs" — don't ignore them.

## Freshness

The top of `index.md` shows the snapshot date. **Cite it in your answer** ("as of <date>, Outlook 2019 does not support flexbox…") so the user can judge whether a refresh is warranted — caniemail gets updated when new client versions ship, and your bundled copy may lag.

Do *not* auto-refresh. The user rebuilds when they want fresh data:

```
python scripts/build_index.py
```

If the user asks about a very new feature or client version and your answer is "unknown / not in data", flag the snapshot age and suggest a rebuild — don't guess.

## Outlook on Windows is the hard case

In practice, Outlook for Windows (versions 2007 through 2021) uses Microsoft Word as its rendering engine. That engine ignores large swaths of modern CSS — flexbox, grid, animations, most pseudo-classes, CSS variables in many places, and more. Scan `support.tsv` for rows matching `outlook\twindows` and you'll see long stretches of `n` across modern CSS. This makes Outlook-on-Windows the effective floor for what's "safe" in HTML email, and it's almost always the client that determines whether a feature can ship.

How to apply that:

- If the user **names** their target clients, answer for those and don't over-editorialize. If Outlook Windows isn't on the list, don't force it into the answer.
- If the user asks "is X safe for email?" **without naming targets**, check Outlook Windows first. That's usually the answer.
- When Outlook Windows is the only thing breaking a feature and every other client is green, say so plainly. The user can decide whether they're willing to eat that trade — that's a common and legitimate choice for modern-audience campaigns.
- Don't preface every answer with Outlook caveats when the user only asked about, say, Gmail. Answer the question they asked.

## Answering style

- Be specific about client + platform + version. "Gmail" is ambiguous; `gmail / desktop-webmail / 2023-01` is not.
- When a feature has partial support (`a`), say so and point at the footnote rather than rounding to yes/no.
- If the user is about to ship an email template with a feature that breaks in a client on their target list, say it before they ask.
