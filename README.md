# Meowmentum — Claude Code agent team

Orphan branch. Nothing here shares history with `main`.

Eleven `meow-*` subagents for **Meowmentum**, a first-person speedrunning platformer, plus
the shared context sheet they all read first. Adapted from
[msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) and rewritten
around this project's real situation.

## Install

Copy `agents/` into the project's `.claude/agents/`:

```bash
cp agents/*.md /path/to/project/.claude/agents/
```

Claude Code picks them up by filename. `CONTEXTO.md` is not an agent — it is the shared
fact sheet every agent is told to read first, and it lives beside them.

## The team

| Agent | Owns |
|---|---|
| `meow-producer` | The 90-day plan, weekly owners, the Monday review, forcing decisions to be written |
| `meow-steam-page` | The store page as a conversion surface: capsule art, tags, copy, the conversion diagnostic |
| `meow-content-engine` | TikTok / Shorts / Reels factory, the monthly YouTube devlog, the four weekly rituals |
| `meow-community` | Discord, speedrun.com, tournaments, Reddit, recruiting the first runners |
| `meow-outreach` | The creator / press / publisher list and every pitch email. 20 a week, no exceptions |
| `meow-email` | The mailing list from zero. Gates the Kickstarter at 1,500 subscribers |
| `meow-funding` | Eligibility, the master dossier, publishers, awards, Kickstarter structure |
| `meow-unity-engineer` | Clip export, ghost replays, autosplitter, telemetry, closing the code-audit findings |
| `meow-speedrun-designer` | Track design, route depth, shortcut policy, leaderboard categories |
| `meow-localization` | String inventory, engineering readiness, language order, LQA |
| `meow-reality-checker` | The last gate. Default verdict NEEDS WORK until the evidence arrives |

## The rule they all share

**No agent acts outward.** None of them publish, post, email press, submit an
application, change a live account, or spend money. They prepare, draft and verify, and
mark the result `READY FOR JOHN`. A human sends it, or it does not go.

## Deliberately excluded

Team member names, internal money figures, Steam keys, and build artifacts are kept out
of every file here, including the context sheet.
