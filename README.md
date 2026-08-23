# LinguistAI — AI-Powered Spoken Language Learning Platform

[![Django](https://img.shields.io/badge/Django-4.2%20LTS-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-1.5%20%2F%202.0%20Flash-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)](https://aistudio.google.com/)
[![AssemblyAI](https://img.shields.io/badge/AssemblyAI-Speech%20to%20Text-0052FF?style=for-the-badge)](https://www.assemblyai.com/)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL%20%26%20Auth-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
[![Chart.js](https://img.shields.io/badge/Chart.js-v4.4-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)

> **LinguistAI** is an interactive spoken language learning web application designed for realistic conversation practice. Learners engage in voice-to-voice scenarios with AI personas, receiving instant, multi-layered feedback on grammar, vocabulary, and pronunciation.

---

## Table of Contents

1. [Key Features](#key-features)
2. [Multi-Provider AI Architecture](#multi-provider-ai-architecture)
3. [Smart Fallback Simulation Engine](#smart-fallback-simulation-engine)
4. [Local Setup and Execution Guide](#local-setup-and-execution-guide)
5. [REST API Specification Directory](#rest-api-specification-directory)
6. [Database Schema and Security](#database-schema-and-security)
7. [Project Directory Layout](#project-directory-layout)
8. [Capstone Project Information](#capstone-project-information)

---

## Key Features

- **Multi-Provider Speech and AI Pipeline**: Flexible integration supporting **Google Gemini 1.5/2.0 Flash** (conversational persona and structured evaluation), **AssemblyAI** and **OpenAI Whisper** (speech-to-text transcription), and **ElevenLabs** (natural voice text-to-speech).
- **Real-time Audio Conversation**: Speech capture using the browser Web Audio API (`MediaRecorder`), transcribed via AssemblyAI or Whisper and synthesized with natural AI voice via ElevenLabs.
- **Adaptive Persona Engine**: Scenario-aware roleplay dynamically adjusting vocabulary to the learner's **CEFR level (A1-C2)**.
- **Multi-Dimensional Feedback**: Structured evaluation per turn delivering **Grammar Score**, **Pronunciation Score**, **Vocabulary Score**, sentence-by-sentence corrections, and natural phrasing suggestions.
- **Interactive Analytics Dashboard**: Dynamic **Chart.js** line/area charts visualizing weekly learning curves, fluency progression, session counts, speaking streaks, and top common grammatical mistakes.
- **Enterprise Security and Route Protection**:
  - Supabase **Row Level Security (RLS)** ensuring strict database-level tenant isolation.
  - Django **API Authentication and Authorization Middleware** intercepting unauthorized requests.
  - Client-side and Server-side **Auth Guards** redirecting unauthenticated guests away from protected user portals.
  - **Global Exception Handler Middleware** preventing Python stack trace leakage.
- **Rate Limiting**: Enforces a daily 5-turn limit on Free Tier accounts with HTTP `403 Forbidden` responses.
- **Automated Audio Garbage Collection**: Scheduled maintenance script (`scripts/run_cleanup_cron.sh`) automatically deleting audio files older than 30 days while preserving database transcripts.

---

## Multi-Provider AI Architecture

LinguistAI features a plug-and-play multi-provider architecture designed to support both free and premium AI services:

| Function | Primary Provider (Free Tier Available) | Secondary / Premium Provider | Offline Fallback |
| :--- | :--- | :--- | :--- |
| **Conversational LLM** | **Google Gemini 1.5/2.0 Flash** (`GEMINI_API_KEY`) | **OpenAI GPT-4o-mini** (`OPENAI_API_KEY`) | Dynamic Scenario-aware Engine |
| **Grammar Evaluation** | **Google Gemini JSON Schema Mode** (`GEMINI_API_KEY`) | **OpenAI Structured JSON** (`OPENAI_API_KEY`) | Rule-based Heuristic Analyzer |
| **Speech-to-Text (STT)** | **AssemblyAI API** (`ASSEMBLYAI_API_KEY`) | **OpenAI Whisper** (`OPENAI_API_KEY`) | Audio Blob Preservation |
| **Text-to-Speech (TTS)** | **ElevenLabs Free Tier** (`ELEVENLABS_API_KEY`) | **ElevenLabs Multilingual** | Client Audio Response |

---

## Smart Fallback Simulation Engine

The platform is engineered with an intelligent **Smart Fallback Simulation Engine** in `myapp/ai_services.py`. If external API keys (`GEMINI_API_KEY`, `ASSEMBLYAI_API_KEY`, `OPENAI_API_KEY`, `ELEVENLABS_API_KEY`) are missing or inactive:
- **LLM Roleplay**: Generates contextual, grammatically sound scenario responses.
- **Feedback Engine**: Computes realistic grammar/pronunciation scores and generates precise corrections.
- **Audio Engine**: Synthesizes speech or falls back seamlessly to text-based audio payloads.
- **Database & Dashboard**: Full database logging, analytics calculation, and Chart.js rendering continue to operate normally.

---

## Local Setup and Execution Guide

### Prerequisites
- **Python 3.11+** installed on the local system.
- **Git** and a standard terminal shell.

---

### Step 1: Clone the Repository
```bash
git clone https://github.com/SympleGuy/LinguistAI.git
cd LinguistAI
```

### Step 2: Create and Activate Python Virtual Environment
```bash
# On Linux / macOS:
python3 -m venv venv
source venv/bin/activate

# On Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration
Create a `.env` file in the project root directory based on `.env.example`:
```bash
cp .env.example .env
```

Define the desired environment variable keys in `.env`:
```env
SECRET_KEY=your_django_secret_key_here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3

# Multi-Provider AI (Choose Gemini + AssemblyAI, or OpenAI)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
ASSEMBLYAI_API_KEY=your_assemblyai_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

SUPABASE_URL=your_supabase_project_url_here
SUPABASE_ANON_KEY=your_supabase_anon_key_here
```

### Step 5: Apply Database Migrations
```bash
python manage.py migrate
```

### Step 6: Seed Conversation Scenarios
Populates default conversation scenarios (Restaurant, Airport, Job Interview, Hotel, Directions, Cafe):
```bash
python manage.py seed_scenarios
```

### Step 7: Run the Development Server
```bash
python manage.py runserver 127.0.0.1:8000
```
Open the browser and navigate to: `http://127.0.0.1:8000/`

---

## REST API Specification Directory

All protected routes enforce authentication via Django session or Bearer token through `ApiAuthenticationMiddleware`.

| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/register/` | Public | Register new user account with email and password |
| `POST` | `/api/auth/login/` | Public | Authenticate user and initialize session |
| `POST` | `/api/auth/logout/` | Public | Terminate active session and clear cookies |
| `GET` | `/api/auth/me/` | Public | Check current authentication status and user details |
| `POST` | `/api/auth/oauth-sync/` | Public | Synchronize OAuth user (Google Sign-In) into database |
| `GET` | `/api/scenarios/` | Public | Fetch list of all active learning scenarios |
| `GET` | `/api/scenarios/<id>/` | Public | Fetch detail for a specific scenario |
| `POST` | `/api/sessions/start/` | Protected | Start a new learning session for a scenario |
| `POST` | `/api/sessions/<uuid>/respond/` | Protected | Submit text transcript response and receive AI feedback |
| `POST` | `/api/sessions/<uuid>/respond-audio/` | Protected | Upload voice recording for STT transcription and feedback |
| `GET` | `/api/dashboard/<uuid:user_id>/` | Protected | Fetch summary statistics and recent session history |
| `GET` | `/api/user/<uuid:user_id>/analytics/` | Protected | Fetch performance series for Chart.js visualization |
| `POST` | `/api/user/profile/` | Protected | Update user target language and CEFR proficiency level |

---

## Database Schema and Security

### 1. 3NF Relational Data Model
- **`users`**: UUID primary key, `username`, `email`, `target_language`, `proficiency_level`, `subscription_plan`.
- **`scenarios`**: `id`, `title`, `system_prompt`, `category`, `cefr`, `emoji`, `lang`, `description`.
- **`learning_sessions`**: UUID primary key, `user_id` (FK), `scenario_id` (FK), `started_at`, `completed_at`, `overall_score`.
- **`interaction_logs`**: UUID primary key, `session_id` (FK), `user_transcript`, `ai_response_text`, `audio_file_url`, `detailed_feedback` (JSONB).

### 2. Supabase Row Level Security (RLS)
The included script `supabase_rls_policies.sql` enforces zero-trust tenant isolation on PostgreSQL:
- Users can only select and update their own profile (`auth.uid() = id`).
- Users can only create and view their own learning sessions (`auth.uid() = user_id`).
- Interaction logs are strictly restricted to session owners.

---

## Project Directory Layout

```text
LinguistAI/
├── manage.py                       # Django management entry point
├── requirements.txt                # Python package dependencies
├── .env.example                    # Environment configuration template
├── supabase_rls_policies.sql       # Supabase Row Level Security policies
├── README.md                       # Master documentation guide
├── linguistAi_web.html             # Frontend Single Page Application (SPA)
├── templates/
│   └── linguistAi_web.html         # Django template sync
├── scripts/
│   └── run_cleanup_cron.sh         # Automated audio cleanup cron script
├── docs/
│   └── CRON_SETUP.md               # Crontab schedule configuration guide
├── linguistai_project/
│   ├── settings.py                 # Global Django settings (Middleware, DB, Apps)
│   ├── urls.py                     # Root URL routing configuration
│   └── wsgi.py                     # WSGI application entry point
└── myapp/
    ├── models.py                   # 3NF Database Models (User, Session, Log, Scenario)
    ├── views.py                    # REST API View Controllers & SPA View
    ├── urls.py                     # App-level API URL routes
    ├── middleware.py               # Auth & Global Exception Handler Middlewares
    ├── ai_services.py              # Multi-Provider AI (Gemini, AssemblyAI, OpenAI, ElevenLabs)
    ├── tests.py                    # Automated unit test suite
    └── management/commands/
        ├── seed_scenarios.py       # Pre-populates conversation scenarios
        └── cleanup_audio_files.py  # Audio file garbage collection command
```

---

## Capstone Project Information

- **Project**: LinguistAI — Spoken Language Learning Platform
- **Course**: IT Capstone Project 1 + 2
- **License**: MIT
