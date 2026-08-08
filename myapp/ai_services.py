import os
import json
import uuid
import time
import urllib.request
import urllib.parse
from pathlib import Path
from django.conf import settings
from decouple import config

OPENAI_API_KEY = config("OPENAI_API_KEY", default="")
ELEVENLABS_API_KEY = config("ELEVENLABS_API_KEY", default="")
ELEVENLABS_VOICE_ID = config("ELEVENLABS_VOICE_ID", default="21m00Tcm4TlvDq8ikWAM")  # Default voice (Rachel)


def _http_post_json(url, payload, headers, retries=3, timeout=10):
    """Helper to perform HTTP POST with JSON data and exponential backoff retry."""
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                if response.status in (200, 201):
                    body = response.read().decode("utf-8")
                    return json.loads(body)
        except Exception as e:
            if attempt == retries - 1:
                print(f"[AI Services] HTTP POST error to {url} after {retries} attempts: {e}")
                raise e
            time.sleep(2 ** attempt)
    return None


def generate_ai_conversation_response(scenario_prompt, user_level="Beginner", target_language="English", context_history=None, user_transcript=""):
    """
    Generate AI conversation response (UC6/UC14).
    Uses OpenAI GPT-4/GPT-3.5 API if key is present, otherwise falls back to dynamic scenario-aware response.
    """
    if context_history is None:
        context_history = []

    system_instruction = (
        f"You are a friendly AI language tutor helping a student practice speaking {target_language}. "
        f"The student's CEFR proficiency level is {user_level}.\n"
        f"Scenario Context/Persona: {scenario_prompt}\n"
        f"Instructions:\n"
        f"1. Stay strictly in character for the scenario.\n"
        f"2. Keep your response concise (2-4 sentences max), natural, and engaging.\n"
        f"3. Adjust vocabulary complexity to match CEFR level '{user_level}'.\n"
        f"4. Ask open questions to encourage the user to keep speaking."
    )

    if OPENAI_API_KEY:
        try:
            messages = [{"role": "system", "content": system_instruction}]
            # Append last 8 turns of context history
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

    # Dynamic Fallback logic
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
    Returns JSON dict.
    """
    if OPENAI_API_KEY:
        try:
            system_instruction = (
                f"You are an expert language evaluator for {target_language} at CEFR level {user_level}.\n"
                f"Analyze the user's spoken transcript for grammar, vocabulary, and phrasing.\n"
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
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": system_instruction},
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

    # Rule-based / Heuristic Fallback Analysis
    words = user_transcript.strip().split()
    word_count = len(words)

    # Heuristic scoring
    grammar_score = min(95, max(70, 75 + min(word_count * 2, 20)))
    pronunciation_score = min(95, max(75, 80 + min(word_count, 15)))
    vocab_score = min(95, max(70, 72 + min(word_count * 3, 22)))

    corrections = []
    # Check simple grammatical checks
    if user_transcript and not user_transcript[0].isupper():
        corrections.append({
            "original": user_transcript.split()[0] if words else "",
            "corrected": user_transcript.split()[0].capitalize() if words else "",
            "explanation": "Sentences in formal writing start with a capital letter."
        })

    suggestions = [
        f"Try expanding your answers with more detailed clauses.",
        f"Practice using transition connectors (e.g. 'because', 'however', 'furthermore')."
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
    Transcribe recorded user audio using OpenAI Whisper API (UC4/UC5).
    """
    if OPENAI_API_KEY:
        try:
            boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
            body = []

            # Add model field
            body.append(f"--{boundary}\r\n".encode("utf-8"))
            body.append(b'Content-Disposition: form-data; name="model"\r\n\r\nwhisper-1\r\n')

            # Add file field
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


def generate_tts_elevenlabs(text, voice_id=None):
    """
    Generate TTS audio for AI response text using ElevenLabs API (UC9).
    Saves audio file to MEDIA_ROOT/tts/ and returns public URL string.
    """
    if not voice_id:
        voice_id = ELEVENLABS_VOICE_ID

    if ELEVENLABS_API_KEY and voice_id:
        try:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            payload = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
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
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    audio_data = resp.read()
                    tts_dir = Path(settings.MEDIA_ROOT) / "tts"
                    tts_dir.mkdir(parents=True, exist_ok=True)
                    filename = f"ai_response_{uuid.uuid4().hex[:10]}.mp3"
                    file_path = tts_dir / filename
                    with open(file_path, "wb") as f:
                        f.write(audio_data)
                    return f"{settings.MEDIA_URL}tts/{filename}"
        except Exception as e:
            print(f"[AI Services] ElevenLabs TTS generation failed: {e}")

    return None
