# MEOWMENTUM — Agent Context Sheet

Shared fact sheet for every `meow-*` agent. Read this before acting. If a fact you need
is not here, go and read the source document named beside it — do not invent it.

**Deliberately excluded from this file:** team member names, internal money figures,
Steam keys, and build artifacts. If a task seems to need one of those, stop and ask John.

---

## 0. The standing rule — no agent acts outward

Every `meow-*` agent **prepares, drafts, researches and recommends. None of them ship.**

Specifically, no agent may:

- publish or post anything to any platform (Steam, TikTok, YouTube, Reddit, Discord, X, Bluesky, Instagram, Kickstarter, speedrun.com)
- send an email to press, a creator, a publisher, a grant officer or a mailing list
- submit an application, a festival entry, a showcase form or a store update
- spend money, commit to a cost, or sign anything
- change the Steam store page, the Discord server, or any live account

Output goes to a file or to the chat, marked `READY FOR JOHN`. **John sends it, or it
does not go.** An agent that is unsure whether something counts as "outward" treats it
as outward.

---

## 1. The game

**Meowmentum** — first-person speedrunning platformer. You play a cat apprentice racing
to become a fully-fledged catmage. Wall-run, slide and dash through magic orbs to chain
momentum, hunt hidden shortcuts, and fight for a place on global leaderboards.

**One-line pitch (use this everywhere):**
> **You are a cat. You are late for wizard school. Go.**

**Comparables** — always pair one movement comp with one cat comp, never just one:
- Movement: *Neon White* (route optimisation), *Clustertruck* / *Karlson* (absurd first-person movement), *Trackmania* (leaderboards as an infinite loop), *Mirror's Edge* (the genre's grandfather)
- Cat: *Stray*, *Little Kitty, Big City*

**Never say again** (from `03_PRESS_KIT.md` part 1):
- "casual" — it is currently a Steam tag and it is bringing the wrong audience, who then leave difficulty-based negative reviews. **The tag has to go.**
- "wholesome cat game" on its own — hides the skill ceiling and puts the game in a category it loses in.
- "final student project" as the primary identity. Great *story*, bad *label*.

---

## 2. Status, as of October 2026

| Thing | Where it is |
|---|---|
| Steam page | Live, **Coming Soon**, Early Access, listed as "2026" |
| Demo | Live and free, **~20 reviews, 100% positive** |
| Discord | **~180 members** |
| Languages | **English only** |
| Platforms | **Windows only** |
| Award | **Best Student Project, 15th Unity Awards (2023)** |
| Mailing list | **Does not exist yet.** This is the biggest missing asset. |
| speedrun.com page | **Does not exist yet.** |

**The verdict that drives everything: the game is good, the marketing does not exist.**

---

## 3. The team and the company

- 8 people, **all part-time**.
- 4 active directors: **1 in Canada, 3 in Colombia.** Plus concept-art and sound-design collaborators.
- The company is **incorporated in Canada**.
- The studio is described publicly as based in Vancouver, working worldwide. That is accurate and it is what the website says.

**Why this matters more than it looks:** the residency split is what decides the whole
funding route (see section 6). It is a structural fact, not a detail.

**Anti-paralysis rule from the plan:** the Marketing Lead decides alone. Nothing in the
90-day plan goes to a vote of eight people. Consensus is what kills friends-team marketing plans.

---

## 4. The technical facts (confirmed by first-party audit — `code_audit/ARCHITECTURE_MAP.md`)

- **Unity 6000.3.9f1**
- **222 `.cs` files / 17,208 lines** under `Assets/Scripts`
- **Zero `.asmdef` under `Assets/Scripts`** — all first-party runtime code compiles into a single `Assembly-CSharp`
- **73 `Debug.Log*` calls**, **25 `TODO|HACK|FIXME` markers**
- **21 uncached `Camera.main` sites**, several inside `Update` / property getters
- Deprecated-API status is clean (Unity 6 forms everywhere, `linearVelocity`, Input System — one legacy `Input.GetKeyDown` site remains in `LevelSelectButton.cs`)
- Third-party in use: **FMOD**, Odin Inspector, DOTween, Cinemachine 3, Newtonsoft.Json, **Steamworks**, **Unity Gaming Services (Authentication / Leaderboards / Analytics)**, Feel, MeshBaker
- **Build-script mismatch:** the build script points at `Unity 2021.3.7f1` while `ProjectVersion.txt` says `6000.3.9f1` (`code_audit/BUILD_CONFIG_FINDINGS.md`)

**The game is single-player.** Online leaderboards come from Unity Gaming Services.
There is **no netcode, no Netcode for GameObjects, no Photon, no Mirror** anywhere in the
audit. Any agent proposing multiplayer work is out of scope until the code says otherwise.

**The engine is Unity.** This disqualifies Epic MegaGrants (UE5/UEFN only) — do not pitch it.

---

## 5. The numbers that decide things (`06_METRICAS.md`)

**North star: net wishlists per week.** Everything else is a diagnostic of that number.

> **Task zero, still open:** nobody has written down the current wishlist count from
> Steamworks, Wishlist Actions. Every target below recalibrates against it. Until that
> number exists, the team is flying blind.

Wishlist thresholds before an Early Access launch:

| Count | Meaning |
|---|---|
| < 2,000 | Invisible. Steam will not surface the game. |
| 5,000 | Bare minimum |
| **7,000–10,000** | Acceptable floor |
| 20,000+ | Popular Upcoming territory |
| 50,000+ | Real indie success |

**Stated goal: 25,000 wishlists before the Early Access launch.**

**Diagnostic A — store conversion** = wishlists divided by page visits:

| Result | Reading | Action |
|---|---|---|
| **< 5%** | The Steam page is broken | Redo capsule art, first trailer, short description. **Do not spend anything on traffic until it is fixed.** |
| 5–10% | Normal | Improvable — test new capsule art |
| **> 12%** | The page converts well | The problem is purely traffic. Push content and creators hard. |

This separates "nobody sees me" from "they see me and don't care". Two completely
different problems, and most indies work the wrong one.

**Capsule art test:** shrink it to 231×87 px. Can you tell it is a cat? Can you read the
name? Do you understand it is about speed? For a cat game the answer is almost always
**a cat's face, large, looking at the camera.**

**Leading indicator:** if outreach emails sent in a week are 0, net wishlists two weeks
later will be 0. It is the most reliable early signal the team has.

---

## 6. Funding reality — read this before researching a single grant

From `07_FINANCIACION.md` section 0-PRE, with the team's confirmed data:

**Today the team is not eligible for public money in either country.** Not for lack of
merit — for structure:

- **Canadian funds:** the entity is Canadian, but **3 of 4 directors are in Colombia**. CMF requires **75% or more of the project developed in Canada**; the BC tax credit is calculated on **BC payroll**. One person in four does not reach any threshold.
- **Colombian funds:** Crea Digital explicitly excludes *"personas jurídicas de origen extranjero, así estén radicadas en Colombia"*. The company is Canadian, so it is ineligible, with no discussion.
- **Epic MegaGrants:** requires UE5/UEFN. The game is Unity.

**So the money order is:**

| Priority | Source | Why |
|---|---|---|
| 1 | **Publishers and porting partners** | They don't ask where you live. They ask how many wishlists. |
| 2 | **Early Access revenue** | Same |
| 3 | **Kickstarter** | Same, and the IP stays with the team |
| 4 | **Awards and showcases with cash prizes** | Globally open |
| 5 | Private funds with no national gate — Kowloon Nights, Indie Fund | Open worldwide, very competitive |

**Two side doors that do exist** (both accept *natural persons*, so the Canadian-company
problem disappears):
- **Portafolio Nacional de Estímulos** (Ministerio de las Culturas, Colombia)
- **Programa Distrital de Estímulos (PDE), IDARTES, Bogotá**

A Colombian director can apply personally. 2026 cycles already closed; the target is
**~Q1 2027**. Confirm videogames is an eligible line in the specific call first.

**Open question worth the most:** **COVA** (Colombia Videogames Association) hands out GDC
scholarships and organises delegations. It is unconfirmed whether a team with a Canadian
company can access them. **Write and ask them directly.**

> **Hard line:** misrepresenting where work actually happens on a public-funding
> application is fraud. No agent drafts anything that blurs this.

---

## 7. The two superpowers

Everything strategic comes from these:

1. **It is a cat game.** Cats cross every audience on the internet. Cat content is the highest-click-through object there is.
2. **It is a speedrunning game with global leaderboards.** It manufactures its own content forever — clips, guides, wikis, races, world records. Precedent: Trackmania, Neon White, Clustertruck, Karlson.

**The real target for the second one: somebody runs Meowmentum at a Games Done Quick.**
That puts the game in front of hundreds of thousands of exactly the right people, with a
story, for free, and permanently on YouTube. It cannot be bought, only cultivated.

**Public shortcut policy** (should be written in the Discord):
> *"We don't patch movement exploits unless they break the game. If you find something weird, it's yours."*

That one sentence will win more runners than any email.

---

## 8. The content engine (`04_MOTOR_DE_CONTENIDO.md`)

Don't *do marketing* — **extract content from the game**. The chain is:

1. Player (or dev) runs a track
2. **"Export clip" button — development feature number one**
3. 9:16 MP4 with timer, world rank, @Meowmentum watermark
4. Posted unedited to TikTok / Shorts / Reels
5. Best ones collected in Discord #clips
6. Best of the month becomes one compiled YouTube video

**Marginal cost of content: zero.** If the button isn't built, the team is throwing away
its single biggest structural advantage.

**The 10 base formats** (rotate forever): world record · broken shortcut · **real cat vs
game split-screen (the winning format)** · fail compilation · impossible challenge ·
before/after · dev reacts · 10-second physics explainer · community cat · art timelapse.

**Form rules:** movement in the first 0–1s (never open on a logo) · 6–15s for run clips,
20–40s for explainers · on-screen text always · clean loop · **use the game's own OST and
cat SFX** (licensed audio on a brand account is a real takedown risk) · one CTA per week, not per post.

**The four rituals** that must run 12 weeks without failing: **World Record Wednesday ·
Shortcut Sunday · Devlog Friday · Cat of the Month.**

---

## 9. Calendar and the one irreversible decision

**Steam Next Fest: a game may enter exactly one, ever.** It does not create an audience,
it multiplies one. Entering with a ~180-person Discord spends the only bullet with a
half-empty magazine.

**Recommendation in the plan: February 2027 (22 Feb – 1 Mar), not October 2026.** That
means moving the Steam page from "2026" to **Early Access — Spring 2027**, and lands the
EA launch inside the hot 6–10 week window after the festival.

**Top 8 event fits** (`08_EVENTOS_Y_SHOWCASES.md`): IGF 2027 · Steam Next Fest Feb 2027 ·
Wholesome Direct 2027 (pitch **the cat**, not the skill) · gamescom Indie Arena Booth ·
BIG Festival / gamescom latam (direct advantage — three directors in Bogotá) ·
TGS Selected Indie 80 · The MIX · BitSummit.

Every submission window in that document is marked verified or pending. **Re-verify
before acting on any date** — several have already passed.

---

## 10. The 90-day plan in one paragraph (`01_PLAN_90_DIAS.md`)

Four objectives: unlock the money · build the email list from 0 to 1,500 · start the
content engine (4 rituals, 12 weeks, no misses) · seed the speedrun scene (speedrun.com
page + 25 active runners + 15 creator videos). Above all: **+6,000 net wishlists in the
quarter.**

The five structural things, if only five are possible:

1. Sort out the entity question
2. **The clip-export button** — turns every player into distribution
3. **The email list** — the only thing that converts into Kickstarter backers
4. **20 outreach emails a week, no exceptions**
5. **Pick the right Next Fest** — one shot, irreversible

The likeliest failure of the plan is not that it's wrong — it's that it gets abandoned in
week 5. Mitigations: batch everything, one written owner per task, 15-minute Monday
review (not a meeting), a planned rest week every 6 weeks, and **if something slips three
weeks running, delete it from the plan** and give the hour back to the 20 emails.

---

## 11. Source documents

| File | What's in it |
|---|---|
| `00_DIAGNOSTICO_Y_RUTA_DE_DINERO.md` | Diagnosis and the money route |
| `01_PLAN_90_DIAS.md` | The week-by-week plan, owners, budget |
| `02_KICKSTARTER_CAMPANA.md` | Campaign structure, rewards, timing, page copy |
| `03_PRESS_KIT.md` | Positioning, ready-to-copy English copy, 4 pitch emails, factsheet |
| `04_MOTOR_DE_CONTENIDO.md` | The content factory, 10 formats, 40 ideas, channel split |
| `05_CREADORES_Y_SPEEDRUN.md` | Runnability requirements, creator tiers, GDQ path |
| `06_METRICAS.md` | North star, weekly dashboard, the four diagnostics |
| `07_FINANCIACION.md` | Full funding research with eligibility gates |
| `08_EVENTOS_Y_SHOWCASES.md` | Global event calendar with verification marks |
| `EXECUTIVE_SUMMARY_EN.md` | English summary of the above |
| `code_audit/` | Architecture map, audit, build-config findings |
| `site/` | The marketing website source |

*Note: the strategy documents are written in Spanish, the working language of the person
who wrote them. The agents work in English because that is the language everything ships
in. Read the Spanish, write the English.*
