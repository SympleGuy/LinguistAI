import os
import time
from pathlib import Path
from datetime import datetime, timezone as dt_timezone, timedelta
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from myapp.models import InteractionLog
from myapp.supabase_client import supabase_admin, supabase


class Command(BaseCommand):
    help = (
        "Clean up voice recordings older than the specified retention threshold (default: 30 days) "
        "from Supabase Storage ('user-audio' bucket) and local media directories, while retaining conversation logs."
    )

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
        self.stdout.write(
            self.style.NOTICE(
                f"Starting audio garbage collection for files older than {days} days (cutoff: {cutoff_date.isoformat()})..."
            )
        )

        cloud_deleted_count = 0
        cloud_freed_bytes = 0
        local_deleted_count = 0
        local_freed_bytes = 0

        # 1. Supabase Cloud Storage Cleanup ('user-audio' bucket)
        client = supabase_admin or supabase
        if client:
            try:
                self.stdout.write("Scanning Supabase Storage bucket 'user-audio'...")
                limit = 100
                offset = 0
                while True:
                    files = client.storage.from_("user-audio").list(
                        options={"limit": limit, "offset": offset, "sortBy": {"column": "created_at", "order": "asc"}}
                    )
                    if not files:
                        break

                    files_to_remove = []
                    for item in files:
                        file_name = item.get("name")
                        if not file_name or file_name.startswith("."):
                            continue

                        # Parse creation timestamp
                        created_str = item.get("created_at") or item.get("updated_at")
                        if created_str:
                            try:
                                parsed_time = datetime.fromisoformat(created_str.replace("Z", "+00:00"))
                                if parsed_time < cutoff_date:
                                    files_to_remove.append(file_name)
                                    metadata = item.get("metadata") or {}
                                    file_size = int(metadata.get("size", 0) or 0)
                                    cloud_freed_bytes += file_size
                            except Exception as parse_err:
                                self.stderr.write(f"Could not parse timestamp for {file_name}: {parse_err}")

                    if files_to_remove:
                        client.storage.from_("user-audio").remove(files_to_remove)
                        cloud_deleted_count += len(files_to_remove)
                        preview_names = ", ".join(files_to_remove[:5])
                        self.stdout.write(
                            f"Deleted {len(files_to_remove)} files from Supabase Storage: {preview_names}"
                            + ("..." if len(files_to_remove) > 5 else "")
                        )

                    # If fewer items than limit were returned, we have reached the end
                    if len(files) < limit:
                        break
                    offset += limit

            except Exception as cloud_err:
                self.stderr.write(f"Notice: Supabase Storage cleanup encountered an issue: {cloud_err}")
        else:
            self.stdout.write("Supabase Storage client not configured. Skipping cloud audio scan.")

        # 2. Local Media Storage Cleanup (local media fallback)
        media_subdirs = ["user_audio", "tts"]
        for subdir in media_subdirs:
            folder_path = Path(settings.MEDIA_ROOT) / subdir
            if not folder_path.exists():
                continue

            for file_path in folder_path.glob("*"):
                if file_path.is_file():
                    try:
                        file_mtime = file_path.stat().st_mtime
                        if file_mtime < cutoff_timestamp:
                            file_size = file_path.stat().st_size
                            file_path.unlink()
                            local_deleted_count += 1
                            local_freed_bytes += file_size
                            self.stdout.write(f"Deleted local audio file: {file_path.name}")
                    except Exception as local_file_err:
                        self.stderr.write(f"Failed to delete local file {file_path.name}: {local_file_err}")

        # 3. Update InteractionLog records to clear audio URLs for purged records
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
                log.save(update_fields=["user_audio_url", "ai_audio_url"])
                updated_logs += 1

        total_freed_mb = round((cloud_freed_bytes + local_freed_bytes) / (1024 * 1024), 2)
        summary_msg = (
            f"Garbage collection finished: {cloud_deleted_count} cloud files and {local_deleted_count} local files deleted "
            f"({total_freed_mb} MB freed). Updated {updated_logs} log records."
        )
        self.stdout.write(self.style.SUCCESS(summary_msg))
