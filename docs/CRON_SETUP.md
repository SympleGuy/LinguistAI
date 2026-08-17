# LinguistAI Audio Garbage Collection — System Cron Setup Guide

This guide explains how to configure automated scheduled maintenance for deleting `.webm` and `.mp3` audio files older than 30 days while preserving all text transcripts and JSON evaluation scores in the database.

---

## Prerequisites
- Linux or macOS server with `cron` daemon enabled.
- Python virtual environment configured at `/home/alex/venv`.

---

## Step-by-Step Crontab Setup

### 1. Open the System Crontab Editor
Run the following command in the terminal:
```bash
crontab -e
```

### 2. Add the Scheduled Job Entry
Add the following line to run the cleanup job **every Sunday at midnight (00:00 UTC)**:
```cron
0 0 * * 0 /home/alex/Projects/LinguistAI/scripts/run_cleanup_cron.sh
```

*(Alternatively, to run the cleanup every night at midnight, use: `0 0 * * * /home/alex/Projects/LinguistAI/scripts/run_cleanup_cron.sh`)*

### 3. Save and Verify
Save and exit the editor. To verify the cron job is active:
```bash
crontab -l
```

---

## Monitoring and Logs
The script automatically appends execution timestamps, number of deleted audio files, freed disk space in MB, and updated log records to:
```bash
cat /home/alex/Projects/LinguistAI/logs/cleanup_cron.log
```

---

## Manual Execution
You can manually trigger the garbage collection job at any time:
```bash
/home/alex/Projects/LinguistAI/scripts/run_cleanup_cron.sh
```
Or directly through Django management command:
```bash
python manage.py cleanup_audio_files --days 30
```
