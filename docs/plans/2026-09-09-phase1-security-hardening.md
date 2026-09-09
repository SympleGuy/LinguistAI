# Phase 1: Security Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans or superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Eliminate critical security vulnerabilities in LinguistAI (admin backdoor password, header-based user impersonation, admin debug bypass, chat DOM XSS, and API key leakage in URLs).

**Architecture:** 
- Enforce strict server-side authentication without client-controlled unverified headers.
- Remove backdoor passwords and developer debug bypasses from production middleware and auth endpoints.
- Sanitize and escape all user and AI transcripts rendered to the DOM in the frontend.
- Transmit Gemini API credentials securely via `x-goog-api-key` HTTP header rather than URL query parameters.

**Tech Stack:** Django 4.2, Supabase Auth/PostgreSQL, Vanilla JavaScript, Python Decouple.

---

## Proposed Changes

### 1. Admin Authentication (`myapp/admin_views.py`)
- Remove hardcoded `password == "admin123"` fallback.
- Require proper password hashing against `AppUser.password_hash` or Django `authenticate()`.

### 2. Middleware Security & Identity Spoofing (`myapp/middleware.py` & `myapp/views.py`)
- In `myapp/middleware.py`:
  - Eliminate `settings.DEBUG or` from `is_admin_api` check.
  - Remove blind trust in `X-User-ID` header for session creation and auth bypass.
- In `myapp/views.py`:
  - In `api_me`, remove unverified `X-User-ID` fallback that was re-establishing sessions for arbitrary UUIDs.

### 3. Frontend DOM XSS Protection (`static/js/app.js`)
- Add `escapeHTML(str)` helper.
- Sanitize `userText`, `user_transcript`, and `data.ai_response` before interpolating into HTML template literals in chat elements.

### 4. Gemini API Key Security (`myapp/ai_services.py`)
- Remove `?key={GEMINI_API_KEY}` from URLs in `_call_gemini_generate` and `_transcribe_gemini_audio`.
- Pass `x-goog-api-key: GEMINI_API_KEY` in HTTP request headers.

---

## Detailed Task Breakdown

### Task 1: Remove Admin Backdoor Password

**Files:**
- Modify: `myapp/admin_views.py:145-155`
- Test: `myapp/tests.py`

- [x] **Step 1: Write failing test in `myapp/tests.py`**
  Add `test_admin_login_rejects_backdoor_password` in `AdminDashboardViewsTestCase`.
  Verify that attempting to log in as an admin user using `"admin123"` without that being their actual hashed password returns HTTP 401.
- [x] **Step 2: Run test to confirm it fails or passes current state**
  Run: `& "D:\Workspace\Projects\LinguistAI\venv\Scripts\python.exe" manage.py test myapp.tests.AdminDashboardViewsTestCase.test_admin_login_rejects_backdoor_password --keepdb`
- [x] **Step 3: Remove backdoor check in `myapp/admin_views.py`**
  Delete line `elif password == "admin123" and app_user.role == "admin": authenticated = True`.
- [x] **Step 4: Run test to verify it passes**
  Ensure test passes and returns 401.

---

### Task 2: Fix `X-User-ID` Auth Bypass and Admin `DEBUG` Bypass

**Files:**
- Modify: `myapp/middleware.py:39-82`
- Modify: `myapp/views.py:406-424`
- Test: `myapp/tests.py`

- [x] **Step 1: Write failing security tests in `MiddlewareSecurityTestCase`**
  - `test_unauthenticated_request_with_spoofed_x_user_id_header_rejected`: Send protected API request with `X-User-ID: <target_user_id>` without session or bearer token; assert HTTP 401.
  - `test_admin_api_denies_unauthenticated_when_debug_true`: Verify that an unauthenticated request to `/api/admin/users/` returns 403 or 401 even when `DEBUG=True`.
- [x] **Step 2: Run test to verify failures**
  Run: `& "D:\Workspace\Projects\LinguistAI\venv\Scripts\python.exe" manage.py test myapp.tests.MiddlewareSecurityTestCase --keepdb`
- [x] **Step 3: Update `myapp/middleware.py` and `myapp/views.py`**
  - In `middleware.py`: Remove `settings.DEBUG or` from admin check. Remove `x_user_id` automatic session attachment and bypass.
  - In `views.py` (`api_me`): Remove `user_id = request.headers.get("X-User-ID", "")` fallback.
- [x] **Step 4: Run tests to verify they pass**
  Ensure all tests in `MiddlewareSecurityTestCase` pass.

---

### Task 3: Prevent DOM XSS in Chat & Audio Bubbles

**Files:**
- Modify: `static/js/app.js`

- [x] **Step 1: Implement `escapeHTML(str)` utility in `static/js/app.js`**
  ```javascript
  function escapeHTML(str) {
    if (!str || typeof str !== 'string') return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }
  ```
- [x] **Step 2: Apply escaping in chat rendering**
  Escape `userText`, `data.ai_response`, and `data.user_transcript` before rendering in user and AI message bubbles.
- [x] **Step 3: Verify no syntax errors in `static/js/app.js`**

---

### Task 4: Deliver Gemini API Key via Header `x-goog-api-key`

**Files:**
- Modify: `myapp/ai_services.py:97-111, 149-166`
- Test: `myapp/tests.py`

- [x] **Step 1: Write unit test in `myapp/tests.py`**
  Mock `_http_post_json` in `ai_services` and verify that when `generate_ai_conversation_response` or `_transcribe_gemini_audio` is called:
  - The URL does NOT contain `?key=`
  - The headers dict contains `"x-goog-api-key": GEMINI_API_KEY`
- [x] **Step 2: Run test to verify failure**
- [x] **Step 3: Update `myapp/ai_services.py`**
  Add `"x-goog-api-key": GEMINI_API_KEY` to headers, remove `?key={GEMINI_API_KEY}` from endpoint URL.
- [x] **Step 4: Run test to verify pass**

---

## Verification Plan

### Automated Tests
- Run full test suite:
  ```powershell
  & "D:\Workspace\Projects\LinguistAI\venv\Scripts\python.exe" manage.py test myapp --keepdb
  ```
- Confirm all existing 23 tests + new security tests pass without regressions.

### Manual Verification
- Verify Admin login flow rejects `"admin123"`.
- Test `/api/admin/users/` from an unauthenticated browser tab to confirm 403/401 is returned.
- Check chat interface to confirm message bubbles render correctly.
