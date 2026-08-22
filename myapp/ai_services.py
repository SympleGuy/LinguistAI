import os
import json
import uuid
import time
import urllib.request
import urllib.parse
from pathlib import Path
from django.conf import settings
from decouple import config

# Multi-Provider Configuration
GEMINI_API_KEY = config("GEMINI_API_KEY", default="")
GEMINI_MODEL = config("GEMINI_MODEL", default="gemini-1.5-flash")

ASSEMBLYAI_API_KEY = config("ASSEMBLYAI_API_KEY", default="")

OPENAI_API_KEY = config("OPENAI_API_KEY", default="")
ELEVENLABS_API_KEY = config("ELEVENLABS_API_KEY", default="")
ELEVENLABS_VOICE_ID = config("ELEVENLABS_VOICE_ID", default="21m00Tcm4TlvDq8ikWAM")  # Default voice (Rachel)


def _http_post_json(url, payload, headers, retries=1, timeout=6):
    """Helper to perform HTTP POST with JSON data."""
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                if response.status in (200, 201):
                    body = response.read().decode("utf-8")
                    return json.loads(body)
        except urllib.error.HTTPError as e:
            if e.code in (400, 401, 402, 403, 404, 429):
                print(f"[AI Services] HTTP {e.code} client error from {url}: {e.reason}")
                raise e
            if attempt == retries - 1:
                print(f"[AI Services] HTTP POST error to {url} after {retries} attempts: {e}")
                raise e
        except Exception as e:
            if attempt == retries - 1:
                print(f"[AI Services] HTTP POST error to {url} after {retries} attempts: {e}")
                raise e
    return None


def _call_gemini_generate(system_prompt, user_prompt, response_json=False):
    """
    Call Google Gemini 1.5/2.0 Flash REST API (Free Tier available).
    """
    if not GEMINI_API_KEY:
        return None
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
        
        contents = []
        if user_prompt:
            contents.append({"role": "user", "parts": [{"text": user_prompt}]})

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.3 if response_json else 0.7,
                "maxOutputTokens": 800
            }
        }
        if system_prompt:
            payload["systemInstruction"] = {
                "parts": [{"text": system_prompt}]
            }
        if response_json:
            payload["generationConfig"]["responseMimeType"] = "application/json"

        headers = {"Content-Type": "application/json"}
        resp = _http_post_json(url, payload, headers, retries=2, timeout=12)
        if resp and "candidates" in resp and len(resp["candidates"]) > 0:
            parts = resp["candidates"][0].get("content", {}).get("parts", [])
            if parts and "text" in parts[0]:
                return parts[0]["text"].strip()
    except Exception as e:
        print(f"[AI Services] Google Gemini API call failed: {e}")
    return None


def _transcribe_assemblyai(audio_bytes):
    """
    Transcribe recorded user audio using AssemblyAI REST API (Free Tier available).
    """
    if not ASSEMBLYAI_API_KEY:
        return ""
    try:
        # Step 1: Upload audio file to AssemblyAI
        upload_url = "https://api.assemblyai.com/v2/upload"
        req = urllib.request.Request(
            upload_url,
            data=audio_bytes,
            headers={
                "authorization": ASSEMBLYAI_API_KEY,
                "content-type": "application/octet-stream"
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            if resp.status not in (200, 201):
                return ""
            upload_res = json.loads(resp.read().decode("utf-8"))
            uploaded_audio_url = upload_res.get("upload_url")

        if not uploaded_audio_url:
            return ""

        # Step 2: Request transcription with language detection
        transcript_url = "https://api.assemblyai.com/v2/transcript"
        payload = {
            "audio_url": uploaded_audio_url,
            "language_detection": True
        }
        t_req = urllib.request.Request(
            transcript_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "authorization": ASSEMBLYAI_API_KEY,
                "content-type": "application/json"
            },
            method="POST"
        )
        with urllib.request.urlopen(t_req, timeout=15) as resp:
            if resp.status not in (200, 201):
                return ""
            t_res = json.loads(resp.read().decode("utf-8"))
            transcript_id = t_res.get("id")

        if not transcript_id:
            return ""

        # Step 3: Poll status (max 10 attempts, 1.2s interval)
        poll_url = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
        for _ in range(10):
            time.sleep(1.2)
            p_req = urllib.request.Request(poll_url, headers={"authorization": ASSEMBLYAI_API_KEY})
            with urllib.request.urlopen(p_req, timeout=10) as resp:
                if resp.status == 200:
                    poll_res = json.loads(resp.read().decode("utf-8"))
                    status = poll_res.get("status")
                    if status == "completed":
                        return poll_res.get("text", "")
                    elif status == "error":
                        print(f"[AssemblyAI] Transcription error: {poll_res.get('error')}")
                        break
    except Exception as e:
        print(f"[AssemblyAI] Transcription exception: {e}")
    return ""


def generate_ai_conversation_response(scenario_prompt, user_level="Beginner", target_language="English", context_history=None, user_transcript=""):
    """
    Generate AI conversation response (UC6/UC14).
    Multi-provider support: Google Gemini (Free) -> OpenAI GPT-4o-mini -> Dynamic Scenario Fallback.
    """
    if context_history is None:
        context_history = []

    system_instruction = (
        f"You are a friendly, encouraging AI language tutor helping a student practice speaking {target_language}. "
        f"The student's CEFR proficiency level is {user_level}.\n"
        f"Scenario Context/Persona: {scenario_prompt}\n"
        f"Instructions:\n"
        f"1. You MUST ALWAYS speak and reply strictly in {target_language}.\n"
        f"2. Stay in character for the scenario. If the user speaks off-topic, humorously steer them back to the scenario.\n"
        f"3. If the user speaks in a language other than {target_language}, politely remind them in {target_language} to practice speaking in {target_language}.\n"
        f"4. Keep your response concise (2-4 sentences max), natural, and engaging.\n"
        f"5. Adjust vocabulary complexity to match CEFR level '{user_level}'.\n"
        f"6. Ask open-ended questions in {target_language} to encourage the user to keep speaking."
    )

    # 1. Try Google Gemini (Free tier)
    if GEMINI_API_KEY:
        history_text = ""
        for msg in context_history[-6:]:
            role = "Student" if msg.get("role") == "user" else "Tutor"
            history_text += f"{role}: {msg.get('content', '')}\n"
        user_prompt = f"{history_text}Student: {user_transcript}\nTutor:" if history_text else f"Student: {user_transcript}\nTutor:"
        
        gemini_resp = _call_gemini_generate(system_instruction, user_prompt)
        if gemini_resp:
            return gemini_resp

    # 2. Try OpenAI GPT-4o-mini
    if OPENAI_API_KEY:
        try:
            messages = [{"role": "system", "content": system_instruction}]
            for msg in context_history[-8:]:
                messages.append({"role": msg.get("role", "user"), "content": msg.get("content", "")})
            messages.append({"role": "user", "content": user_transcript})

            payload = {
                "model": "gpt-4o-mini",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 200
            }
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENAI_API_KEY}"
            }
            resp = _http_post_json("https://api.openai.com/v1/chat/completions", payload, headers)
            if resp and "choices" in resp and len(resp["choices"]) > 0:
                return resp["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"[AI Services] OpenAI LLM call failed: {e}. Falling back to dynamic mock.")

    # 3. Dynamic Fallback logic
    user_lower = user_transcript.lower()
    if any(w in user_lower for w in ["hello", "hi", "bonjour", "hola", "guten tag"]):
        return f"Hello! Great to connect with you. I'm ready to practice {target_language} for our scenario. What would you like to start with?"
    elif any(w in user_lower for w in ["order", "menu", "coffee", "food", "table", "commander"]):
        return f"Certainly! Here is our menu. What would you like to order today, and do you have any dietary preferences?"
    elif any(w in user_lower for w in ["help", "direction", "where", "ticket", "station"]):
        return f"I can certainly help you with that! Which location or destination are you looking for?"
    elif any(w in user_lower for w in ["bye", "thank", "merci", "goodbye"]):
        return f"You're very welcome! Excellent effort practicing today. Keep up the great work!"
    else:
        return f"That's a very interesting response! Regarding '{user_transcript}', could you tell me more or elaborate a bit in {target_language}?"


def generate_grammar_and_feedback(user_transcript, target_language="English", user_level="Beginner"):
    """
    Generate detailed multi-layered feedback (grammar, pronunciation score, corrections, suggestions) (UC7/UC8).
    Multi-provider support: Google Gemini (Free) -> OpenAI GPT-4o-mini -> Rule-Based Fallback.
    """
    feedback_system_instruction = (
        f"You are an expert language evaluator for {target_language} at CEFR level {user_level}.\n"
        f"Analyze the user's spoken transcript for grammar, vocabulary, and phrasing.\n"
        f"Special Rule for Language Compliance:\n"
        f"- If the user spoke in {target_language}: Evaluate their grammar, pronunciation, and vocabulary normally.\n"
        f"- If the user spoke in a different language: Give a lower score (30-50), mention in 'comments' that they should speak in {target_language}, and in 'corrections' provide the proper translation/phrasing in {target_language}.\n"
        f"You MUST respond ONLY with a valid JSON object matching this schema:\n"
        f"{{\n"
        f'  "grammar_score": integer 0-100,\n'
        f'  "pronunciation_score": integer 0-100,\n'
        f'  "vocabulary_score": integer 0-100,\n'
        f'  "comments": "Short encouraging evaluation summary.",\n'
        f'  "corrections": [ {{"original": "incorrect segment", "corrected": "fixed segment", "explanation": "why" }} ],\n'
        f'  "suggestions": ["suggestion 1", "suggestion 2"]\n'
        f"}}\n"
    )

    # 1. Try Google Gemini (Free Tier JSON Mode)
    if GEMINI_API_KEY:
        gemini_json_str = _call_gemini_generate(feedback_system_instruction, f"User Transcript to evaluate: '{user_transcript}'", response_json=True)
        if gemini_json_str:
            try:
                return json.loads(gemini_json_str)
            except Exception as e:
                print(f"[AI Services] Gemini JSON parse warning: {e}")

    # 2. Try OpenAI GPT-4o-mini
    if OPENAI_API_KEY:
        try:
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": feedback_system_instruction},
                    {"role": "user", "content": f"User Transcript: '{user_transcript}'"}
                ],
                "response_format": {"type": "json_object"},
                "temperature": 0.3
            }
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENAI_API_KEY}"
            }
            resp = _http_post_json("https://api.openai.com/v1/chat/completions", payload, headers)
            if resp and "choices" in resp and len(resp["choices"]) > 0:
                raw_json = resp["choices"][0]["message"]["content"]
                return json.loads(raw_json)
        except Exception as e:
            print(f"[AI Services] OpenAI feedback generation failed: {e}. Falling back to rule-based analysis.")

    # 3. Rule-based / Heuristic Fallback Analysis
    words = user_transcript.strip().split()
    word_count = len(words)

    grammar_score = min(95, max(70, 75 + min(word_count * 2, 20)))
    pronunciation_score = min(95, max(75, 80 + min(word_count, 15)))
    vocab_score = min(95, max(70, 72 + min(word_count * 3, 22)))

    corrections = []
    if user_transcript and not user_transcript[0].isupper():
        corrections.append({
            "original": user_transcript.split()[0] if words else "",
            "corrected": user_transcript.split()[0].capitalize() if words else "",
            "explanation": "Sentences in formal writing start with a capital letter."
        })

    suggestions = [
        "Try expanding your answers with more detailed clauses.",
        "Practice using transition connectors (e.g. 'because', 'however', 'furthermore')."
    ]

    return {
        "grammar_score": grammar_score,
        "pronunciation_score": pronunciation_score,
        "vocabulary_score": vocab_score,
        "comments": "Good effort! Your response was clear and understandable. Keep building complex sentences.",
        "corrections": corrections,
        "suggestions": suggestions
    }


def transcribe_audio_whisper(audio_bytes, filename="speech.webm"):
    """
    Transcribe recorded user audio using AssemblyAI (Free) or OpenAI Whisper (UC4/UC5).
    """
    # 1. Try AssemblyAI (Free tier)
    if ASSEMBLYAI_API_KEY:
        assembly_text = _transcribe_assemblyai(audio_bytes)
        if assembly_text:
            return assembly_text

    # 2. Try OpenAI Whisper
    if OPENAI_API_KEY:
        try:
            boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
            body = []

            body.append(f"--{boundary}\r\n".encode("utf-8"))
            body.append(b'Content-Disposition: form-data; name="model"\r\n\r\nwhisper-1\r\n')

            body.append(f"--{boundary}\r\n".encode("utf-8"))
            body.append(f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode("utf-8"))
            body.append(b"Content-Type: audio/webm\r\n\r\n")
            body.append(audio_bytes)
            body.append(b"\r\n")
            body.append(f"--{boundary}--\r\n".encode("utf-8"))

            payload_bytes = b"".join(body)
            req = urllib.request.Request(
                "https://api.openai.com/v1/audio/transcriptions",
                data=payload_bytes,
                headers={
                    "Content-Type": f"multipart/form-data; boundary={boundary}",
                    "Authorization": f"Bearer {OPENAI_API_KEY}"
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                if resp.status == 200:
                    res_json = json.loads(resp.read().decode("utf-8"))
                    return res_json.get("text", "")
        except Exception as e:
            print(f"[AI Services] Whisper STT transcription failed: {e}")

    return ""


LANGUAGE_VOICE_MAP = {
    "English": config("ELEVENLABS_VOICE_EN", default=ELEVENLABS_VOICE_ID or "21m00Tcm4TlvDq8ikWAM"),
    "French": config("ELEVENLABS_VOICE_FR", default="ThT5KcBeYPX3keUQqHPh"),
    "Spanish": config("ELEVENLABS_VOICE_ES", default="FGY2WhTYpPnrIDTdsKH5"),
    "German": config("ELEVENLABS_VOICE_DE", default="pNInz6obpgDQGcFmaJgB"),
    "Japanese": config("ELEVENLABS_VOICE_JA", default="pFZP5JQG7iQjIQuC4Bku"),
    "Chinese": config("ELEVENLABS_VOICE_ZH", default="21m00Tcm4TlvDq8ikWAM"),
    "Korean": config("ELEVENLABS_VOICE_KO", default="21m00Tcm4TlvDq8ikWAM"),
    "Vietnamese": config("ELEVENLABS_VOICE_VI", default="21m00Tcm4TlvDq8ikWAM"),
}


def generate_tts_elevenlabs(text, voice_id=None, target_language="English"):
    """
    Generate TTS audio for AI response text using ElevenLabs API (UC9).
    Supports dedicated Voice ID per language and ElevenLabs Multilingual v2.
    Saves audio file to MEDIA_ROOT/tts/ and returns public URL string.
    """
    if not voice_id:
        voice_id = LANGUAGE_VOICE_MAP.get(target_language, ELEVENLABS_VOICE_ID or "21m00Tcm4TlvDq8ikWAM")

    if ELEVENLABS_API_KEY and voice_id:
        try:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            payload = {
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=data,
                headers={
                    "Content-Type": "application/json",
                    "xi-api-key": ELEVENLABS_API_KEY
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=6) as resp:
                if resp.status == 200:
                    audio_data = resp.read()
                    tts_dir = Path(settings.MEDIA_ROOT) / "tts"
                    tts_dir.mkdir(parents=True, exist_ok=True)
                    filename = f"ai_response_{uuid.uuid4().hex[:10]}.mp3"
                    file_path = tts_dir / filename
                    with open(file_path, "wb") as f:
                        f.write(audio_data)
                    return f"{settings.MEDIA_URL}tts/{filename}"
        except urllib.error.HTTPError as e:
            print(f"[AI Services] ElevenLabs HTTP {e.code}: {e.reason}")
        except Exception as e:
            print(f"[AI Services] ElevenLabs TTS generation failed: {e}")

    return None
