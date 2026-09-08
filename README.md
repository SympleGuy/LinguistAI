# LinguistAI — AI-Powered Spoken Language Learning Platform

[![Django](https://img.shields.io/badge/Django-4.2%20LTS-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-1.5%20%2F%202.0%20%2F%202.5%20Flash-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)](https://aistudio.google.com/)
[![ElevenLabs](https://img.shields.io/badge/ElevenLabs-Multilingual%20TTS-000000?style=for-the-badge&logo=elevenlabs&logoColor=white)](https://elevenlabs.io/)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL%20%26%20Auth-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
[![Chart.js](https://img.shields.io/badge/Chart.js-v4.4-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)

> **LinguistAI** is a comprehensive, production-grade spoken language learning platform. It empowers learners to develop conversational fluency through voice-to-voice and text interactions with adaptive AI personas, receiving instant, multi-layered feedback on grammar, pronunciation, and vocabulary.

---

## Table of Contents

1. [Key Features](#key-features)
2. [Core Modules](#core-modules)
   - [Structured Scenarios Practice](#1-structured-scenarios-practice)
   - [Free Talk AI Studio](#2-free-talk-ai-studio)
   - [Vocabulary Builder & SRS Flashcards](#3-vocabulary-builder--srs-flashcards)
   - [Interactive Analytics Dashboard](#4-interactive-analytics-dashboard)
   - [Admin Portal & Telemetry](#5-admin-portal--telemetry)
3. [AI & Audio Pipeline Architecture](#ai--audio-pipeline-architecture)
4. [Smart Fallback Simulation Engine](#smart-fallback-simulation-engine)
5. [Local Setup and Installation Guide](#local-setup-and-installation-guide)
6. [REST API Specification Directory](#rest-api-specification-directory)
7. [Database Schema and Security](#database-schema-and-security)
8. [Automated Testing Suite](#automated-testing-suite)
9. [Project Directory Layout](#project-directory-layout)
10. [Capstone Project Information](#capstone-project-information)

---

## Key Features

- **Exclusive Best-of-Breed AI Pipeline**:
  - **Conversational Intelligence**: Google Gemini (1.5 Flash / 2.0 Flash / 2.5 Flash) for dynamic, scenario-aware roleplay.
  - **Linguistic Evaluation**: Google Gemini Structured JSON Schema mode delivering detailed grammar correction, CEFR-appropriate rephrasings, and phonetic pronunciation tips.
  - **Multimodal Audio Transcription (STT)**: Gemini Multimodal Audio handling varied speaker accents, ambient background noise, and natural cadence.
  - **Natural Speech Synthesis (TTS)**: ElevenLabs Multilingual v2 models providing ultra-realistic voice output with native intonation.
- **Custom Interactive Dialog System**: Full replacement of browser-native popups (`alert()` and `confirm()`) with glassmorphic modal dialogs (`#linguistDialogModal`) featuring async confirmation workflows.
- **Strict Session Management**: Turn-based progress tracking preventing ghost or 0-turn empty records in PostgreSQL. Validates turns before concluding, switching personas, or navigating away.
- **Role-Based Access Control (RBAC)**: Enforces `USER` and `ADMIN` role boundaries with dedicated permission guards and admin authentication.
- **Cloud Audio Storage**: User voice recordings are stored in Supabase Storage (`user-audio` bucket) with public CDN streaming and resilient local fallback.

---

## Core Modules

### 1. Structured Scenarios Practice
- **Context-Rich Environments**: Real-world communication simulations including Restaurant Ordering, Airport Check-in, Job Interview, Hotel Reception, Asking for Directions, and Medical Emergencies.
- **CEFR Alignment**: Dynamic vocabulary complexity automatically adjusting to learner proficiency levels (A1 through C2).
- **Turn Limit Enforcement**: Configurable daily practice limits (5 free turns per day) with automatic upgrade flow for VIP tier.

### 2. Free Talk AI Studio
- **Unscripted Spontaneous Practice**: Open-ended conversational practice with 4 specialized AI personalities:
  - ☕ **Friendly Pal**: Warm, casual, and encouraging partner for relaxed chats.
  - 💼 **Career Coach**: Professional interview preparation and workplace communication.
  - 🧠 **Debate Partner**: Inquisitive and thought-provoking counter-argumentation.
  - 🎓 **Strict Professor**: Rigorous grammar discipline and subtle nuance correction.
- **Conversation Starters**: Contextual ice-breaker chips tailored to target languages with randomized shuffling.
- **Real-time Live Feedback Panel**: Immediate turn-by-turn grammar score, fluency score, correction notes, and audio playback.

### 3. Vocabulary Builder & SRS Flashcards
- **Automated Extraction**: Words used during conversations are automatically analyzed and extracted with definitions and contextual usage examples.
- **Spaced Repetition System (SRS)**: Leitner-inspired review scheduling ensuring long-term memory retention.

### 4. Interactive Analytics Dashboard
- **Chart.js Visualizations**: Interactive line and bar charts tracking weekly speaking activity, grammar progress, pronunciation refinement, and vocabulary growth.
- **Streak & Milestone Tracking**: Daily practice streak counters and historical lesson logs.

### 5. Admin Portal & Telemetry (`/admin/dashboard/`)
- **Learner Management**: Real-time user roster, subscription upgrade/downgrade, and manual daily turn limit reset.
- **Scenario Studio**: Create, edit, test AI system prompts, and seed initial curriculum data.
- **Session Telemetry**: Audit individual learning sessions, inspect turn-by-turn dialogue logs, and examine AI evaluation payloads.
- **System Health & Audio Garbage Collection**: Monitor server diagnostics, trigger audio cleanup routines, and export system data (Learners, Sessions, Logs) to CSV and JSON formats.

---

## AI & Audio Pipeline Architecture

LinguistAI consolidates its intelligence pipeline exclusively on **Google Gemini** and **ElevenLabs**:

```
[ User Microphone / Text Input ]
               │
               ▼
   [ Browser Web Audio API ]
               │
       (Audio Blob / WAV)
               │
               ▼
[ Google Gemini Audio Transcription (STT) ]
               │
       (User Transcript)
               │
               ▼
  [ Google Gemini Conversational LLM ]  ◄── [ Scenario / Persona Context ]
               │
     ┌─────────┴──────────┐
     ▼                    ▼
[ AI Text Response ]  [ Google Gemini JSON Evaluation Engine ]
     │                    │
     │                    ├─ Grammar Score (0-100%)
     │                    ├─ Pronunciation Score (0-100%)
     │                    ├─ Vocabulary Score (0-100%)
     │                    ├─ Grammar Corrections
     │                    └─ Extracted Vocabulary
     ▼
[ ElevenLabs Natural Voice TTS ]
     │
 (MP3 Stream)
     │
     ▼
[ Real-Time Web Audio Playback ]
```

| Task | Primary Engine | Fallback |
| :--- | :--- | :--- |
| **Conversational LLM** | Google Gemini 2.5/2.0 Flash (`GEMINI_API_KEY`) | Contextual Simulation Engine |
| **Linguistic Evaluation** | Google Gemini JSON Schema Mode | Heuristic Rule-Based Evaluator |
| **Speech-to-Text (STT)** | Google Gemini Multimodal Audio | Preserved Audio Blob |
| **Text-to-Speech (TTS)** | ElevenLabs Multilingual v2 (`ELEVENLABS_API_KEY`) | Client Speech Synthesis |

---

## Smart Fallback Simulation Engine

Engineered in `myapp/ai_services.py`, the **Smart Fallback Simulation Engine** ensures 100% platform availability:
- If external API keys are absent or rate limits are reached, the system gracefully shifts to deterministic, grammatically sound offline heuristics.
- All evaluation scores, vocabulary extractions, and conversation turns are processed without raising unhandled runtime exceptions.

---

## Local Setup and Installation Guide

### Prerequisites

- **Python 3.11+**
- **Git**

---

### Step 1: Clone the Repository

```bash
git clone https://github.com/SympleGuy/LinguistAI.git
cd LinguistAI
```

### Step 2: Set Up Virtual Environment

```bash
# Linux / macOS:
python3 -m venv venv
source venv/bin/activate

# Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create `.env` in the root directory:

```bash
cp .env.example .env
```

Set the required environment keys in `.env`:

```env
SECRET_KEY=your_django_secret_key_here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3

# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

# ElevenLabs API
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Supabase Credentials (Optional for local SQLite development)
SUPABASE_URL=your_supabase_project_url_here
SUPABASE_ANON_KEY=your_supabase_anon_key_here
```

### Step 5: Database Migrations & Initial Data

```bash
python manage.py migrate
python manage.py seed_scenarios
```

### Step 6: Start the Development Server

```bash
python manage.py runserver 127.0.0.1:8000
```

Access the application in your browser at: `http://127.0.0.1:8000/`

---

## REST API Specification Directory

All protected routes enforce authentication via Django session or `X-User-ID` header through `ApiAuthenticationMiddleware`.

### Learner & Core APIs

| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/register/` | Public | Register new user account with target language and CEFR level |
| `POST` | `/api/auth/login/` | Public | Authenticate user credentials and establish session |
| `POST` | `/api/auth/logout/` | Public | Terminate active user session |
| `GET` | `/api/auth/me/` | Public | Retrieve current authentication state and profile details |
| `POST` | `/api/auth/upgrade/` | Protected | Upgrade account to VIP (Unlimited Practice) tier |
| `GET` | `/api/scenarios/` | Public | Retrieve list of curated conversational scenarios |
| `GET` | `/api/scenarios/<id>/` | Public | Retrieve detailed scenario prompt and CEFR guidelines |
| `POST` | `/api/sessions/start/` | Protected | Initialize a new conversational session |
| `POST` | `/api/sessions/<uuid>/respond/` | Protected | Submit text response for turn evaluation and AI audio response |
| `POST` | `/api/sessions/<uuid>/respond-audio/` | Protected | Upload voice recording for STT transcription and feedback |
| `GET` | `/api/sessions/<uuid>/logs/` | Protected | Retrieve historical interaction logs and feedback for a session |
| `GET` | `/api/dashboard/<uuid>/` | Protected | Retrieve overall statistics, recent sessions, and streak counts |
| `GET` | `/api/user/<uuid>/analytics/` | Protected | Retrieve weekly fluency performance series for Chart.js |
| `POST` | `/api/user/profile/` | Protected | Update user target language or CEFR proficiency level |
| `GET` | `/api/flashcards/due/` | Protected | Fetch Spaced Repetition System (SRS) cards due for review |
| `POST` | `/api/flashcards/<uuid>/review/` | Protected | Submit review grading for an SRS vocabulary card |
| `GET` | `/api/tts/` | Public | Generate ElevenLabs text-to-speech audio for a phrase |

### Admin Telemetry & Management APIs

| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/admin/dashboard/` | Admin | Administrative dashboard web interface |
| `POST` | `/api/admin/auth/login/` | Public | Authenticate administrator credentials |
| `GET` | `/api/admin/metrics/` | Admin | Fetch system KPIs (active users, total sessions, audio storage) |
| `GET` | `/api/admin/users/` | Admin | Search, filter, and paginate all platform learners |
| `POST` | `/api/admin/users/<uuid>/reset-turns/` | Admin | Reset daily practice turn counter for a learner |
| `GET` | `/api/admin/scenarios/` | Admin | List all active conversation scenarios |
| `POST` | `/api/admin/scenarios/test-prompt/` | Admin | Interactive testbed for scenario system prompts with Gemini |
| `GET` | `/api/admin/sessions/` | Admin | Audit learning sessions with score filters |
| `GET` | `/api/admin/sessions/<uuid>/` | Admin | Inspect full dialogue transcript and grammar feedback |
| `POST` | `/api/admin/system/cleanup-audio/` | Admin | Execute manual audio garbage collection |
| `GET` | `/api/admin/export/<dataset>/` | Admin | Export platform data (`learners`, `sessions`, `logs`) to CSV/JSON |

---

## Database Schema and Security

### 1. 3NF Relational Model
- **`users`**: UUID primary key, `username`, `email`, `role` (`USER`/`ADMIN`), `target_language`, `proficiency_level`, `subscription_plan`, `today_turns`, `last_turn_date`.
- **`scenarios`**: `id`, `title`, `system_prompt`, `category`, `cefr`, `emoji`, `lang`, `description`.
- **`learning_sessions`**: UUID primary key, `user_id` (FK), `scenario_id` (FK), `started_at`, `completed_at`, `overall_score`.
- **`interaction_logs`**: UUID primary key, `session_id` (FK), `user_transcript`, `ai_response_text`, `ai_audio_url`, `detailed_feedback` (JSONB), `created_at`.
- **`vocabulary_cards`**: UUID primary key, `user_id` (FK), `word`, `language`, `translation`, `example`, `interval_days`, `due_date`.

### 2. Supabase Row Level Security (RLS)
The included `supabase_rls_policies.sql` provides database-level multi-tenant isolation:
- Learners can only access and modify their own sessions, logs, and vocabulary cards (`auth.uid() = user_id`).
- Administrative operations require verified `ADMIN` role claims.

---

## Automated Testing Suite

The codebase includes an automated unit test suite covering authentication, session evaluation, turn rate limits, admin telemetry, audio cleanup, and middleware:

```bash
python manage.py test --keepdb
```

**Status**: 23/23 tests passing (100% pass rate).

---

## Project Directory Layout

```text
LinguistAI/
├── manage.py                       # Django CLI management entry point
├── requirements.txt                # Python package dependencies
├── .env.example                    # Environment variable template
├── supabase_rls_policies.sql       # Supabase Row Level Security configuration
├── README.md                       # Master platform documentation
├── templates/
│   └── linguistAi_web.html         # Main SPA template (Scenarios, Free Talk, Dashboard)
├── static/
│   ├── css/
│   │   └── app.css                 # Vanilla CSS design system & dialog modal styles
│   ├── js/
│   │   ├── app.js                  # Frontend SPA controller & audio/dialog logic
│   │   └── admin_dashboard.js      # Admin telemetry & portal management logic
│   └── audio/                      # Transient audio storage directory
├── docs/
│   └── AUDIO_STORAGE_GUIDE.md      # Cloud audio storage setup documentation
├── linguistai_project/
│   ├── settings.py                 # Django settings & middleware registration
│   ├── urls.py                     # Root URL routing configuration
│   └── wsgi.py                     # WSGI web server deployment entry point
└── myapp/
    ├── models.py                   # Relational ORM models (User, Session, Log, Card)
    ├── views.py                    # REST API endpoints & session lifecycle handlers
    ├── admin_views.py              # Dedicated Admin Portal REST controllers
    ├── urls.py                     # API routing table
    ├── middleware.py               # Auth guard, RBAC & Global Exception Middlewares
    ├── ai_services.py              # Gemini & ElevenLabs multi-provider AI engine
    ├── tests.py                    # 23-scenario automated test suite
    └── management/commands/
        ├── seed_scenarios.py       # Default conversation scenarios seeder
        └── cleanup_audio_files.py  # Retention policy audio cleanup command
```

---

## Capstone Project Information

- **Project Title**: LinguistAI — Spoken Language Learning Platform
- **Course**: IT Capstone Project
- **License**: MIT License
