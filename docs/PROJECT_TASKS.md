# LinguistAI — Master Project Task Roadmap & Implementation Checklist

> **Single Source of Truth** for tracking, managing, and executing all engineering tasks for the **LinguistAI** Capstone Project.

---

## Completed Milestones

### Phase 1: Core AI & Audio Processing Pipeline
- [x] **Dynamic LLM Conversation Service (`myapp/ai_services.py`)**: OpenAI GPT-4o-mini persona integration with scenario context, CEFR proficiency adaptation (A1-C2), and conversation memory (8 recent turns).
- [x] **Multi-Layered JSON Feedback Generator (`myapp/ai_services.py`)**: Evaluates Grammar, Pronunciation, and Vocabulary scores with detailed `corrections` (original vs. corrected + explanation) and `suggestions`.
- [x] **Speech-to-Text Endpoint (`POST /api/sessions/<uuid>/respond-audio/`)**: Receives `.webm` audio uploads and transcribes speech via OpenAI Whisper API.
- [x] **Natural Voice TTS Generator (`generate_tts_elevenlabs`)**: Synthesizes AI voice audio in MP3 format using ElevenLabs API with local caching in `media/tts/`.
- [x] **Smart Fallback Simulation Engine**: Heuristic fallback engine enabling full local testing without requiring paid external API keys.

### Phase 2: Authentication & Database Sync
- [x] **Auth API Suite (`myapp/views.py`)**: Endpoints for `/api/auth/register/`, `/api/auth/login/`, `/api/auth/logout/`, `/api/auth/me/`.
- [x] **Dual Database Synchronization**: Synchronizes user accounts between Django internal database and Supabase Auth / PostgreSQL `users` table.
- [x] **Profile Management (`PUT /api/user/profile/`)**: Updates Target Language, CEFR level, Display Name, and syncs directly with Supabase.
- [x] **Session Storage & Clean Logout**: Flushes sessions and unconsumed flash messages upon logout.

### Phase 3: Database Optimization, Rate Limiting & Automation
- [x] **PostgreSQL & SQLite Dual Configuration (`linguistai_project/settings.py`)**: Dynamic configuration via `dj-database-url` with fallback to SQLite for local development.
- [x] **3NF Schema & UUID Primary Keys (`myapp/models.py`)**: UUIDs on `User`, `LearningSession`, `InteractionLog` to eliminate IDOR vulnerabilities.
- [x] **Database Performance Indexing**: B-Tree indexes on `LearningSession(user_id, started_at)` and `InteractionLog(session_id, created_at)`.
- [x] **Free Tier Daily Turn Limiter (`check_user_daily_turn_limit`)**: Enforces max 5 turns/day per user with HTTP 403 Forbidden responses.
- [x] **Audio Garbage Collection Command (`python manage.py cleanup_audio_files`)**: Automated deletion of audio files older than 30 days while preserving text/JSON logs.
- [x] **Scenario Seeding Command (`python manage.py seed_scenarios`)**: Pre-populates 6 diverse scenarios (Restaurant, Airport, Interview, Hotel, Directions, Cafe).

### Phase 4: Frontend SPA Integration & UI/UX Synchronization
- [x] **Unified SPA Routing**: Root `/`, `/dashboard/`, and `/app/` render `linguistAi_web.html` directly.
- [x] **Dynamic Scenario Rendering**: Client dynamically loads and filters scenarios from `/api/scenarios/`.
- [x] **Web Audio Recording (MediaRecorder API)**: Live microphone audio capture and auto-play for AI voice responses.
- [x] **Smart Navigation & State Handling**: Logo and Navbar automatically adapt for authenticated users (hiding "Try for Free" and directing logo click to Dashboard).
- [x] **Live Profile & Dashboard Sync**: Dynamic bindings for profile updates and real-time dashboard stats.
- [x] **Dual-Layer Route Protection (Auth Guard)**: Protects `/dashboard` and `/profile` routes on both Frontend (SPA redirect) and Backend (Django view redirect).

### Phase 5 (Sprint 1): Security, Middleware & Data Integrity
- [x] **Task 1 - Supabase Row Level Security (RLS) SQL Script (`supabase_rls_policies.sql`)**: Production-ready SQL policies for `users`, `learning_sessions`, `interaction_logs`, and `scenarios`.
- [x] **Task 2 - API Authentication Middleware (`myapp/middleware.py`)**: Intercepts protected `/api/` endpoints, returning standard `401 Unauthorized` JSON when unauthenticated.
- [x] **Task 3 - Global Exception Handler Middleware (`myapp/middleware.py`)**: Captures unhandled 500 exceptions across the app, prevents Python stack trace leakage, and returns structured JSON error.

### Phase 6 (Sprint 2): Analytics, Visualizations & System Automation
- [x] **Task 4 - User Analytics API Endpoint (`GET /api/user/<uuid>/analytics/`)**: Computes 7-day daily score progression, total conversational turns, speaking minutes, and top mistake categories.
- [x] **Task 5 - Dynamic Chart.js Visualization in Dashboard**: Replaced static CSS bar mockup with interactive Chart.js line/area chart rendering Grammar vs. Pronunciation curves.
- [x] **Task 6 - Automated Audio Cleanup Cron Script (`scripts/run_cleanup_cron.sh` & `docs/CRON_SETUP.md`)**: Fully automated bash automation with crontab setup guide.

### Phase 7 (Sprint 3): OAuth & Master Documentation
- [x] **Task 7 - Google OAuth2 Sign-In (`POST /api/auth/oauth-sync/` & Supabase JS SDK)**: 1-click Google OAuth authentication with automated session synchronization.
- [x] **Task 9 - Master README Guide (`README.md`)**: Complete guide with zero-config setup, architecture diagrams, and REST API specification table.
- [x] **Automated Test Suite (`myapp/tests.py`)**: 15/15 unit tests passing 100% in under 0.8s.

---


## Technology Stack Reference

| Layer | Technology / Library |
| :--- | :--- |
| **Backend** | Python 3.11+, Django 4.2 LTS, dj-database-url, psycopg2 |
| **Database & Auth** | Supabase PostgreSQL, Supabase Auth SDK, SQLite (Dev fallback) |
| **AI & Speech Services** | OpenAI GPT-4o-mini (LLM), OpenAI Whisper (STT), ElevenLabs (TTS) |
| **Frontend** | HTML5, Bootstrap 5.3, Chart.js v4.4, Vanilla JavaScript (ES6+), HTMX |
| **Testing** | Django TestCase Suite (15 tests, 100% pass), unittest.mock |
