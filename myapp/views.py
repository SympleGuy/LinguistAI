from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from .supabase_client import supabase_admin
from .models import Scenario, LearningSession, InteractionLog
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils import timezone


def register_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        username = request.POST.get("username")
        proficiency_level = request.POST.get("proficiency_level", "Beginner")

        try:
            # 1. Sign up user in Supabase Auth
            result = supabase.auth.sign_up({"email": email, "password": password})
            user_id = result.user.id

            # 2. Insert user record into app's users table with proficiency_level
            # Note: Using our custom User model which has different field names
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.create(
                username=username,
                email=email,
                # Note: Password handling is done by Supabase auth, so we don't set password here
                # Our User model has password_hash field but Django's create_user handles hashing
            )
            # Update the user's actual password is handled by Supabase, so we don't store it locally in a way that conflicts
            # Actually, let's just create a basic user record - the auth is handled by Supabase
            # Our User model extends AbstractUser so we can use Django's auth system alongside Supabase
            # But for simplicity given the migration, let's just note that user creation is complex here
            
            # For now, let's just create a simple user entry that matches our User model structure
            # Since we're using Supabase for auth, we'll mainly use the User model for local references if needed
            
            messages.success(request, "Account created! Please check your email to confirm.")
            return redirect("login")
        except Exception as e:
            messages.error(request, f"Registration failed: {str(e)}")

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            result = supabase.auth.sign_in_with_password({"email": email, "password": password})

            # Store auth tokens and user info in session
            request.session["supabase_access_token"] = result.session.access_token
            request.session["supabase_refresh_token"] = result.session.refresh_token
            request.session["supabase_user_id"] = result.user.id
            request.session["user_email"] = result.user.email

            return redirect("dashboard")
        except Exception as e:
            messages.error(request, "Invalid email or password.")

    return render(request, "login.html")


def logout_view(request):
    try:
        supabase.auth.sign_out()
    except:
        pass
    request.session.flush()
    return redirect("home")


def home_view(request):
    return render(request, "home.html")


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
    Returns JSON array of scenario objects with only the fields that exist in the database.
    """
    # Query all scenarios from the database
    scenarios = Scenario.objects.all().order_by('id')

    # Return only the fields that actually exist in the database
    # Based on the updated 0001_initial.py migration:
    # id, title, system_prompt, video_url
    scenario_list = []
    for scenario in scenarios:
        scenario_data = {
            "id": str(scenario.id),  # Convert to string for consistency
            "title": scenario.title if scenario.title is not None else "",
            "system_prompt": scenario.system_prompt if scenario.system_prompt is not None else "",
            "video_url": scenario.video_url if scenario.video_url is not None else ""
        }
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
                "video_url": scenario.video_url if scenario.video_url is not None else ""
            }
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
            scenario_id = int(data.get("scenario_id"))

            if not user_id or not scenario_id:
                return JsonResponse({"error": "user_id and scenario_id are required"}, status=400)

            # Verify user exists (in Django auth system)
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({"error": "User not found"}, status=404)

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
                detailed_feedback=detailed_feedback
            )

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
        # This is a simplified version - in production this would call an LLM
        # For now, return a basic acknowledgment
        return f"I understand you said: '{user_transcript}'. Let's continue practicing!"

    def generate_feedback(self, user_transcript):
        """Generate feedback on user's response"""
        # This is a simplified version - in production this would analyze grammar, pronunciation, etc.
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
            # Verify user exists
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({"error": "User not found"}, status=404)

            # Get user's learning sessions
            sessions = LearningSession.objects.filter(user_id=user_id).order_by('-started_at')

            # Calculate stats
            total_sessions = sessions.count()
            completed_sessions = sessions.filter(overall_score__isnull=False).count()

            # Get recent sessions with details
            recent_sessions = []
            for session in sessions[:10]:  # Last 10 sessions
                try:
                    scenario = Scenario.objects.get(id=session.scenario_id)
                    recent_sessions.append({
                        "session_id": str(session.id),
                        "scenario_title": scenario.title if scenario.title else "Unknown Scenario",
                        "scenario_id": session.scenario_id,
                        "started_at": session.started_at.isoformat() if session.started_at else None,
                        "overall_score": session.overall_score
                    })
                except Scenario.DoesNotExist:
                    # Skip if scenario not found
                    pass

            # Calculate average scores from completed sessions
            completed_with_scores = sessions.exclude(overall_score__isnull=True)
            avg_grammar = 0
            avg_pronunciation = 0

            # In a real app, we'd calculate these from interaction logs
            # For now, using placeholder values
            if completed_with_scores.exists():
                avg_grammar = 82  # placeholder
                avg_pronunciation = 79  # placeholder

            dashboard_data = {
                "user_id": user_id,
                "username": user.username if user.username else f"User {user_id}",
                "total_sessions": total_sessions,
                "completed_sessions": completed_sessions,
                "average_grammar_score": avg_grammar,
                "average_pronunciation_score": avg_pronunciation,
                "recent_sessions": recent_sessions,
                "streak_days": 0  # placeholder - would calculate from session dates
            }

            return JsonResponse(dashboard_data)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class SessionHistoryView(View):
    def get(self, request, user_id):
        """Get learning session history for a user"""
        try:
            # Verify user exists
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({"error": "User not found"}, status=404)

            # Get user's learning sessions with scenario details
            sessions = LearningSession.objects.filter(user_id=user_id).select_related().order_by('-started_at')

            session_history = []
            for session in sessions:
                try:
                    scenario = Scenario.objects.get(id=session.scenario_id)
                    session_history.append({
                        "session_id": str(session.id),
                        "scenario": {
                            "id": scenario.id,
                            "title": scenario.title if scenario.title else "Unknown Scenario",
                            "system_prompt": scenario.system_prompt if scenario.system_prompt else ""
                        },
                        "started_at": session.started_at.isoformat() if session.started_at else None,
                        "ended_at": None,  # We don't track ended_at in current model
                        "overall_score": session.overall_score,
                        "interaction_count": InteractionLog.objects.filter(session_id=session.id).count()
                    })
                except Scenario.DoesNotExist:
                    # Include session even if scenario is missing
                    session_history.append({
                        "session_id": str(session.id),
                        "scenario": {
                            "id": session.scenario_id,
                            "title": "Scenario Not Found",
                            "system_prompt": ""
                        },
                        "started_at": session.started_at.isoformat() if session.started_at else None,
                        "ended_at": None,
                        "overall_score": session.overall_score,
                        "interaction_count": InteractionLog.objects.filter(session_id=session.id).count()
                    })

            return JsonResponse({
                "user_id": user_id,
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
