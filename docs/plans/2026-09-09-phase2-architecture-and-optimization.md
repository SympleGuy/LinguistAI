# Phase 2: Architecture & Optimization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans or superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Strengthen architecture, production readiness, and database security by adding RLS policies for flashcards, hardening Django production settings, removing leftover debug views, and standardizing in-memory caching via `django.core.cache`.

**Architecture:**
- Extend Supabase Row Level Security to `vocabulary_cards` table to enforce tenant isolation at database level.
- Configure flexible and secure production settings in `settings.py` (environment-driven `ALLOWED_HOSTS`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, and configured `CACHES`).
- Remove obsolete `DebugSessionView` endpoint from public routes, views, and middleware.
- Replace unbounded process-global dict caches (`_USER_DASHBOARD_CACHE`, `_USER_ANALYTICS_CACHE`) with `django.core.cache.cache` with bounded entries and TTL.

**Tech Stack:** Django 4.2, PostgreSQL / Supabase RLS, Python Decouple.

---

## Proposed Changes

### 1. Database & Security Policies (`supabase_rls_policies.sql`)
- Add `ALTER TABLE IF EXISTS vocabulary_cards ENABLE ROW LEVEL SECURITY;`.
- Add standard SELECT, INSERT, UPDATE, DELETE policies for `vocabulary_cards` scoped to `auth.uid() = user_id`.

### 2. Production Settings Hardening (`linguistai_project/settings.py`)
- Parse `ALLOWED_HOSTS` dynamically from `.env` (default to `*` for dev or comma-separated domains).
- Set `SESSION_COOKIE_SECURE` and `CSRF_COOKIE_SECURE` based on `not DEBUG` / environment variable.
- Define `CACHES['default']` with `LocMemCache` (bounded `MAX_ENTRIES: 1000`).

### 3. Remove Residual Debug View (`myapp/views.py`, `myapp/urls.py`, `myapp/middleware.py`)
- Delete `DebugSessionView` from `myapp/views.py`.
- Remove route `api/debug-session/` from `myapp/urls.py`.
- Remove `"/api/debug-session/"` from `PUBLIC_API_ROUTES` in `myapp/middleware.py`.

### 4. Refactor Cache to `django.core.cache` (`myapp/views.py`)
- Replace unconstrained dictionary caching with `from django.core.cache import cache`.
- Update `DashboardView`, `UserAnalyticsView`, and `invalidate_dashboard_cache` to use `cache.get()` and `cache.set()`.

---

## Detailed Task Breakdown

### Task 1: Add RLS Policies for `vocabulary_cards`
**Files:**
- Modify: `supabase_rls_policies.sql`

- [x] **Step 1: Update `supabase_rls_policies.sql`**
  Add RLS activation and CRUD policies for `vocabulary_cards` where `auth.uid() = user_id`.
- [x] **Step 2: Verify SQL syntax and completeness**

---

### Task 2: Remove Residual Debug View
**Files:**
- Modify: `myapp/views.py:1280-1296`
- Modify: `myapp/urls.py:21`
- Modify: `myapp/middleware.py:19`
- Test: `myapp/tests.py`

- [x] **Step 1: Write test in `myapp/tests.py`**
  Verify `/api/debug-session/` returns 404.
- [x] **Step 2: Delete `DebugSessionView` from views, urls, and middleware**
- [x] **Step 3: Run test to confirm 404**

---

### Task 3: Production Settings Hardening
**Files:**
- Modify: `linguistai_project/settings.py`

- [x] **Step 1: Configure `ALLOWED_HOSTS`, cookies, and `CACHES` in `settings.py`**
- [x] **Step 2: Run Django system check to verify settings**

---

### Task 4: Standardize Cache with `django.core.cache`
**Files:**
- Modify: `myapp/views.py:40-54, 860-910, 1370-1420`
- Test: `myapp/tests.py`

- [x] **Step 1: Refactor dashboard and analytics cache to `django.core.cache`**
- [x] **Step 2: Run test suite to verify dashboard & analytics caching tests pass**

---

## Verification Plan
- Run complete test suite:
  ```powershell
  & "D:\Workspace\Projects\LinguistAI\venv\Scripts\python.exe" manage.py test myapp --keepdb
  ```
- Run Django system check:
  ```powershell
  & "D:\Workspace\Projects\LinguistAI\venv\Scripts\python.exe" manage.py check
  ```
