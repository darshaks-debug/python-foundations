# 🤖 AGENTS.md — Agents & RAG Roadmap Tracker

Companion to `PLAN.md`. This is the **45-minute daily slot**, not a second curriculum.

**Sources triaged into this file:**
- 20-section "AI Agents Developer Roadmap" (X, Nov 13 2026) → `docs/agents-roadmap.png`
- 30-item production-RAG checklist (X, Nov 14 2026)

## 🔒 Slot rules
- **45 min/day at [FILL YOUR TIME].** Timer on. Hard stop mid-sentence.
- Overflow → **Parking Lot**. Never eats the build block, DSA, or job-search hour.
- **One in, one out.** New roadmaps get triaged here, never added as tracks. No new lists until Day 40.
- Interviews pause this track. Any decent offer ends it.
- Ritual: 15 min read one subsection → 25 min touch my own code / write the answer → 5 min tick + log + commit (`agents: <topic>`).

---

## 📚 Section checklist (20-section roadmap)

| # | Section | Status | Scheduled |
|---|---|---|---|
| 1 | Programming Foundations | 🟡 ~80% done | JS/TS Days 26–33, DSA Days 41–50 |
| 2 | Math & AI Fundamentals | ⛔ SKIP | learn paid |
| 3 | Understanding LLMs | 🟡 ~50% done | Days 26, 29 |
| 4 | LLM APIs & Providers | 🟡 Gemini deep | Day 31 |
| 5 | Prompt & Context Engineering | 🟡 ~70% done | Days 27–28 |
| 6 | Agent Fundamentals | ⬜ scheduled | Days 32, 34 |
| 7 | Tool Use & Function Calling | ⬜ scheduled | Days 34–35 |
| 8 | Reasoning & Planning (ReAct) | ⬜ scheduled | Day 35 |
| 9 | Agent Memory | 🟡 ~50% done | Day 34 |
| 10 | RAG | 🟡 ~70% done | eval → Parking Lot |
| 11 | Agent Frameworks | ⬜ LangChain/LangGraph ONLY | Days 34–36 |
| 12 | Multi-Agent Systems | ⛔ SKIP | learn paid |
| 13 | MCP | 🅿️ PARKED | Days 81–84 |
| 14 | Advanced Capabilities | ⛔ SKIP | learn paid |
| 15 | Agent Evaluation & Testing | 🟡 Pytest done | Day 36 + Days 71–75 |
| 16 | Security & Safety | 🟡 secrets/JWT done | Days 37–38 |
| 17 | Infrastructure & Deployment | 🟡 ~70% done | Day 39 + Days 76–80 |
| 18 | Performance & Cost | 🟡 retry done | Day 40 |
| 19 | Real-World Projects | 🟡 3 of 14 built | agent Day 35, SQL agent Days 85–90 |
| 20 | Career & Professional Growth | ✅ running | job-search track, daily |

Legend: ✅ done · 🟡 partial · ⬜ scheduled · 🅿️ parked · ⛔ skip until employed

---

## 🗓️ Daily slot schedule

### Phase 1 · Days 26–33 (React is the main event)
- **26** — §3: write my RAG's actual context budget (chunks + history + question, in tokens)
- **27** — §5: rewrite categorizer prompt with one few-shot example; test 5 inputs
- **28** — RAG: add `date` + `owner` to chunk metadata (15m) + write 10 test Q&As (30m) → seeds Day 66 eval
- **29** — §3: document my 3 hallucination mitigations (grounding, citations, "not in docs" fallback)
- **30** — FLEX: catch up a missed slot, or rest
- **31** — §4: Groq free-tier fallback in one function. If short on time: weak-query logging instead (other → Parking Lot)
- **32** — §6: sketch the Day-34 agent on paper — goal, tools, loop, stop condition
- **33** — §20: record 60-sec RAG demo answering a hard question; fold slot notes into resume keywords

### Phase 2 · Days 34–36 (riders inside the main build, no extra slot)
- **34** — §9: give the agent explicit conversation history
- **35** — §7: DB tool must be read-only; write one line on why
- **36** — §15: one "agent picked the right tool" test case

### Phase 3 · Days 37–40
- **37** — §16: audit the agent's DB tool — can it run DELETE? Scope to SELECT
- **38** — §16: feed my RAG a PDF containing "ignore previous instructions"; log what happens + one fix
- **39** — §17: map my stack vs the infra list; mark gaps (Redis, queues, WebSockets) → Parking Lot
- **40** — §18: token/cost logging on one endpoint; confirm backoff covers 429/503; write the cost answer

### Phase 4 · Days 41–50
Slot = **Q&A drill**. One completed section → 3 interview questions, answered out loud from this file.

### Phase 5 · Days 51–60
Drop to **15 min/day**: one subsection read, no building. One LinkedIn post about the agent.

---

## 🔍 RAG checklist audit (30 items)

### ✅ Already done (~10)
Page-level citations · "I don't know" fallback · metadata source+page · per-user isolation
(Day 25) · chunk overlap + word boundaries · retry/backoff · embeddings persisted to disk ·
live deploy · GitHub + README · resume bullets

### 🎯 High-ROI upgrades (~10) → RAG v2, Days 61–70
Chunk by structure (mine is fixed 500-char) · dedupe before embedding · hybrid BM25+vector ·
cross-encoder reranker · query rewriting · tune top-k · test set + separate retrieval/generation
eval · log weak/failed queries · clickable sources UI · 60-sec hard-question demo (Day 33)

### ⏸️ Deferred (~10) — learn paid
Permissions at retrieval (session isolation is the fresher-appropriate version) ·
incremental re-indexing · stale-doc expiry · embedding/prompt versioning · small-model routing ·
sub-3-second SLA · OCR/tables/scanned PDFs · answer caching

**Framing upgrade for Day 61:** point the RAG app at ONE real messy corpus
(RBI circulars, university regulations, company policy docs) instead of random PDFs.

---

## 🅿️ Parking Lot (post-Day-60, priority order)

1. **RAG v2** — structural chunking, dedupe, hybrid search, reranker, eval harness (Days 61–70)
2. **Agent eval** — task-completion tests, LLM-as-judge, tracing (Days 71–75)
3. **Redis + background jobs + streaming** (Days 76–80)
4. **One MCP server** exposing the expense API as tools (Days 81–84)
5. **SQL/Data-Analyst Agent** over my own Postgres (Days 85–90)

**Overflow from daily slots lands here:**
- [ ] (add items as they overflow)

---

## 📓 Daily log

- Day 26:
- Day 27:
- Day 28:
- Day 29:
- Day 30:
- Day 31:
- Day 32:
- Day 33:
- Day 34:
- Day 35:
- Day 36:
- Day 37:
- Day 38:
- Day 39:
- Day 40:

---

## 🎤 Interview answers (my own words, one per completed section)

### §3 — LLM fundamentals
- Context budget of my RAG app:
- 3 hallucination mitigations I actually implemented:

### §5 — Prompt & context engineering
- How I force structured JSON output:
- Few-shot example that improved categorization:

### §4 — Providers
- How my fallback works / would work:

### §6/7/8 — Agents, tools, reasoning
- Agent vs chain vs automation:
- My agent's tools and stop condition:
- Why the DB tool is read-only:

### §10 — RAG
- Draw the pipeline (ingest → chunk → embed → store → retrieve → prompt → generate):
- Why chunk overlap:
- Top-k trade-off:

### §16 — Security
- What happened when I injected "ignore previous instructions":
- How I scope tool permissions:

### §17 — Infrastructure
- My stack vs the production list; what's missing and why it's deferred:

### §18 — Cost
- Token/cost per request; how backoff handles 429/503:

---

*The roadmap works for the job search, not the other way around. 🐋*