import os
import json
import uuid
import time
import base64
import urllib.request
import urllib.parse
from pathlib import Path
from django.conf import settings
from decouple import config

# Multi-Provider Configuration
GEMINI_API_KEY = config("GEMINI_API_KEY", default="")
GEMINI_MODEL = config("GEMINI_MODEL", default="gemini-3.5-flash-lite")


ELEVENLABS_API_KEY = config("ELEVENLABS_API_KEY", default="")
ELEVENLABS_VOICE_ID = config("ELEVENLABS_VOICE_ID", default="JBFqnCBsd6RMkjVDRZzb")  # George (Free Tier Multilingual v2)


def _http_post_json(url, payload, headers, retries=1, timeout=6):
    """Helper to perform HTTP POST with JSON data and exponential backoff for 429."""
    import urllib.request
    import urllib.error
    import json
    import time

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                if response.status in (200, 201):
                    body = response.read().decode("utf-8")
                    return json.loads(body)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(f"[AI Services] Rate limit (429) hit. Waiting before retry...")
                time.sleep(5)
                # Let it loop to retry if attempts left
                if attempt == retries - 1:
                    raise e
                continue
            if e.code in (400, 401, 402, 403, 404):
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
    Call Google Gemini Flash REST API (Free Tier available).
    """
    if not GEMINI_API_KEY:
        return None

    models_to_try = [GEMINI_MODEL, "gemini-3.5-flash-lite", "gemini-2.5-flash-lite", "gemini-flash-lite-latest"]
    # De-duplicate while preserving order
    seen = set()
    models_to_try = [m for m in models_to_try if m and not (m in seen or seen.add(m))]

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

    for model_name in models_to_try:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_API_KEY}"
            resp = _http_post_json(url, payload, headers, retries=3, timeout=15)
            if resp and "candidates" in resp and len(resp["candidates"]) > 0:
                parts = resp["candidates"][0].get("content", {}).get("parts", [])
                if parts and "text" in parts[0]:
                    return parts[0]["text"].strip()
        except Exception as e:
            print(f"[AI Services] Google Gemini model {model_name} failed: {e}")
            continue

    return None


def _transcribe_gemini_audio(audio_bytes, mime_type="audio/webm"):
    """
    Transcribe spoken audio directly using Gemini Multimodal capability.
    Uses the active GEMINI_API_KEY with 0 external dependencies.
    """
    if not GEMINI_API_KEY or not audio_bytes:
        return ""
    try:
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": (
                                "Listen carefully to this audio recording of a language learner. "
                                "Transcribe the exact spoken words in their original language. "
                                "Output ONLY the clean transcribed text without any timestamps, notes, quotes, or commentary. "
                                "If the audio is silent or unintelligible, output nothing."
                            )
                        },
                        {
                            "inlineData": {
                                "mimeType": mime_type,
                                "data": audio_b64
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 300
            }
        }
        headers = {"Content-Type": "application/json"}
        models_to_try = [GEMINI_MODEL, "gemini-3.5-flash-lite", "gemini-2.5-flash-lite", "gemini-flash-lite-latest"]
        seen = set()
        models_to_try = [m for m in models_to_try if m and not (m in seen or seen.add(m))]

        for model_name in models_to_try:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_API_KEY}"
                resp = _http_post_json(url, payload, headers, retries=3, timeout=15)
                if resp and "candidates" in resp and len(resp["candidates"]) > 0:
                    parts = resp["candidates"][0].get("content", {}).get("parts", [])
                    if parts and "text" in parts[0]:
                        transcript = parts[0]["text"].strip()
                        if transcript and not transcript.lower().startswith("silent") and not transcript.lower().startswith("you go first"):
                            return transcript
            except Exception as e:
                print(f"[AI Services] Gemini Audio Transcription ({model_name}) attempt note: {e}")
                continue
    except Exception as e:
        print(f"[AI Services] Gemini Audio STT failed: {e}")
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


def generate_grammar_and_feedback(user_transcript, target_language, user_level, ai_response=""):
    """
    Evaluates the user's spoken transcript for grammar, pronunciation, and vocabulary.
    Returns a dictionary of scores and feedback.
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
        f'  "suggestions": ["suggestion 1", "suggestion 2"],\n'
        f'  "extracted_vocabulary": [ {{"word": "word in target language", "translation": "translation in English", "example": "example sentence"}} ]\n'
        f"}}\n"
        f"For extracted_vocabulary, extract 1-2 useful new vocabulary words from the provided AI response that the user should learn. If AI response is empty, extract from user transcript.\n"
    )

    # 1. Try Google Gemini (Free Tier JSON Mode)
    if GEMINI_API_KEY:
        gemini_json_str = _call_gemini_generate(feedback_system_instruction, f"User Transcript: '{user_transcript}'\nAI Response: '{ai_response}'", response_json=True)
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
                    {"role": "user", "content": f"User Transcript: '{user_transcript}'\nAI Response: '{ai_response}'"}
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


def transcribe_audio_whisper(audio_bytes, filename="audio.webm"):
    """
    Transcribe audio using Google Gemini Multimodal.
    """
    mime_type = "audio/webm"
    if filename.endswith(".mp3"):
        mime_type = "audio/mp3"
    elif filename.endswith(".wav"):
        mime_type = "audio/wav"
    elif filename.endswith(".ogg"):
        mime_type = "audio/ogg"
    elif filename.endswith(".m4a"):
        mime_type = "audio/m4a"

    if GEMINI_API_KEY:
        gemini_text = _transcribe_gemini_audio(audio_bytes, mime_type=mime_type)
        if gemini_text:
            return gemini_text

    return ""
LANGUAGE_VOICE_MAP = {
    "English": config("ELEVENLABS_VOICE_EN", default=ELEVENLABS_VOICE_ID or "JBFqnCBsd6RMkjVDRZzb"),
    "French": config("ELEVENLABS_VOICE_FR", default="EXAVITQu4vr4xnSDxMaL"),
    "Spanish": config("ELEVENLABS_VOICE_ES", default="EXAVITQu4vr4xnSDxMaL"),
    "German": config("ELEVENLABS_VOICE_DE", default="pNInz6obpgDQGcFmaJgB"),
    "Japanese": config("ELEVENLABS_VOICE_JA", default="JBFqnCBsd6RMkjVDRZzb"),
    "Chinese": config("ELEVENLABS_VOICE_ZH", default="JBFqnCBsd6RMkjVDRZzb"),
    "Korean": config("ELEVENLABS_VOICE_KO", default="JBFqnCBsd6RMkjVDRZzb"),
    "Vietnamese": config("ELEVENLABS_VOICE_VI", default="JBFqnCBsd6RMkjVDRZzb"),
}


def generate_tts_elevenlabs(text, voice_id=None, target_language="English"):
    """
    Generate TTS audio for AI response text using ElevenLabs API (UC9).
    Supports dedicated Voice ID per language and ElevenLabs Multilingual v2.
    Saves audio file to MEDIA_ROOT/tts/ and returns public URL string.
    """
    if not voice_id:
        voice_id = LANGUAGE_VOICE_MAP.get(target_language, ELEVENLABS_VOICE_ID or "JBFqnCBsd6RMkjVDRZzb")

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
