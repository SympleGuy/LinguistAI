from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from .supabase_client import supabase_admin, supabase
from django.contrib.auth.hashers import make_password, check_password
from .models import User as AppUser, Scenario, LearningSession, InteractionLog
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils import timezone


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
        # Primary user identifier is email if provided, otherwise username
        user_identifier = email if email else input_username
        password = data.get("password")
        proficiency_level = data.get("proficiency_level", "Beginner")
        target_language = data.get("target_language", "English")

        if not user_identifier or not password:
            if request.content_type == "application/json" or request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"error": "Email/Username and password are required"}, status=400)
            messages.error(request, "Email/Username and password are required.")
            return render(request, "register.html")

        # Check existing user by email or username
        existing = AppUser.objects.filter(username=user_identifier).first()
        if not existing and input_username:
            existing = AppUser.objects.filter(username=input_username).first()

        if existing:
            if request.content_type == "application/json" or request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"error": "User with this email/username already exists"}, status=400)
            messages.error(request, "User already exists.")
            return render(request, "register.html")

        # Create user record in DB
        hashed = make_password(password)
        app_user = AppUser.objects.create(
            username=user_identifier,
            password_hash=hashed,
            target_language=target_language,
            proficiency_level=proficiency_level,
            subscription_plan="Free",
            created_at=timezone.now()
        )

        # Optional Supabase sign_up if configured
        if supabase:
            try:
                supabase.auth.sign_up({"email": email or user_identifier, "password": password})
            except Exception as e:
                print(f"Supabase auth sign_up notice: {e}")

        # Store session info
        request.session["supabase_user_id"] = str(app_user.id)
        request.session["user_email"] = user_identifier
        request.session["username"] = input_username or user_identifier

        user_data = {
            "id": str(app_user.id),
            "username": input_username or user_identifier,
            "email": user_identifier,
            "proficiency_level": app_user.proficiency_level or "Beginner",
            "target_language": app_user.target_language or "English",
            "subscription_plan": app_user.subscription_plan or "Free"
        }

        if request.content_type == "application/json" or request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"status": "success", "message": "Account created successfully", "user": user_data})

        messages.success(request, "Account created successfully!")
        return redirect("dashboard")

    return render(request, "register.html")


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

        login_input = (data.get("email") or data.get("username") or "").strip()
        password = data.get("password")

        if not login_input or not password:
            if request.content_type == "application/json" or request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"error": "Email/username and password are required"}, status=400)
            messages.error(request, "Email and password are required.")
            return render(request, "login.html")

        # Find in AppUser table
        app_user = AppUser.objects.filter(username=login_input).first()
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
                            username=login_input,
                            created_at=timezone.now()
                        )
            except Exception:
                pass

        if not authenticated:
            if request.content_type == "application/json" or request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"error": "Invalid email or password"}, status=401)
            messages.error(request, "Invalid email or password.")
            return render(request, "login.html")

        # Save session
        request.session["supabase_user_id"] = str(app_user.id)
        request.session["user_email"] = app_user.username
        request.session["username"] = app_user.username

        user_data = {
            "id": str(app_user.id),
            "username": app_user.username,
            "email": app_user.username,
            "proficiency_level": app_user.proficiency_level or "Beginner",
            "target_language": app_user.target_language or "English",
            "subscription_plan": app_user.subscription_plan or "Free"
        }

        if request.content_type == "application/json" or request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"status": "success", "message": "Login successful", "user": user_data})

        return redirect("dashboard")

    return render(request, "login.html")


@csrf_exempt
def logout_view(request):
    if supabase:
        try:
            supabase.auth.sign_out()
        except Exception:
            pass
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

    return JsonResponse({
        "authenticated": True,
        "user": {
            "id": str(app_user.id),
            "username": app_user.username,
            "email": app_user.username,
            "proficiency_level": app_user.proficiency_level or "Beginner",
            "target_language": app_user.target_language or "English",
            "subscription_plan": app_user.subscription_plan or "Free"
        }
    })


def home_view(request):
    return render(request, "home.html")


def spa_web_view(request):
    return render(request, "linguistAi_web.html")


def dashboard_view(request):
    # Verify user is authenticated
    if "supabase_user_id" not in request.session:
        return redirect("login")

    user_id = request.session["supabase_user_id"]
    user_email = request.session.get("user_email")

    context = {
        "user_email": user_email,
    }
    return render(request, "dashboard.html", context)


def scenarios_list(request):
    """
    API endpoint to list all scenarios.
    Returns JSON array of scenario objects with metadata fields.
    """
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
            data = json.loads(request.body)
            user_id = data.get('user_id')
            raw_scenario_id = data.get("scenario_id")

            if not user_id or raw_scenario_id is None:
                return JsonResponse({"error": "user_id and scenario_id are required"}, status=400)

            scenario_id = int(raw_scenario_id)

            # Verify scenario exists
            try:
                scenario = Scenario.objects.get(id=scenario_id)
            except Scenario.DoesNotExist:
                return JsonResponse({"error": "Scenario not found"}, status=404)

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
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class SubmitResponseView(View):
    def post(self, request, session_id):
        """Submit a user response for a learning session and get AI feedback"""
        try:
            data = json.loads(request.body)
            user_transcript = data.get('user_transcript', '')
            user_audio_url = data.get('user_audio_url', '')

            if not user_transcript:
                return JsonResponse({"error": "user_transcript is required"}, status=400)

            # Get the session
            try:
                session = LearningSession.objects.get(id=session_id)
            except LearningSession.DoesNotExist:
                return JsonResponse({"error": "Session not found"}, status=404)

            # Get the scenario for context
            try:
                scenario = Scenario.objects.get(id=session.scenario_id)
            except Scenario.DoesNotExist:
                return JsonResponse({"error": "Associated scenario not found"}, status=404)

            # Generate AI response and feedback (simplified version - in reality this would call Supabase/OpenAI)
            # For now, we'll use the scenario's system_prompt as context and generate a basic response
            ai_response = self.generate_ai_response(scenario.system_prompt, user_transcript)
            detailed_feedback = self.generate_feedback(user_transcript)

            # Create interaction log
            interaction = InteractionLog.objects.create(
                session_id=session.id,
                user_transcript=user_transcript,
                user_audio_url=user_audio_url,
                ai_response_text=ai_response,
                detailed_feedback=detailed_feedback,
                created_at=timezone.now()
            )

            # Update overall_score of session in DB
            g_score = detailed_feedback.get("grammar_score", 85)
            p_score = detailed_feedback.get("pronunciation_score", 80)
            session.overall_score = round((g_score + p_score) / 2)
            session.save()

            return JsonResponse({
                "interaction_id": str(interaction.id),
                "ai_response": ai_response,
                "feedback": detailed_feedback,
                "created_at": interaction.created_at.isoformat() if interaction.created_at else None
            })
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def generate_ai_response(self, system_prompt, user_transcript):
        """Generate AI response based on scenario context and user input"""
        return f"I understand you said: '{user_transcript}'. Let's continue practicing!"

    def generate_feedback(self, user_transcript):
        """Generate feedback on user's response"""
        feedback = {
            "grammar_score": 85,
            "pronunciation_score": 80,
            "vocabulary_score": 78,
            "comments": "Good effort! Try to use more complete sentences next time.",
            "suggestions": ["Consider adding more detail to your response", "Pay attention to verb tenses"]
        }
        return feedback


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
                "streak_days": min(total_sessions, 7) if total_sessions > 0 else 0
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
