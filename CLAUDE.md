# CLAUDE.md: LinguistAI System Architecture & Context

## 1. Project Overview & Objective

- **Project:** LinguistAI Capstone Project.
- **Goal:** A web application acting as an AI language learning companion to bypass the "fluency plateau." It offers 24/7, real-time, context-specific conversational practice with multi-layered AI feedback (grammar, pronunciation).

## 2. Tech Stack & Environment

- **Backend:** Django 4.2 (Python). Audio processing via `pydub` or `librosa`.
- **Database & Auth:** Supabase (PostgreSQL).
- **Frontend:** Single Page Application (SPA) structure (`linguistAi_web.html`) with JavaScript routing. Auth views use Django templates (`login.html`, `register.html`). UI components built with Bootstrap 5.3 (WCAG 2.1 Level AA compliant).
- **Interactivity:** HTMX for dynamic HTML fragment swapping (no full page reloads).
- **External AI APIs:** OpenAI Whisper (STT), Claude/GPT-4 (LLM), ElevenLabs (TTS).
- **Security:** All API credentials MUST be stored as environment variables (via `python-dotenv`). NEVER expose them to the frontend or version control.

## 3. Database Schema & Supabase Rules

- **Design Pattern:** Strictly Third Normal Form (3NF).
- **Primary Keys:** Exclusively use `UUID`s to prevent IDOR vulnerabilities.
- **Row Level Security (RLS):** Must be strictly enforced. Users can only SELECT, INSERT, UPDATE, DELETE their own sessions and logs.
- **Core Tables & Responsibilities:**
  - `users`: `id` (UUID), `username`, `password_hash` (Django PBKDF2), `target_language`, `proficiency_level` (CEFR), `subscription_plan`.
  - `scenarios`: `id` (INT), `title`, `system_prompt` (defines AI persona), `video_url`. (Read-only for users).
  - `learning_sessions`: `id` (UUID), `user_id`, `scenario_id`, `started_at`, `overall_score`.
  - `interaction_logs`: `id` (UUID), `session_id`, `user_audio_url`, `user_transcript`, `ai_audio_url`, `ai_response_text`, `detailed_feedback`, `created_at`.
- **JSONB Usage:** Use PostgreSQL `JSONB` for the `detailed_feedback` column in `interaction_logs` to flexibly store LLM grammar and pronunciation scores.
- **Indexing:** B-Tree indexes required on `user_id` and `session_id` to optimize dashboard queries.

## 4. Coding Conventions & Best Practices

- **Python/Django:** Follow standard PEP-8 (`snake_case` for variables/functions, `PascalCase` for classes).
- **Pseudocode/Documentation matching:** Abstract DB calls dynamically (e.g., mapping logical `DB_SELECT` to Django ORM or Supabase client).
- **HTMX Swaps:** Use HTMX aggressively for chat updates (injecting transcribed text, AI feedback panels, and ElevenLabs `<audio>` elements) to prevent UI blocking.
- **API Error Handling:** Implement exponential backoff for all external API calls (Whisper, Claude, ElevenLabs). Provide graceful UI fallbacks (e.g., text-input if mic fails).

## 5. Core Implementation Workflows (Use Cases)

- **Audio Pipeline (UC4/UC5):** Frontend captures audio via `MediaRecorder` API -> Django verifies format/size -> Sends to Whisper STT -> Transcribed text injected via HTMX.
- **AI Engine & Memory (UC6/UC14):** At every turn, Django queries `interaction_logs` to retrieve ordered session history. The LLM prompt = (Transcript + Scenario Context + User CEFR Level + Conversation History).
- **Feedback Display (UC7/UC8):** HTMX injects a grammar correction panel below the chat bubble. Incorrect tokens should be highlighted via Bootstrap utility classes.
- **AI Voice Playback (UC9):** ElevenLabs generates audio. The `<audio>` tag is injected into the DOM via HTMX to auto-play, decoupling audio loading from text rendering to maintain speed.

## 6. Business Logic & Constraints (NFRs)

- **Usage Limits (UC12):** System must intercept interactions to restrict 'Free Tier' users to a maximum of 5 conversational turns per day.
- **Latency NFRs:** \* STT Transcript must appear in < 3 seconds.
  - LLM first-word response in < 5 seconds.
  - TTS playback initiates in < 2 seconds post-text generation.
- **Garbage Collection:** CRON jobs must automatically delete heavy `.wav`/`.webm` files from cloud storage after 30 days, retaining only the text/JSON logs.
- **Data Privacy:** Recorded audio must not be retained persistently; only text transcripts and generated AI voice files are kept long-term.

## 7. Development Guidelines for AI Assistant

- Prioritize HTMX over complex JS frameworks for UI reactivity.
- Ensure all frontend changes remain fully responsive and accessible.
- When writing backend views, separate concerns clearly: route handling, external API fetching, and Supabase database interactions should not be deeply tangled in a single function.
