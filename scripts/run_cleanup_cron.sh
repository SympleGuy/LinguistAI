#!/usr/bin/env bash
# ==============================================================================
# LinguistAI Automated Audio Cleanup Cron Script
# ==============================================================================
# Deletes recorded (.webm) and generated TTS audio files older than 30 days
# while retaining all text transcripts and JSON evaluation logs in database.
# ==============================================================================

set -e

# Project root directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="${PROJECT_DIR}/logs"
LOG_FILE="${LOG_DIR}/cleanup_cron.log"
PYTHON_BIN="/home/alex/venv/bin/python"

mkdir -p "${LOG_DIR}"

echo "==============================================================================" >> "${LOG_FILE}"
echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Starting scheduled audio cleanup job..." >> "${LOG_FILE}"

cd "${PROJECT_DIR}"

# Execute Django management command
if [ -f "${PYTHON_BIN}" ]; then
    "${PYTHON_BIN}" manage.py cleanup_audio_files --days 30 >> "${LOG_FILE}" 2>&1
else
    python3 manage.py cleanup_audio_files --days 30 >> "${LOG_FILE}" 2>&1
fi

echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Audio cleanup job completed." >> "${LOG_FILE}"
echo "==============================================================================" >> "${LOG_FILE}"
