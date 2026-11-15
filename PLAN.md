# 📋 Master Plan — Days 26–90

**Owner:** Darshak · **Repo:** python-foundations
**Status:** Day 25 complete. Day 26 starts Sun, Nov 15, 2026.
**Supersedes:** all earlier plan versions.

## Where I am (Day 25)
Live and working: FastAPI + PostgreSQL + Alembic + JWT/Argon2 (pwdlib) + Pytest (7 tests)
+ GitHub Actions CI/CD + Docker on Railway. RAG from scratch with page citations,
retry/backoff, per-user isolation. 4 Streamlit apps + portfolio.
**Missing:** React/Next.js/TypeScript, agents, Django, cloud, consistent DSA.

## Why this order (market data, Nov 2026)
- React/JS in ~67% of entry-level dev roles; nearly every "Full Stack" title. Agents ~15–20%.
- Entry-level = 16,000 of 130,000 active tech openings (~12%).
- IT services (76k) + GCCs (19k) lead volume; product/startup postings shrinking.
- Many mass fresher drives filter to 2024–26 batches. I'm 2022 → check eligibility first.
- WFO ≈ 12× remote. Salary cluster ₹3–8 LPA; ₹8–12 is the stretch.
- Half of all postings are <2 weeks old → apply early, apply now.

---

## ⚙️ Daily template (non-negotiable)

| Track | Time | What |
|---|---|---|
| Build | 3–4 hrs | The day's mission |
| DSA/SQL | 1–1.5 hrs | Topic per phase |
| Job search | 1–1.5 hrs | 3–5 tailored apps + 2 outreach, logged in tracker |
| Agents slot | 45 min | Fixed time, hard stop (see AGENTS.md) |
| Ship | 15 min | Commit + push + 3-line PROGRESS.md |

Bad day? **Cut build scope, never the job-search hour.**

---

## ⚛️ Phase 1 · React/Next.js/TypeScript (Days 26–33 · Nov 15–22)

Learn React *inside* Next.js — one framework, TS from the scaffold.
Goal: rebuild the Expense Tracker frontend against the live Railway backend.

| Day | Build (3–4 hrs) | 45-min slot |
|---|---|---|
| 26 | ES6+ crash course; `create-next-app --ts`; components/props/JSX → static dashboard | §3: write RAG context budget (chunks + history + question) |
| 27 | `useState`/`useEffect`/fetch; Login + Register → `/token`, `/register`; JWT in sessionStorage | §5: few-shot rewrite of categorizer prompt; test 5 inputs |
| 28 | Protected dashboard; list + total + add-expense with Bearer header | RAG: add `date`/`owner` to chunk metadata + write 10 test Q&As |
| 29 | Delete, AI Analyze button, loading/error states, Tailwind → Streamlit parity | §3: document 3 hallucination mitigations |
| 30 | **Flex:** TS types for API models/props, or catch up | Flex / rest |
| 31 | 401→login redirect, empty states, responsive polish | §4: Groq fallback in one function (or weak-query logging) |
| 32 | Deploy Vercel (`NEXT_PUBLIC_API_URL`); tighten Railway CORS to Vercel domain; test live | §6: sketch the agent (goal, tools, loop) for Day 34 |
| 33 | README + architecture diagram + 2-min Loom; update portfolio/resume/LinkedIn | §20: record 60-sec RAG demo; fold notes into resume |

**DSA:** arrays + hashing, 1–2 easy/day.
**Jobs:** 3–5/day. Start with Digitals AI GenAI Fresher (0–3 yrs), Finflock AI Full Stack
(₹8–12L), Internshala/Cutshort "no experience required" roles.

## 🤖 Phase 2 · Agents, hard-capped (Days 34–36 · Nov 23–25)

The main build **is** roadmap §6/7/8/11. Stop at Day 36 no matter what.

| Day | Build | Rider (inside the block) |
|---|---|---|
| 34 | LangChain: chat model, prompt template, Pydantic output parser; categorizer as a chain | §9: explicit conversation history |
| 35 | LangGraph agent: calculator + DB query + web search (Tavily free) | §7: DB tool is **read-only**; note why |
| 36 | `POST /agent/query` behind JWT; "Ask AI" tab if time; Pytest + README; resume += LangChain/LangGraph | §15: one "agent picked the right tool" test |

**DSA:** strings + two pointers. **Jobs:** add AI Application Developer titles.

## 🏭 Phase 3 · Production breadth (Days 37–40 · Nov 26–29)

| Day | Build | 45-min slot |
|---|---|---|
| 37 | Django polls tutorial 1–3; ORM/MTV vs SQLAlchemy/routers notes | §16: audit agent DB tool — scope to SELECT |
| 38 | DRF serializer + viewset mini-API; "FastAPI vs Django" answer. **⚠️ Railway decision: pay ~$5/mo or commit to migrate** | §16: prompt-injection test on own RAG + one fix |
| 39 | AWS: IAM/EC2/S3/RDS concepts; one real artifact (S3 page or EC2 Docker run) | §17: map stack vs infra list; gaps → Parking Lot |
| 40 | System design doc: Next.js→FastAPI→Postgres/Chroma→Gemini, JWT flow, scaling story. **Execute migration if chosen** | §18: token/cost logging; confirm backoff covers 429/503 |

**DSA:** sliding window + stacks. **Jobs:** batch-year eligibility check on every drive.

## 🧠 Phase 4 · Interview mode (Days 41–50 · Nov 30–Dec 9)

Build ≈ 2 hrs · DSA 2–3 hrs · apps 5/day · **2 mocks/week**.
Slot becomes Q&A drills: one AGENTS.md section → 3 questions, answered aloud.

| Day | DSA/SQL | Interview mission |
|---|---|---|
| 41 | Arrays/hashing medium | Pitch #1: Expense Tracker (2 min, recorded). Python: mutability, decorators, generators |
| 42 | Two pointers | Pitch #2: RAG. **Mock #1 technical** |
| 43 | Sliding window | Write + record 60-sec gap answer. FastAPI: DI, async, Pydantic |
| 44 | Stacks/queues + GROUP BY/HAVING | 3 STAR stories. **Mock #2 behavioral (gap included)** |
| 45 | Linked lists | Pitch #3: Agent. Postgres: indexes, transactions, why Alembic |
| 46 | Binary search + window functions | Auth: JWT vs sessions, hashing vs encryption, CORS. **Callback-rate checkpoint** |
| 47 | Revise 5 worst problems | Design mock: RAG for 100k users. **Mock #3** |
| 48 | SQL live queries | 90-min machine coding: "tags" feature (endpoint + migration + test). **Mock #4** |
| 49 | Timed set (3 in 60 min) | HR: why now, salary ₹3–8 LPA, relocation yes. Follow up all apps >7 days |
| 50 | **Buffer** | Re-record weakest pitch; tally metrics; evening off |

## 🚀 Phase 5 · Blitz (Days 51–60 · Dec 10–19)

8–12 apps/day · 1 DSA/day · mock every 2 days · slot drops to 15-min reads.

| Day | Mission |
|---|---|
| 51 | 10 apps: 4 SME/startup boards, 3 LinkedIn + referral ask, 2 eligible GCC/services, 1 QA/SDET fallback |
| 52 | 10 apps + 5 founder/EM DMs. LinkedIn post: Next.js flagship |
| 53 | 10 apps. **Mock #5.** Follow-ups |
| 54 | 10 apps. LinkedIn post: RAG demo. 2 alumni chat requests |
| 55 | **Iteration checkpoint:** <2 callbacks/50 apps → rewrite resume, broaden titles. 10 apps with new version |
| 56 | 10 apps. **Mock #6.** SQL revision |
| 57 | 10 apps. Referral push to every warm contact |
| 58 | 10 apps. **Click every live link** (Railway credit!). Fix anything dead |
| 59 | 10 apps. **Mock #7.** Pipeline review |
| 60 | Retro: apps/callbacks/interviews. Write next-30-day search plan. Celebrate 🎉 |

---

## 📦 Extension · Days 61–90 (Dec 20 – Jan 18)

Runs **only while applying**. ~3 hrs/day learning, rest on search.
Interviews pause it. Any offer ends it.

| Days | Module |
|---|---|
| 61–70 | **RAG v2:** 61–63 structural chunking + dedupe + hybrid BM25/vector · 64–65 cross-encoder reranker + top-k · 66–68 20-question eval (retrieval hit-rate + faithfulness measured separately) · 69–70 query rewriting + confidence-thresholded "I don't know" + clickable sources. Pick one real messy corpus on Day 61 |
| 71–75 | Agent eval: task-completion tests, LLM-as-judge, tracing |
| 76–80 | Redis + background jobs + SSE/WebSocket streaming |
| 81–84 | One MCP server exposing the expense API as tools |
| 85–90 | Project 4: SQL/Data-Analyst Agent over own Postgres |

**Skip until employed:** math/RL, multi-agent orchestration, the other 9 frameworks,
Kubernetes, vLLM, computer-use agents, sub-3s SLA, OCR, model routing,
embedding versioning, incremental re-indexing, answer caching.

---

## 📊 Weekly targets

| Metric | Target |
|---|---|
| Applications | 25–35/wk (P1–3), 35/wk (P4), ~60/wk (blitz) → **~200 by Day 60** |
| Outreach | 10+/wk personalized, portfolio link included |
| LinkedIn posts | 1/wk |
| DSA | ~60–70 problems + ~30 SQL by Day 60 |
| Mocks | 7–8 total |
| **The rule** | 50 apps, zero callbacks → change resume/targets, never "apply harder" |

## 🔒 Hard rules

1. Agents stop Day 36. Django stops Day 38. No new frameworks after Day 40.
2. Buffers: Day 30 and Day 50 — catch up, don't add features.
3. Railway: decide Day 38, verify links Day 58. Links never die during the blitz.
4. Every drive: batch-year check first. Channels = skills-first SMEs/startups, referrals, eligible GCC roles.
5. Relocation-open (Blr/Hyd/Pune/Chennai/NCR). Remote-only cuts the market ~12×.
6. 45-min slot: timer stops mid-sentence; overflow → Parking Lot in AGENTS.md.
7. **One in, one out. No new roadmaps until Day 40.** New lists get triaged, never added as tracks.
8. Interviews pause all learning. Any decent offer beats a finished checklist.
9. Job-search hour and DSA are untouchable.
10. Resume keywords now: FastAPI, PostgreSQL, Alembic, JWT, Pytest, GitHub Actions, Docker, RAG, ChromaDB, Gemini. After Day 33: React, Next.js, TypeScript. After Day 36: LangChain, LangGraph.

## ✅ Tonight (45 min, before Day 26)

1. Save `PLAN.md` + `AGENTS.md` in repo root. Link both from README.
2. Create the application tracker spreadsheet (company, role, date, channel, status, follow-up).
3. Resume v1 with current truthful stack + live links.
4. Apply to 3: Digitals AI, Finflock, one Internshala fresher listing.
5. Install Node.js. Block the 45-min slot on the calendar.

---

*Momentum beats intensity. Forward is the only direction we know. 🐋*