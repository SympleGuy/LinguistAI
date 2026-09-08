# Cloud Audio Storage Setup Guide (Supabase Storage)

LinguistAI automatically stores user voice recordings in **Supabase Storage** under a public bucket named `user-audio`. This eliminates the need for local server disk space and allows seamless, persistent audio playback across devices and cloud hosting platforms (such as Render, Railway, or Fly.io).

---

## 1. Overview & Free Tier Limits

- **Provider**: Supabase Storage
- **Free Tier Allowance**: 1 GB of storage included with every free project (sufficient for tens of thousands of compressed `.webm` audio recordings).
- **Security & Privacy**: Public read access for audio playback; upload restricted to authenticated service roles.
- **Resilience**: If Supabase Storage is ever unreachable or the bucket is missing, the application automatically falls back to local media storage (`media/user_audio/`) without interrupting learner conversations.

---

## 2. Setting Up the Storage Bucket

If you are connecting LinguistAI to a new Supabase project or configuring storage manually, choose either **Option A** (Dashboard UI) or **Option B** (SQL Editor):

### Option A: Via Supabase Dashboard (Recommended — 30 Seconds)

1. Open your project on the [Supabase Dashboard](https://supabase.com/dashboard).
2. In the left navigation menu, click on **Storage**.
3. Click the **New bucket** button in the top right corner.
4. Configure the bucket settings:
   - **Name**: `user-audio`
   - **Public bucket**: Toggle **ON** (required so the browser and audio player can stream the recording).
   - **File size limit**: Set to `10 MB` (or leave blank).
   - **Allowed MIME types**: `audio/webm`, `audio/wav`, `audio/mpeg`, `audio/mp3`, `audio/ogg`.
5. Click **Save bucket**.

---

### Option B: Via Supabase SQL Editor (1-Click Query)

1. Navigate to the **SQL Editor** tab in your Supabase Dashboard.
2. Paste and run the following script:

```sql
-- 1. Create the public user-audio bucket
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
    'user-audio',
    'user-audio',
    true,
    10485760,
    ARRAY['audio/webm', 'audio/wav', 'audio/mpeg', 'audio/mp3', 'audio/ogg']
)
ON CONFLICT (id) DO UPDATE SET public = true;

-- 2. Allow public read access to stored audio files
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies 
    WHERE tablename = 'objects' AND policyname = 'Public Access for user-audio'
  ) THEN
    CREATE POLICY "Public Access for user-audio"
    ON storage.objects FOR SELECT
    USING (bucket_id = 'user-audio');
  END IF;
END $$;

-- 3. Allow service role and server uploads
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies 
    WHERE tablename = 'objects' AND policyname = 'Allow upload to user-audio'
  ) THEN
    CREATE POLICY "Allow upload to user-audio"
    ON storage.objects FOR INSERT
    WITH CHECK (bucket_id = 'user-audio');
  END IF;
END $$;
```

3. Click **Run**. The bucket and security policies will be created immediately.

---

## 3. Environment Configuration

No extra API keys are needed! LinguistAI uses your existing Supabase credentials in `.env`:

```ini
SUPABASE_URL='https://<your-project-ref>.supabase.co'
SUPABASE_ANON_KEY='<your-anon-key>'
SUPABASE_SERVICE_ROLE_KEY='<your-service-role-key>'
```

When an audio response is submitted via `/api/sessions/<id>/respond-audio/`:
1. The server receives the recorded audio stream.
2. The file is uploaded directly to `user-audio/<filename>.webm`.
3. The generated public CDN URL is attached to the session's `InteractionLog` entry.
