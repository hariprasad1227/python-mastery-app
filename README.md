# Python Mastery · Production Platform

An interactive, production-ready Python learning platform featuring:
- **FastAPI Progression & Security Backend**
- **Isolated Python Execution Sandbox** (Subprocess with AST security & 3.0s timeout limits)
- **Socratic AI Mentor Feedback** (OpenAI API integration with offline heuristic fallbacks)
- **Supabase PostgreSQL Schema with Row-Level Security (RLS)**
- **Next.js & Standalone Interactive Classroom Web App**

---

## Architecture

| Component | Technology | Responsibility |
|---|---|---|
| **Frontend** | Next.js 14 / React & Standalone Web App | Responsive UI, interactive Monaco/CodeMirror editor, test console, AI mentor drawer |
| **Backend** | FastAPI (Python 3.13) | REST API, progression engine, XP/streak rules, auth tokens, AI mentor proxy |
| **Database** | PostgreSQL (Supabase) | Profiles, modules, lessons, challenges, user_progress, submissions, badges |
| **Auth** | Supabase Auth | Email/password, verification, JWT session tokens, RLS enforcement |
| **Python Runner** | Isolated Sandbox Subprocess | AST security analyzer, hard wall-clock timeouts (3.0s), restricted namespace |
| **AI Mentor** | OpenAI API via FastAPI | Socratic hints (nudge, syntax clue, step breakdown); secrets never touch browser |
| **Deployment** | Vercel + Render/Railway + Supabase | Scalable, independent cloud microservices |

---

## Directory Structure

```
python-mastery/
├── database/
│   ├── schema.sql              # Complete PostgreSQL DDL with RLS policies and auth triggers
│   └── seed_lessons.sql        # Seed curriculum for Levels 1–5 with test cases and hints
├── runner/
│   ├── security.py             # AST inspector blocking os, sys, subprocess, eval, open, etc.
│   ├── test_harness.py         # Subprocess harness running user functions against test cases
│   ├── runner.py               # Orchestrator with timeout enforcement (3.0s) and crash recovery
│   └── test_runner.py          # Automated verification tests for the sandbox
├── backend/
│   ├── app/
│   │   ├── api/                # REST endpoints (/runner/execute, /progression, /mentor)
│   │   ├── core/config.py      # App settings and environment variables
│   │   ├── schemas/            # Pydantic models for runner, progression, and mentor
│   │   ├── services/           # Progression calculation, sandbox client, AI mentor
│   │   └── main.py             # FastAPI app entry point with CORS
│   ├── tests/
│   │   └── test_api.py         # Integration tests for FastAPI endpoints
│   ├── requirements.txt        # Backend dependencies
│   └── .env.example            # Environment variables template
├── frontend/
│   ├── src/app/page.tsx        # Next.js learner dashboard
│   ├── src/lib/api.ts          # TypeScript API client
│   ├── index.html              # Standalone interactive web app (Open directly in browser!)
│   └── package.json            # Next.js dependencies
└── README.md
```

---

## Quick Start (Running Locally)

### 1. Run the FastAPI Backend
```powershell
# From python-mastery directory:
& "C:\Users\gumma\anaconda3\python.exe" -m uvicorn backend.app.main:app --reload --port 8000
```
- API root: `http://127.0.0.1:8000/`
- Interactive Swagger API docs: `http://127.0.0.1:8000/docs`

### 2. Run Automated Verification Tests
```powershell
# Test the isolated Python runner sandbox (timeouts, security blocks, assertions):
& "C:\Users\gumma\anaconda3\python.exe" runner/test_runner.py

# Test the FastAPI REST endpoints (progression, execution, mentor hints):
& "C:\Users\gumma\anaconda3\python.exe" backend/tests/test_api.py
```

### 3. Launch the Frontend
You have two options:

- **Instant Browser Access**: Simply open `frontend/index.html` in your web browser (Chrome, Edge, etc.). It connects directly to your running FastAPI backend at `http://127.0.0.1:8000/api`!
- **Next.js Full App**: Once Node.js is installed (`winget install OpenJS.NodeJS.LTS`):
  ```bash
  cd frontend
  npm install
  npm run dev
  ```
  Visit `http://localhost:3000`.

---

## Database Setup (Supabase / PostgreSQL)

1. Create a project at [supabase.com](https://supabase.com).
2. Open the **SQL Editor** in your Supabase dashboard.
3. Paste and run `database/schema.sql` to generate all tables, foreign keys, and RLS policies.
4. Paste and run `database/seed_lessons.sql` to populate Levels 1 to 5 challenges, test cases, and badges.
5. In your project settings, copy your `SUPABASE_URL` and `SUPABASE_ANON_KEY` into `backend/.env`.

---

## Production Deployment Guide

1. **Frontend (Vercel)**:
   - Connect your GitHub repository to Vercel.
   - Set Root Directory to `frontend`.
   - Set Environment Variable `NEXT_PUBLIC_API_URL` to your production FastAPI URL.

2. **Backend (Render / Railway)**:
   - Deploy the `backend/` folder as a Python Web Service.
   - Start command: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
   - Set environment variables: `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `OPENAI_API_KEY`.

3. **Production Python Runner Container**:
   - For high-volume multi-tenant production, deploy the runner in a separate Docker container using lightweight Linux seccomp/cgroups or integrate an external sandboxing cluster (like Piston / Judge0).
