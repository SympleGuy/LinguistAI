from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
import uuid
from pathlib import Path
from django.conf import settings
from .supabase_client import supabase_admin, supabase
from django.contrib.auth.hashers import make_password, check_password
from .models import User as AppUser, Scenario, LearningSession, InteractionLog
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils import timezone
from datetime import timedelta
from .ai_services import (
    generate_ai_conversation_response,
    generate_grammar_and_feedback,
    transcribe_audio_whisper,
    generate_tts_elevenlabs
)


def calculate_user_streak(user_id):
    """
    Calculate consecutive active learning days (streak).
    Counts distinct days where the user completed a session or interaction.
    """
    try:
        user_sessions = LearningSession.objects.filter(user_id=user_id).values_list('id', flat=True)

        session_dates = set(
            LearningSession.objects.filter(user_id=user_id, started_at__isnull=False)
            .values_list('started_at__date', flat=True)
        )

        log_dates = set(
            InteractionLog.objects.filter(session_id__in=user_sessions, created_at__isnull=False)
            .values_list('created_at__date', flat=True)
        )

        active_dates = session_dates.union(log_dates)
        if not active_dates:
            return 0

        today = timezone.now().date()
        yesterday = today - timedelta(days=1)

        # If user did not practice today and did not practice yesterday, streak is broken
        if today not in active_dates and yesterday not in active_dates:
            return 0

        # Start from the most recent active day (today if practiced today, else yesterday)
        current_check = today if today in active_dates else yesterday
        streak = 0

        while current_check in active_dates:
            streak += 1
            current_check -= timedelta(days=1)

        return streak
    except Exception as e:
        print(f"[Streak Calculation] Error calculating streak: {e}")
        return 0



@csrf_exempt
def register_view(request):
    if request.method == "POST":
        if request.content_type == "application/json":
            try:
                data = json.loads(request.body)
            except Exception:
                data = {}
        else:
            data = request.POST

        email = (data.get("email") or "").strip()
        input_username = (data.get("username") or "").strip()

        # If username looks like email and email is empty
        if not email and input_username and "@" in input_username:
            email = input_username

        if not email:
            email = input_username

        display_username = input_username if input_username else email.split("@")[0]
        password = data.get("password")
        proficiency_level = data.get("proficiency_level", "Beginner")
        target_language = data.get("target_language", "English")

        if not email or not password:
            if request.content_type == "application/json" or request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"error": "Email and password are required"}, status=400)
            messages.error(request, "Email and password are required.")
            return render(request, "linguistAi_web.html")

        # Check existing user by unique email
        existing = AppUser.objects.filter(email=email).first()

        if existing:
            if request.content_type == "application/json" or request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"error": "An account with this email already exists. Please sign in."}, status=400)
            messages.error(request, "An account with this email already exists.")
            return render(request, "linguistAi_web.html")

        # 1. Register user with Supabase Auth (if Supabase client is configured)
        supabase_uid = None
        if supabase:
            try:
                auth_res = supabase.auth.sign_up({"email": email, "password": password})
                if auth_res and hasattr(auth_res, 'user') and auth_res.user:
                    supabase_uid = str(auth_res.user.id)
            except Exception as e:
                print(f"[Supabase Auth] Sign up notice: {e}")

        # 2. Assign primary key UUID (use Supabase Auth user ID if available, otherwise generate new UUID)
        user_uuid = uuid.UUID(supabase_uid) if supabase_uid else uuid.uuid4()
        now_dt = timezone.now()

        # 3. Direct insertion into Supabase PostgreSQL Database 'users' table using Supabase Client
        hashed = make_password(password)
        supabase_payload = {
            "id": str(user_uuid),
            "username": display_username,
            "email": email,
            "password_hash": hashed,
            "target_language": target_language,
            "proficiency_level": proficiency_level,
            "subscription_plan": "Free",
            "created_at": now_dt.isoformat()
        }

        if supabase_admin:
            try:
                supabase_admin.table("users").insert(supabase_payload).execute()
            except Exception as e:
                if "email" in str(e) and "column" in str(e):
                    try:
                        fallback_payload = supabase_payload.copy()
                        fallback_payload.pop("email", None)
                        supabase_admin.table("users").insert(fallback_payload).execute()
                    except Exception as inner_e:
                        print(f"[Supabase DB] Fallback insertion notice: {inner_e}")
                else:
                    print(f"[Supabase DB] Direct table insertion notice: {e}")
        elif supabase:
            try:
                supabase.table("users").insert(supabase_payload).execute()
            except Exception as e:
                if "email" in str(e) and "column" in str(e):
                    try:
                        fallback_payload = supabase_payload.copy()
                        fallback_payload.pop("email", None)
                        supabase.table("users").insert(fallback_payload).execute()
                    except Exception as inner_e:
                        print(f"[Supabase DB] Fallback insertion notice: {inner_e}")
                else:
                    print(f"[Supabase DB] Direct table insertion notice: {e}")


        # 4. Create local Django database record synced with Supabase user UUID
        app_user = AppUser.objects.create(
            id=user_uuid,
            username=display_username,
            email=email,
            password_hash=hashed,
            target_language=target_language,
            proficiency_level=proficiency_level,
            subscription_plan="Free",
            created_at=now_dt
        )

        # 5. Store active session info
        request.session["supabase_user_id"] = str(app_user.id)
        request.session["user_email"] = email
        request.session["username"] = display_username

        user_data = {
            "id": str(app_user.id),
            "username": display_username,
            "email": email,
            "proficiency_level": app_user.proficiency_level or "Beginner",
            "target_language": app_user.target_language or "English",
            "subscription_plan": app_user.subscription_plan or "Free"
        }

        if request.content_type == "application/json" or request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"status": "success", "message": "Account created successfully", "user": user_data})

        messages.success(request, "Account created successfully!")
        return redirect("dashboard")

    return render(request, "linguistAi_web.html")


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        if request.content_type == "application/json":
            try:
                data = json.loads(request.body)
            except Exception:
                data = {}
        else:
            data = request.POST

        login_input = data.get("email", "").strip()
        password = data.get("password")

        if not login_input or not password:
            if request.content_type == "application/json" or request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"error": "Email and password are required"}, status=400)
            messages.error(request, "Email and password are required.")
            return render(request, "linguistAi_web.html")

        # Find in AppUser table by email
        app_user = AppUser.objects.filter(email=login_input).first()
        authenticated = False

        if app_user and app_user.password_hash:
            if check_password(password, app_user.password_hash):
                authenticated = True

        # Fallback if Supabase configured
        if not authenticated and supabase:
            try:
                res = supabase.auth.sign_in_with_password({"email": login_input, "password": password})
                if res and res.user:
                    authenticated = True
                    if not app_user:
                        app_user = AppUser.objects.create(
                            id=res.user.id,
                            email=login_input,
                            username=login_input.split("@")[0] if "@" in login_input else login_input,
                            created_at=timezone.now()
                        )
            except Exception:
                pass

        if not authenticated:
            if request.content_type == "application/json" or request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"error": "Invalid email or password"}, status=401)
            messages.error(request, "Invalid email or password.")
            return render(request, "linguistAi_web.html")

        # Save session
        user_email = app_user.email or app_user.username
        user_display = app_user.username or user_email
        request.session["supabase_user_id"] = str(app_user.id)
        request.session["user_email"] = user_email
        request.session["username"] = user_display

        user_data = {
            "id": str(app_user.id),
            "username": user_display,
            "email": user_email,
            "proficiency_level": app_user.proficiency_level or "Beginner",
            "target_language": app_user.target_language or "English",
            "subscription_plan": app_user.subscription_plan or "Free"
        }

        if request.content_type == "application/json" or request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"status": "success", "message": "Login successful", "user": user_data})

        return redirect("dashboard")

    return render(request, "linguistAi_web.html")


@csrf_exempt
def logout_view(request):
    if supabase:
        try:
            supabase.auth.sign_out()
        except Exception:
            pass

    # Clear any unconsumed messages stored in session
    storage = messages.get_messages(request)
    for _ in storage:
        pass
    storage.used = True

    request.session.flush()

    if request.content_type == "application/json" or request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"status": "success", "message": "Logged out successfully"})

    return redirect("home")



@csrf_exempt
def api_me(request):
    user_id = request.session.get("supabase_user_id")
    if not user_id:
        return JsonResponse({"authenticated": False}, status=401)

    app_user = AppUser.objects.filter(id=user_id).first()
    if not app_user:
        return JsonResponse({"authenticated": False}, status=401)

    user_email = app_user.email or app_user.username
    user_display = app_user.username or user_email
    return JsonResponse({
        "authenticated": True,
        "user": {
            "id": str(app_user.id),
            "username": user_display,
            "email": user_email,
            "proficiency_level": app_user.proficiency_level or "Beginner",
            "target_language": app_user.target_language or "English",
            "subscription_plan": app_user.subscription_plan or "Free"
        }
    })



def home_view(request):
    return render(request, "linguistAi_web.html")


def spa_web_view(request):
    return render(request, "linguistAi_web.html")


def dashboard_view(request):
    if not request.session.get("supabase_user_id"):
        return redirect("/?page=login")
    return render(request, "linguistAi_web.html")


def scenarios_list(request):
    """
    API endpoint to list scenarios matching learner's target language and CEFR level.
    Supports:
      - ?user_id=...
      - ?lang=... (filters by language)
      - ?cefr=... (filters by level)
      - ?all_levels=true (keeps target language, shows all levels for that language)
      - ?all=true (bypasses all filters)
    """
    user_id = request.GET.get('user_id') or request.session.get('user_id') or request.session.get('supabase_user_id')
    req_lang = (request.GET.get('lang') or '').strip()
    req_cefr = (request.GET.get('cefr') or '').strip()
    all_levels = request.GET.get('all_levels', '').lower() in ('true', '1')
    show_all = request.GET.get('all', '').lower() in ('true', '1')

    if user_id and not req_lang:
        app_user = AppUser.objects.filter(id=user_id).first()
        if app_user:
            req_lang = app_user.target_language or ''
            if not req_cefr and not all_levels:
                req_cefr = app_user.proficiency_level or ''

    scenarios = Scenario.objects.all().order_by('id')
    scenario_list = []
    for scenario in scenarios:
        scenario_data = {
            "id": str(scenario.id),
            "title": scenario.title if scenario.title is not None else "",
            "system_prompt": scenario.system_prompt if scenario.system_prompt is not None else "",
            "video_url": scenario.video_url if scenario.video_url is not None else "",
            "category": "Daily Life",
            "cefr": "Beginner",
            "emoji": "💬",
            "lang": "English",
            "description": ""
        }
        if scenario.system_prompt:
            try:
                parsed = json.loads(scenario.system_prompt)
                if isinstance(parsed, dict):
                    scenario_data["description"] = parsed.get("description", "")
                    scenario_data["category"] = parsed.get("category", "Daily Life")
                    scenario_data["cefr"] = parsed.get("cefr", "Beginner")
                    scenario_data["emoji"] = parsed.get("emoji", "💬")
                    scenario_data["lang"] = parsed.get("lang", "English")
                    scenario_data["system_prompt"] = parsed.get("prompt", scenario.system_prompt)
            except Exception:
                pass
        scenario_list.append(scenario_data)

    if not show_all and (req_lang or req_cefr):
        filtered_list = []
        for s in scenario_list:
            match_lang = not req_lang or s["lang"].lower() == req_lang.lower()
            match_cefr = all_levels or not req_cefr or s["cefr"].lower() == req_cefr.lower()
            if match_lang and match_cefr:
                filtered_list.append(s)

        # Fallback 1: match language if level has no exact match
        if not filtered_list and req_lang:
            for s in scenario_list:
                if s["lang"].lower() == req_lang.lower():
                    filtered_list.append(s)

        # Fallback 2: adapt scenarios for this language if none seeded
        if not filtered_list and req_lang:
            for s in scenario_list[:6]:
                adapted = dict(s)
                adapted["lang"] = req_lang
                adapted["cefr"] = req_cefr or s["cefr"]
                filtered_list.append(adapted)

        if filtered_list:
            return JsonResponse(filtered_list, safe=False)

    return JsonResponse(scenario_list, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class ScenarioDetailView(View):
    def get(self, request, scenario_id):
        """Get detailed information about a specific scenario"""
        try:
            scenario = Scenario.objects.get(id=scenario_id)
            scenario_data = {
                "id": str(scenario.id),
                "title": scenario.title if scenario.title is not None else "",
                "system_prompt": scenario.system_prompt if scenario.system_prompt is not None else "",
                "video_url": scenario.video_url if scenario.video_url is not None else "",
                "category": "Daily Life",
                "cefr": "Beginner",
                "emoji": "💬",
                "lang": "English",
                "description": ""
            }
            if scenario.system_prompt:
                try:
                    parsed = json.loads(scenario.system_prompt)
                    if isinstance(parsed, dict):
                        scenario_data["description"] = parsed.get("description", "")
                        scenario_data["category"] = parsed.get("category", "Daily Life")
                        scenario_data["cefr"] = parsed.get("cefr", "Beginner")
                        scenario_data["emoji"] = parsed.get("emoji", "💬")
                        scenario_data["lang"] = parsed.get("lang", "English")
                        scenario_data["system_prompt"] = parsed.get("prompt", scenario.system_prompt)
                except Exception:
                    pass
            return JsonResponse(scenario_data)
        except Scenario.DoesNotExist:
            return JsonResponse({"error": "Scenario not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class StartSessionView(View):
    def post(self, request):
        """Start a new learning session for a user and scenario"""
        try:
            data = {}
            if request.body:
                try:
                    data = json.loads(request.body)
                except Exception:
                    pass

            user_id = data.get('user_id') or request.session.get('user_id')
            if not user_id:
                first_u = AppUser.objects.first()
                if first_u:
                    user_id = str(first_u.id)

            raw_scenario_id = data.get("scenario_id")

            if not user_id:
                return JsonResponse({"error": "user_id is required"}, status=400)

            # Resolve scenario ID
            scenario_id = None
            if raw_scenario_id is not None:
                try:
                    scenario_id = int(raw_scenario_id)
                except (ValueError, TypeError):
                    matched = Scenario.objects.filter(title__icontains=str(raw_scenario_id)).first()
                    if matched:
                        scenario_id = matched.id

            if not scenario_id:
                first_scen = Scenario.objects.first()
                if first_scen:
                    scenario_id = first_scen.id
                else:
                    return JsonResponse({"error": "No scenarios available"}, status=404)

            # Verify scenario exists
            try:
                scenario = Scenario.objects.get(id=scenario_id)
            except Scenario.DoesNotExist:
                first_scen = Scenario.objects.first()
                if not first_scen:
                    return JsonResponse({"error": "Scenario not found"}, status=404)
                scenario = first_scen
                scenario_id = scenario.id

            # Create new learning session
            session = LearningSession.objects.create(
                user_id=user_id,
                scenario_id=scenario_id,
                started_at=timezone.now()
            )

            return JsonResponse({
                "session_id": str(session.id),
                "user_id": user_id,
                "scenario_id": scenario_id,
                "started_at": session.started_at.isoformat() if session.started_at else None
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


def check_user_daily_turn_limit(user_id):
    """
    UC12: Restrict 'Free Tier' users to maximum 5 conversational turns per day.
    Returns tuple: (is_allowed, today_turn_count, plan_name)
    """
    app_user = AppUser.objects.filter(id=user_id).first()
    plan = (app_user.subscription_plan if (app_user and app_user.subscription_plan) else "Free").strip()

    if plan.lower() != "free":
        return True, 0, plan

    today = timezone.now().date()
    user_sessions = LearningSession.objects.filter(user_id=user_id).values_list('id', flat=True)
    today_turns = InteractionLog.objects.filter(
        session_id__in=user_sessions,
        created_at__date=today
    ).count()

    if today_turns >= 5:
        return False, today_turns, plan
    return True, today_turns, plan


@method_decorator(csrf_exempt, name='dispatch')
class SubmitResponseView(View):
    def post(self, request, session_id):
        """Submit a text user response for a learning session and get AI feedback"""
        try:
            data = json.loads(request.body)
            user_transcript = (data.get('user_transcript') or '').strip()
            user_audio_url = data.get('user_audio_url', '')

            if not user_transcript:
                return JsonResponse({"error": "user_transcript is required"}, status=400)

            try:
                session = LearningSession.objects.get(id=session_id)
            except LearningSession.DoesNotExist:
                return JsonResponse({"error": "Session not found"}, status=404)

            # UC12: Check daily turn limit for Free Tier users
            is_allowed, today_turns, plan = check_user_daily_turn_limit(session.user_id)
            if not is_allowed:
                return JsonResponse({
                    "error": "Daily turn limit reached. Free Tier users are restricted to 5 turns per day.",
                    "limit_reached": True,
                    "turns_today": today_turns,
                    "daily_limit": 5
                }, status=403)

            try:
                scenario = Scenario.objects.get(id=session.scenario_id)
            except Scenario.DoesNotExist:
                return JsonResponse({"error": "Associated scenario not found"}, status=404)

            app_user = AppUser.objects.filter(id=session.user_id).first()
            user_level = app_user.proficiency_level if (app_user and app_user.proficiency_level) else "Beginner"
            target_lang = app_user.target_language if (app_user and app_user.target_language) else "English"

            # Retrieve context history from previous logs in this session
            previous_logs = InteractionLog.objects.filter(session_id=session.id).order_by('created_at')[:10]
            context_history = []
            for log in previous_logs:
                if log.user_transcript:
                    context_history.append({"role": "user", "content": log.user_transcript})
                if log.ai_response_text:
                    context_history.append({"role": "assistant", "content": log.ai_response_text})

            # AI Conversation Response
            ai_response = generate_ai_conversation_response(
                scenario_prompt=scenario.system_prompt or "",
                user_level=user_level,
                target_language=target_lang,
                context_history=context_history,
                user_transcript=user_transcript
            )

            # Multi-layered Grammar & Feedback
            detailed_feedback = generate_grammar_and_feedback(
                user_transcript=user_transcript,
                target_language=target_lang,
                user_level=user_level
            )

            # ElevenLabs Voice Audio Generation (supports native language intonation)
            ai_audio_url = generate_tts_elevenlabs(ai_response, target_language=target_lang)

            interaction = InteractionLog.objects.create(
                session_id=session.id,
                user_transcript=user_transcript,
                user_audio_url=user_audio_url,
                ai_response_text=ai_response,
                ai_audio_url=ai_audio_url or "",
                detailed_feedback=detailed_feedback,
                created_at=timezone.now()
            )

            g_score = detailed_feedback.get("grammar_score", 85)
            p_score = detailed_feedback.get("pronunciation_score", 80)
            session.overall_score = round((g_score + p_score) / 2)
            session.save()

            return JsonResponse({
                "interaction_id": str(interaction.id),
                "ai_response": ai_response,
                "ai_audio_url": ai_audio_url,
                "feedback": detailed_feedback,
                "created_at": interaction.created_at.isoformat() if interaction.created_at else None,
                "turns_today": today_turns + 1,
                "daily_limit": 5 if plan.lower() == "free" else None
            })
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class SubmitAudioResponseView(View):
    def post(self, request, session_id):
        """Submit audio file for speech-to-text transcription and AI response"""
        try:
            try:
                session = LearningSession.objects.get(id=session_id)
            except LearningSession.DoesNotExist:
                return JsonResponse({"error": "Session not found"}, status=404)

            # UC12: Check daily turn limit for Free Tier users
            is_allowed, today_turns, plan = check_user_daily_turn_limit(session.user_id)
            if not is_allowed:
                return JsonResponse({
                    "error": "Daily turn limit reached. Free Tier users are restricted to 5 turns per day.",
                    "limit_reached": True,
                    "turns_today": today_turns,
                    "daily_limit": 5
                }, status=403)

            audio_file = request.FILES.get("audio")
            user_transcript = (request.POST.get("user_transcript") or "").strip()
            user_audio_url = ""

            if audio_file:
                audio_dir = Path(settings.MEDIA_ROOT) / "user_audio"
                audio_dir.mkdir(parents=True, exist_ok=True)
                ext = Path(audio_file.name).suffix or ".webm"
                saved_filename = f"user_{uuid.uuid4().hex[:10]}{ext}"
                saved_path = audio_dir / saved_filename

                audio_bytes = audio_file.read()
                with open(saved_path, "wb") as f:
                    f.write(audio_bytes)

                user_audio_url = f"{settings.MEDIA_URL}user_audio/{saved_filename}"

                if not user_transcript:
                    user_transcript = transcribe_audio_whisper(audio_bytes, filename=saved_filename)

            if not user_transcript:
                user_transcript = "Hello! I would like to practice speaking."

            try:
                scenario = Scenario.objects.get(id=session.scenario_id)
            except Scenario.DoesNotExist:
                return JsonResponse({"error": "Associated scenario not found"}, status=404)

            app_user = AppUser.objects.filter(id=session.user_id).first()
            user_level = app_user.proficiency_level if (app_user and app_user.proficiency_level) else "Beginner"
            target_lang = app_user.target_language if (app_user and app_user.target_language) else "English"

            previous_logs = InteractionLog.objects.filter(session_id=session.id).order_by('created_at')[:10]
            context_history = []
            for log in previous_logs:
                if log.user_transcript:
                    context_history.append({"role": "user", "content": log.user_transcript})
                if log.ai_response_text:
                    context_history.append({"role": "assistant", "content": log.ai_response_text})

            ai_response = generate_ai_conversation_response(
                scenario_prompt=scenario.system_prompt or "",
                user_level=user_level,
                target_language=target_lang,
                context_history=context_history,
                user_transcript=user_transcript
            )

            detailed_feedback = generate_grammar_and_feedback(
                user_transcript=user_transcript,
                target_language=target_lang,
                user_level=user_level
            )

            ai_audio_url = generate_tts_elevenlabs(ai_response, target_language=target_lang)

            interaction = InteractionLog.objects.create(
                session_id=session.id,
                user_transcript=user_transcript,
                user_audio_url=user_audio_url,
                ai_response_text=ai_response,
                ai_audio_url=ai_audio_url or "",
                detailed_feedback=detailed_feedback,
                created_at=timezone.now()
            )

            g_score = detailed_feedback.get("grammar_score", 85)
            p_score = detailed_feedback.get("pronunciation_score", 80)
            session.overall_score = round((g_score + p_score) / 2)
            session.save()

            return JsonResponse({
                "interaction_id": str(interaction.id),
                "user_transcript": user_transcript,
                "ai_response": ai_response,
                "ai_audio_url": ai_audio_url,
                "feedback": detailed_feedback,
                "created_at": interaction.created_at.isoformat() if interaction.created_at else None,
                "turns_today": today_turns + 1,
                "daily_limit": 5 if plan.lower() == "free" else None
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)



@method_decorator(csrf_exempt, name='dispatch')
class DashboardView(View):
    def get(self, request, user_id):
        """Get dashboard/progress data for a user"""
        try:
            app_user = AppUser.objects.filter(id=user_id).first()

            # Get user's learning sessions
            sessions = LearningSession.objects.filter(user_id=user_id).order_by('-started_at')
            total_sessions = sessions.count()

            # Get logs for calculating averages
            session_ids = list(sessions.values_list('id', flat=True))
            logs = InteractionLog.objects.filter(session_id__in=session_ids)

            g_scores = []
            p_scores = []
            for log in logs:
                if log.detailed_feedback and isinstance(log.detailed_feedback, dict):
                    if "grammar_score" in log.detailed_feedback:
                        g_scores.append(log.detailed_feedback["grammar_score"])
                    if "pronunciation_score" in log.detailed_feedback:
                        p_scores.append(log.detailed_feedback["pronunciation_score"])

            avg_grammar = round(sum(g_scores) / len(g_scores)) if g_scores else 85
            avg_pronunciation = round(sum(p_scores) / len(p_scores)) if p_scores else 82

            recent_sessions = []
            for session in sessions[:10]:
                title = "Practice Session"
                emoji = "💬"
                lang = "English"
                try:
                    scenario = Scenario.objects.get(id=session.scenario_id)
                    title = scenario.title if scenario.title else "Practice Session"
                    if scenario.system_prompt:
                        try:
                            parsed = json.loads(scenario.system_prompt)
                            emoji = parsed.get("emoji", "💬")
                            lang = parsed.get("lang", "English")
                        except Exception:
                            pass
                except Scenario.DoesNotExist:
                    pass

                recent_sessions.append({
                    "session_id": str(session.id),
                    "scenario_id": session.scenario_id,
                    "scenario_title": title,
                    "emoji": emoji,
                    "lang": lang,
                    "started_at": session.started_at.isoformat() if session.started_at else None,
                    "overall_score": session.overall_score or 85
                })

            username = app_user.username if app_user else f"User {str(user_id)[:8]}"

            dashboard_data = {
                "user_id": str(user_id),
                "username": username,
                "email": username,
                "proficiency_level": app_user.proficiency_level if (app_user and app_user.proficiency_level) else "Beginner",
                "target_language": app_user.target_language if (app_user and app_user.target_language) else "French",
                "total_sessions": total_sessions,
                "completed_sessions": total_sessions,
                "average_grammar_score": avg_grammar,
                "average_pronunciation_score": avg_pronunciation,
                "recent_sessions": recent_sessions,
                "streak_days": calculate_user_streak(user_id)
            }

            return JsonResponse(dashboard_data)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class SessionHistoryView(View):
    def get(self, request, user_id):
        """Get learning session history for a user"""
        try:
            sessions = LearningSession.objects.filter(user_id=user_id).order_by('-started_at')
            session_history = []
            for session in sessions:
                title = "Unknown Scenario"
                prompt = ""
                try:
                    scenario = Scenario.objects.get(id=session.scenario_id)
                    title = scenario.title if scenario.title else "Unknown Scenario"
                    prompt = scenario.system_prompt if scenario.system_prompt else ""
                except Scenario.DoesNotExist:
                    pass

                session_history.append({
                    "session_id": str(session.id),
                    "scenario": {
                        "id": session.scenario_id,
                        "title": title,
                        "system_prompt": prompt
                    },
                    "started_at": session.started_at.isoformat() if session.started_at else None,
                    "ended_at": None,
                    "overall_score": session.overall_score,
                    "interaction_count": InteractionLog.objects.filter(session_id=session.id).count()
                })

            return JsonResponse({
                "user_id": str(user_id),
                "sessions": session_history,
                "total_count": len(session_history)
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class DebugSessionView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            return JsonResponse({
                'received_data': data,
                'user_id_type': str(type(data.get('user_id'))),
                'user_id_value': repr(data.get('user_id')),
                'scenario_id_type': str(type(data.get('scenario_id'))),
                'scenario_id_value': repr(data.get('scenario_id'))
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class UserProfileUpdateView(View):
    def put(self, request, user_id=None):
        return self.post(request, user_id)

    def post(self, request, user_id=None):
        """Update user profile preferences (Target Language, Proficiency Level, Username)"""
        try:
            if not user_id:
                user_id = request.session.get("supabase_user_id")

            if not user_id:
                return JsonResponse({"error": "User authentication required"}, status=401)

            app_user = AppUser.objects.filter(id=user_id).first()
            if not app_user:
                return JsonResponse({"error": "User not found"}, status=404)

            data = json.loads(request.body)
            new_target_lang = data.get("target_language")
            new_level = data.get("proficiency_level")
            new_username = data.get("username")

            update_data = {}
            if new_target_lang:
                app_user.target_language = new_target_lang
                update_data["target_language"] = new_target_lang
            if new_level:
                app_user.proficiency_level = new_level
                update_data["proficiency_level"] = new_level
            if new_username:
                app_user.username = new_username
                update_data["username"] = new_username

            app_user.save()

            # Sync with Supabase Database table if client is active
            if update_data and (supabase_admin or supabase):
                client = supabase_admin or supabase
                try:
                    client.table("users").update(update_data).eq("id", str(app_user.id)).execute()
                except Exception as e:
                    print(f"[Supabase DB Profile Sync Notice]: {e}")

            return JsonResponse({
                "status": "success",
                "message": "Profile updated successfully",
                "user": {
                    "id": str(app_user.id),
                    "username": app_user.username,
                    "email": app_user.email or app_user.username,
                    "target_language": app_user.target_language,
                    "proficiency_level": app_user.proficiency_level,
                    "subscription_plan": app_user.subscription_plan or "Free"
                }
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class UserAnalyticsView(View):
    def get(self, request, user_id):
        """
        Aggregate learning analytics, performance trends, and daily stats for Chart.js.
        GET /api/user/<uuid:user_id>/analytics/
        """
        try:
            from datetime import timedelta
            app_user = AppUser.objects.filter(id=user_id).first()
            if not app_user:
                return JsonResponse({"error": "User not found"}, status=404)

            sessions = LearningSession.objects.filter(user_id=user_id)
            total_sessions = sessions.count()
            session_ids = list(sessions.values_list('id', flat=True))

            logs = InteractionLog.objects.filter(session_id__in=session_ids).order_by('created_at')
            total_turns = logs.count()

            # Build 7-day timeline (from today - 6 days up to today)
            today = timezone.now().date()
            days_labels = []
            dates_list = []
            grammar_series = []
            pron_series = []
            vocab_series = []
            turns_series = []

            for i in range(6, -1, -1):
                d = today - timedelta(days=i)
                day_name = d.strftime("%a")  # Mon, Tue, etc.
                date_str = d.isoformat()
                days_labels.append(day_name)
                dates_list.append(date_str)

                # Filter logs on this date
                day_logs = [log for log in logs if log.created_at and log.created_at.date() == d]
                turns_count = len(day_logs)
                turns_series.append(turns_count)

                g_day_scores = []
                p_day_scores = []
                v_day_scores = []

                for l in day_logs:
                    if l.detailed_feedback and isinstance(l.detailed_feedback, dict):
                        if "grammar_score" in l.detailed_feedback:
                            g_day_scores.append(l.detailed_feedback["grammar_score"])
                        if "pronunciation_score" in l.detailed_feedback:
                            p_day_scores.append(l.detailed_feedback["pronunciation_score"])
                        if "vocabulary_score" in l.detailed_feedback:
                            v_day_scores.append(l.detailed_feedback["vocabulary_score"])

                # If user had activity, calculate actual average; otherwise provide smooth default baseline
                g_avg = round(sum(g_day_scores) / len(g_day_scores)) if g_day_scores else (80 + (6 - i) * 2)
                p_avg = round(sum(p_day_scores) / len(p_day_scores)) if p_day_scores else (78 + (6 - i) * 2)
                v_avg = round(sum(v_day_scores) / len(v_day_scores)) if v_day_scores else (82 + (6 - i))

                grammar_series.append(min(100, g_avg))
                pron_series.append(min(100, p_avg))
                vocab_series.append(min(100, v_avg))

            # Overall averages
            all_g = []
            all_p = []
            all_v = []
            corrections_list = []

            for log in logs:
                if log.detailed_feedback and isinstance(log.detailed_feedback, dict):
                    if "grammar_score" in log.detailed_feedback:
                        all_g.append(log.detailed_feedback["grammar_score"])
                    if "pronunciation_score" in log.detailed_feedback:
                        all_p.append(log.detailed_feedback["pronunciation_score"])
                    if "vocabulary_score" in log.detailed_feedback:
                        all_v.append(log.detailed_feedback["vocabulary_score"])
                    if "corrections" in log.detailed_feedback and isinstance(log.detailed_feedback["corrections"], list):
                        for c in log.detailed_feedback["corrections"]:
                            if isinstance(c, dict) and "explanation" in c:
                                corrections_list.append(c.get("explanation", ""))

            avg_grammar = round(sum(all_g) / len(all_g)) if all_g else 85
            avg_pron = round(sum(all_p) / len(all_p)) if all_p else 82
            avg_vocab = round(sum(all_v) / len(all_v)) if all_v else 80

            # Count top common mistakes
            from collections import Counter
            top_mistakes = [item[0] for item in Counter(corrections_list).most_common(3) if item[0]]

            analytics_data = {
                "user_id": str(user_id),
                "username": app_user.username or f"User {str(user_id)[:8]}",
                "days": days_labels,
                "dates": dates_list,
                "grammar_series": grammar_series,
                "pronunciation_series": pron_series,
                "vocabulary_series": vocab_series,
                "turns_series": turns_series,
                "total_sessions": total_sessions,
                "total_turns": total_turns,
                "estimated_practice_minutes": round(total_turns * 1.5),
                "streak_days": calculate_user_streak(user_id),
                "average_grammar": avg_grammar,
                "average_pronunciation": avg_pron,
                "average_vocabulary": avg_vocab,
                "top_corrections": top_mistakes if top_mistakes else [
                    "Capitalization at the beginning of sentences",
                    "Verb conjugation consistency",
                    "Article and preposition agreement"
                ]
            }

            return JsonResponse(analytics_data)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class OAuthSessionSyncView(View):
    def post(self, request):
        """
        Synchronize OAuth user (e.g. Google Sign-In via Supabase) with Django DB and session.
        POST /api/auth/oauth-sync/
        """
        try:
            if request.content_type == "application/json":
                data = json.loads(request.body.decode("utf-8") or "{}")
            else:
                data = request.POST

            supabase_uid_str = (data.get("supabase_user_id") or "").strip()
            email = (data.get("email") or "").strip()
            display_name = (data.get("username") or data.get("name") or "").strip()

            if not email and not supabase_uid_str:
                return JsonResponse({"error": "Missing user identity details"}, status=400)

            # Try parsing UUID
            user_uuid = None
            if supabase_uid_str:
                try:
                    user_uuid = uuid.UUID(supabase_uid_str)
                except ValueError:
                    user_uuid = None

            # Look up existing user by ID or Email
            app_user = None
            if user_uuid:
                app_user = AppUser.objects.filter(id=user_uuid).first()
            if not app_user and email:
                app_user = AppUser.objects.filter(email=email).first()

            username_to_use = display_name or (email.split("@")[0] if email else f"User_{str(uuid.uuid4())[:8]}")

            if not app_user:
                final_uuid = user_uuid or uuid.uuid4()
                app_user = AppUser.objects.create(
                    id=final_uuid,
                    username=username_to_use,
                    email=email or f"{username_to_use}@example.com",
                    password_hash="oauth_provider_authenticated",
                    target_language="English",
                    proficiency_level="Beginner",
                    subscription_plan="Free",
                    created_at=timezone.now()
                )
            else:
                if display_name and not app_user.username:
                    app_user.username = display_name
                    app_user.save(update_fields=["username"])

            # Establish Django session
            request.session["supabase_user_id"] = str(app_user.id)
            request.session.modified = True

            return JsonResponse({
                "status": "success",
                "message": "OAuth session synchronized successfully",
                "user": {
                    "id": str(app_user.id),
                    "username": app_user.username,
                    "email": app_user.email,
                    "target_language": app_user.target_language,
                    "proficiency_level": app_user.proficiency_level,
                    "subscription_plan": app_user.subscription_plan or "Free"
                }
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


