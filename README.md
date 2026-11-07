# Election Viz

County-level election maps, state by state. FastAPI backend, TypeScript + D3 frontend.

## Local dev (no Docker needed)

```bash
# backend: http://localhost:8000/docs  (SQLite by default)
cd backend && python3 -m venv .venv && .venv/bin/pip install -e '.[dev]'
.venv/bin/uvicorn app.main:app --reload

# frontend: http://localhost:5173  (proxies /api to :8000)
cd frontend && npm install && npm run dev
```

Tests/lint: `cd backend && .venv/bin/pytest && .venv/bin/ruff check .`

## Layout
- `backend/` FastAPI app, SQLAlchemy models (`Race`, `CountyResult`)
- `frontend/` Vite + TypeScript + D3 choropleth
- `.github/workflows/` CI, plus GitHub Pages deploy for the frontend

## Roadmap
1. ~~Scaffold~~
2. Historical ingest (MIT Election Lab, 2000-2024) and the API
3. Map modes: margin, swing, turnout, third-party share
4. 2026 ingest and polling scheduler
5. Deploy backend (Fly.io/Render + Postgres) and enable Pages
