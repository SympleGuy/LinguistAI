import os
import time
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from myapp.models import InteractionLog


class Command(BaseCommand):
    help = "Delete recorded and generated audio files older than 30 days while retaining text/JSON logs (Garbage Collection)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=30,
            help="Threshold age in days for deleting audio files (default: 30 days)."
        )

    def handle(self, *args, **options):
        days = options["days"]
        cutoff_date = timezone.now() - timedelta(days=days)
        cutoff_timestamp = time.time() - (days * 86400)
        self.stdout.write(self.style.NOTICE(f"Starting audio garbage collection for files older than {days} days (cutoff: {cutoff_date})..."))

        deleted_count = 0
        freed_bytes = 0

        # Scan media directories
        media_subdirs = ["user_audio", "tts"]
        for subdir in media_subdirs:
            folder_path = Path(settings.MEDIA_ROOT) / subdir
            if not folder_path.exists():
                continue

            for file_path in folder_path.glob("*"):
                if file_path.is_file():
                    file_mtime = file_path.stat().st_mtime
                    if file_mtime < cutoff_timestamp:
                        file_size = file_path.stat().st_size
                        try:
                            file_path.unlink()
                            deleted_count += 1
                            freed_bytes += file_size
                            self.stdout.write(f"Deleted old audio file: {file_path.name}")
                        except Exception as e:
                            self.stderr.write(f"Failed to delete {file_path.name}: {e}")

        # Update interaction logs user_audio_url and ai_audio_url for old logs if needed
        old_logs = InteractionLog.objects.filter(created_at__lt=cutoff_date)
        updated_logs = 0
        for log in old_logs:
            changed = False
            if log.user_audio_url:
                log.user_audio_url = ""
                changed = True
            if log.ai_audio_url:
                log.ai_audio_url = ""
                changed = True
            if changed:
                log.save()
                updated_logs += 1

        freed_mb = round(freed_bytes / (1024 * 1024), 2)
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully completed garbage collection: Deleted {deleted_count} files ({freed_mb} MB freed). Updated {updated_logs} log records."
            )
        )
