# LinguistAI — AI-Powered Spoken Language Learning Platform

[![Django](https://img.shields.io/badge/Django-4.2%20LTS-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-Flash%20Models-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)](https://aistudio.google.com/)
[![ElevenLabs](https://img.shields.io/badge/ElevenLabs-Multilingual%20TTS-000000?style=for-the-badge&logo=elevenlabs&logoColor=white)](https://elevenlabs.io/)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL%20%26%20Storage-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
[![Chart.js](https://img.shields.io/badge/Chart.js-v4.4-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)

> **LinguistAI** is an AI-powered spoken language learning platform. It empowers learners to practice conversational fluency through voice-to-voice and text interactions with adaptive AI personas, receiving instant feedback on grammar, pronunciation, and vocabulary.

---

## Table of Contents

1. [Key Features](#key-features)
2. [Core Modules](#core-modules)
3. [Windows Installation & Setup Guide](#windows-installation--setup-guide)
   - [Prerequisites](#prerequisites)
   - [Step 1: Clone Repository](#step-1-clone-repository)
   - [Step 2: Create & Activate Virtual Environment](#step-2-create--activate-virtual-environment)
   - [Step 3: Install Dependencies](#step-3-install-dependencies)
   - [Step 4: Configure Environment Variables (.env)](#step-4-configure-environment-variables-env)
   - [Step 5: Apply Migrations & Seed Scenarios](#step-5-apply-migrations--seed-scenarios)
   - [Step 6: Start the Development Server](#step-6-start-the-development-server)
4. [Windows Troubleshooting & FAQ](#windows-troubleshooting--faq)
5. [Automated Testing](#automated-testing)
6. [REST API Directory](#rest-api-directory)
7. [Project Directory Layout](#project-directory-layout)
8. [Capstone Project Information](#capstone-project-information)

---

## Key Features

- **AI-Driven Conversational Intelligence**:
  - **Conversational Roleplay**: Google Gemini models generate natural, context-aware dialogues.
  - **Linguistic Evaluation**: Real-time structured evaluation returning grammar scores, phonetic feedback, CEFR-aligned rephrasings, and vocabulary suggestions.
  - **Speech-to-Text (STT)**: Gemini Multimodal Audio transcription handling diverse accents, natural pauses, and varying recording conditions.
  - **Natural Speech Synthesis (TTS)**: Realistic audio streaming with ElevenLabs, backed by browser-native speech synthesis fallback.
  - **Smart Fallback Engine**: If third-party AI keys are unavailable or rate limits are reached, the system smoothly shifts to offline heuristic rules so the app never crashes.
- **Glassmorphic Interactive UI**: Fully custom modal dialog system replacing browser-native alerts for a seamless modern experience.
- **Strict Session Management**: Turn-based progress tracking prevents empty or zero-turn session records in the database.
- **Cloud Audio Storage**: User voice recordings are stored in Supabase Storage (`user-audio` bucket) with public CDN streaming and local disk fallback.
- **Role-Based Access Control (RBAC)**: Secure separation between regular learners (`USER`) and administrators (`ADMIN`).

---

## Core Modules

### 1. Structured Scenarios Practice
- **Real-World Scenarios**: Includes Restaurant Ordering, Airport Check-in, Job Interview, Hotel Reception, Asking for Directions, and Medical Emergencies.
- **CEFR Alignment**: Dynamic vocabulary and response complexity calibrated from beginner (A1) to proficient (C2).
- **Turn Limits**: Configurable daily limits (5 free turns/day) with VIP unlimited practice tier.

### 2. Free Talk AI Studio
- **Unscripted Conversational Practice**: Chat freely with 4 distinct personas:
  - ☕ **Friendly Pal**: Warm, casual chats for stress-free practice.
  - 💼 **Career Coach**: Professional workplace communication and interview coaching.
  - 🧠 **Debate Partner**: Inquisitive counter-perspectives for advanced critical discussion.
  - 🎓 **Strict Professor**: Precise grammatical feedback and vocabulary refinement.
- **Instant Live Feedback**: Score cards for grammar, fluency, and vocabulary with turn-by-turn correction notes.

### 3. Vocabulary Builder & SRS Flashcards
- **Contextual Extraction**: High-value vocabulary from conversation turns is automatically saved with translations and example sentences.
- **Spaced Repetition System (SRS)**: Leitner-based review intervals to optimize memory retention.

### 4. Interactive Analytics Dashboard
- **Visual Progress**: Interactive Chart.js charts displaying weekly speaking consistency, accuracy trends, and vocabulary growth.
- **Streaks & Milestones**: Daily practice streak counter and historical learning logs.

### 5. Admin Portal & Telemetry (`/admin/dashboard/`)
- **Learner Management**: Search users, toggle VIP status, and reset daily turn quotas.
- **Scenario Studio**: Create and update scenarios, inspect AI system prompts, and test prompt generation.
- **Session Telemetry & Cleanup**: Inspect turn logs, audit AI feedback payloads, and run storage cleanup routines.

---

## Windows Installation & Setup Guide

This guide is specifically tailored for **Windows 10 / Windows 11** using **PowerShell** or **Command Prompt (CMD)**.

### Prerequisites

1. **Python 3.11 or newer**:
   - Download the official installer from [python.org](https://www.python.org/downloads/windows/).
   - ⚠️ **Important**: During installation, check the box: **"Add python.exe to PATH"**.
   - Verify installation in PowerShell:
     ```powershell
     python --version
     ```
2. **Git for Windows**:
   - Download and install from [git-scm.com](https://git-scm.com/).
   - Verify installation:
     ```powershell
     git --version
     ```

---

### Step 1: Clone Repository

Open **PowerShell** (or Windows Terminal) and run:

```powershell
git clone https://github.com/SympleGuy/LinguistAI.git
cd LinguistAI
```

---

### Step 2: Create & Activate Virtual Environment

Create an isolated virtual environment (`venv`) to avoid dependency conflicts:

```powershell
python -m venv venv
```

Activate the virtual environment:

- **In PowerShell**:
  ```powershell
  # If you get a script execution policy error, run this first:
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

  # Activate venv:
  .\venv\Scripts\Activate.ps1
  ```
- **In Command Prompt (CMD)**:
  ```cmd
  venv\Scripts\activate.bat
  ```

*(Once activated, you will see `(venv)` at the beginning of your terminal prompt).*

---

### Step 3: Install Dependencies

Ensure `pip` is up to date and install all project dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

### Step 4: Configure Environment Variables (.env)

Create your local `.env` configuration file from the provided template:

- **In PowerShell**:
  ```powershell
  Copy-Item .env.example .env
  ```
- **In Command Prompt (CMD)**:
  ```cmd
  copy .env.example .env
  ```

Open `.env` in Notepad or your preferred editor (`notepad .env`) and configure the settings:

```ini
# Django Security & Debug
SECRET_KEY=django-insecure-change-this-to-a-random-secret-key-12345
DEBUG=True

# Database: Default local SQLite requires ZERO setup!
DATABASE_URL=sqlite:///db.sqlite3

# Google Gemini API Key (Get a free key at https://aistudio.google.com/)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-flash-lite-latest

# ElevenLabs API Key (Optional — browser speech synthesis is used if empty)
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_VOICE_ID=JBFqnCBsd6RMkjVDRZzb

# Supabase Storage & Database (Optional for local testing)
# See docs/AUDIO_STORAGE_GUIDE.md for setting up cloud audio storage
SUPABASE_URL=your_supabase_project_url_here
SUPABASE_ANON_KEY=your_supabase_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key_here
```

> **Note on Database**: By default, `DATABASE_URL=sqlite:///db.sqlite3` uses a local SQLite database file created automatically on your computer. You do not need PostgreSQL or Docker installed to run the application locally!

---

### Step 5: Apply Migrations & Seed Scenarios

Initialize the database tables and populate the default conversational scenarios:

```powershell
# Run database migrations
python manage.py migrate

# Populate default learning scenarios
python manage.py seed_scenarios
```

*(Optional)* Create an administrative superuser to access the Django admin portal:
```powershell
python manage.py createsuperuser
```

---

### Step 6: Start the Development Server

Start the local Django server:

```powershell
python manage.py runserver 127.0.0.1:8000
```

Open your browser and navigate to:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

- **Learner App**: `http://127.0.0.1:8000/`
- **Admin Dashboard**: `http://127.0.0.1:8000/admin/dashboard/`

---

## Windows Troubleshooting & FAQ

### 1. `Activate.ps1 cannot be loaded because running scripts is disabled`
- **Cause**: PowerShell's default execution policy restricts external scripts.
- **Fix**: Run this command in your PowerShell window before activating:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
  .\venv\Scripts\Activate.ps1
  ```

### 2. `'python' is not recognized as an internal or external command`
- **Cause**: Python was installed without checking "Add python.exe to PATH".
- **Fix**:
  - Re-run the Python installer, select **Modify**, check **Add Python to environment variables**, and complete the wizard.
  - Or use the `py` launcher instead: `py -m venv venv` and `py manage.py runserver`.

### 3. Port 8000 is already in use
- **Cause**: Another process or background server is occupying port 8000.
- **Fix**: Launch the server on an alternate port:
  ```powershell
  python manage.py runserver 127.0.0.1:8080
  ```

### 4. Audio recording doesn't work in browser
- **Cause**: Browsers restrict microphone access to secure origins (`localhost`, `127.0.0.1`, or `https://`).
- **Fix**: Always open the site via `http://127.0.0.1:8000/` (not an external IP) and grant microphone permissions when prompted by your browser.

---

## Automated Testing

Run the automated test suite on Windows to verify the application:

```powershell
python manage.py test --keepdb
```

> **Note**: Always include `--keepdb` to preserve the test database schema across test runs and prevent connection-lock errors.

---

## REST API Directory

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
| `POST` | `/api/sessions/<uuid>/respond/` | Protected | Submit text response for turn evaluation and AI feedback |
| `POST` | `/api/sessions/<uuid>/respond-audio/` | Protected | Upload voice recording for STT transcription and feedback |
| `GET` | `/api/sessions/<uuid>/logs/` | Protected | Retrieve historical interaction logs and feedback |
| `GET` | `/api/dashboard/<uuid>/` | Protected | Retrieve overall statistics, recent sessions, and streak counts |
| `GET` | `/api/user/<uuid>/analytics/` | Protected | Retrieve weekly fluency performance series for Chart.js |
| `POST` | `/api/user/profile/` | Protected | Update user target language or CEFR proficiency level |
| `GET` | `/api/flashcards/due/` | Protected | Fetch Spaced Repetition System (SRS) cards due for review |
| `POST` | `/api/flashcards/<uuid>/review/` | Protected | Submit review grading for an SRS vocabulary card |
| `GET` | `/admin/dashboard/` | Admin | Administrative dashboard web interface |
| `GET` | `/api/admin/metrics/` | Admin | Fetch system KPIs (active users, total sessions, storage) |
| `GET` | `/api/admin/users/` | Admin | Search, filter, and paginate platform learners |
| `POST` | `/api/admin/users/<uuid>/reset-turns/` | Admin | Reset daily practice turn counter for a learner |
| `GET` | `/api/admin/sessions/` | Admin | Audit learning sessions with score filters |
| `POST` | `/api/admin/system/cleanup-audio/` | Admin | Trigger manual audio garbage collection |
| `GET` | `/api/admin/export/<dataset>/` | Admin | Export platform data (`learners`, `sessions`, `logs`) to CSV/JSON |

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
