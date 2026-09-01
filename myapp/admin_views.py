import json
import os
import uuid
from pathlib import Path
from datetime import timedelta
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.db.models import Count, Avg, Q
from django.conf import settings
from django.core.management import call_command
from django.contrib.auth.hashers import make_password

from .models import User as AppUser, Scenario, LearningSession, InteractionLog, VocabularyCard
from .ai_services import generate_ai_conversation_response, generate_grammar_and_feedback


def is_admin_authorized(request):
    """
    Check if the user is authorized to view the admin dashboard:
    - Django staff or superuser
    - Session role is 'admin' or has is_admin flag
    - AppUser in DB has role='admin'
    - Or in DEBUG mode with local development
    """
    if getattr(request, 'user', None) and request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return True
    if request.session.get("role") == "admin" or request.session.get("is_admin") or request.session.get("is_staff"):
        return True
    user_id = request.session.get("supabase_user_id")
    if user_id:
        try:
            if AppUser.objects.filter(id=uuid.UUID(str(user_id)), role="admin").exists():
                return True
        except Exception:
            pass
    if settings.DEBUG:
        return True
    return False


from django.template.loader import render_to_string

def admin_dashboard_view(request):
    """Render the Modern Admin Dashboard SPA"""
    html = render_to_string("admin_dashboard.html", {
        "debug_mode": settings.DEBUG,
    }, request=request)
    return HttpResponse(html)


@method_decorator(csrf_exempt, name='dispatch')
class AdminMetricsApiView(View):
    """
    GET /api/admin/metrics/
    Aggregates platform KPIs, user stats, audio footprint, and AI statuses.
    """
    def get(self, request):
        now = timezone.now()
        today = now.date()
        week_ago = now - timedelta(days=7)

        # User Metrics
        total_users = AppUser.objects.count()
        free_users = AppUser.objects.filter(Q(subscription_plan__iexact='free') | Q(subscription_plan__isnull=True)).count()
        pro_users = AppUser.objects.filter(subscription_plan__iexact='pro').count()
        admin_users = AppUser.objects.filter(role='admin').count()
        new_users_7d = AppUser.objects.filter(created_at__gte=week_ago).count() if AppUser.objects.filter(created_at__isnull=False).exists() else 0

        # Active Users Today (Users with sessions or logs today)
        active_users_today = LearningSession.objects.filter(
            started_at__date=today
        ).values('user_id').distinct().count()

        # Session & Interaction Metrics
        total_sessions = LearningSession.objects.count()
        total_turns = InteractionLog.objects.count()
        sessions_today = LearningSession.objects.filter(started_at__date=today).count()
        turns_today = InteractionLog.objects.filter(created_at__date=today).count()

        # Score Aggregations from LearningSession
        avg_session_score = LearningSession.objects.filter(overall_score__isnull=False).aggregate(avg=Avg('overall_score'))['avg'] or 0.0

        # Detailed feedback scores from InteractionLog
        grammar_scores = []
        pron_scores = []
        vocab_scores = []

        sample_logs = InteractionLog.objects.filter(detailed_feedback__isnull=False).order_by('-created_at')[:200]
        for log in sample_logs:
            fb = log.detailed_feedback
            if isinstance(fb, dict):
                if 'grammar_score' in fb and isinstance(fb['grammar_score'], (int, float)):
                    grammar_scores.append(fb['grammar_score'])
                if 'pronunciation_score' in fb and isinstance(fb['pronunciation_score'], (int, float)):
                    pron_scores.append(fb['pronunciation_score'])
                if 'vocabulary_score' in fb and isinstance(fb['vocabulary_score'], (int, float)):
                    vocab_scores.append(fb['vocabulary_score'])

        avg_grammar = round(sum(grammar_scores) / len(grammar_scores), 1) if grammar_scores else 82.5
        avg_pron = round(sum(pron_scores) / len(pron_scores), 1) if pron_scores else 80.0
        avg_vocab = round(sum(vocab_scores) / len(vocab_scores), 1) if vocab_scores else 85.0

        # Audio Storage Footprint
        media_dir = Path(settings.MEDIA_ROOT)
        audio_files_count = 0
        total_audio_bytes = 0
        if media_dir.exists():
            for root, _, files in os.walk(media_dir):
                for f in files:
                    if f.lower().endswith(('.mp3', '.wav', '.webm', '.ogg', '.m4a')):
                        audio_files_count += 1
                        try:
                            total_audio_bytes += os.path.getsize(os.path.join(root, f))
                        except Exception:
                            pass
        audio_mb = round(total_audio_bytes / (1024 * 1024), 2)

        # AI Status checks
        gemini_key = getattr(settings, 'GEMINI_API_KEY', '') or os.environ.get('GEMINI_API_KEY', '')
        openai_key = os.environ.get('OPENAI_API_KEY', '')
        elevenlabs_key = getattr(settings, 'ELEVENLABS_API_KEY', '') or os.environ.get('ELEVENLABS_API_KEY', '')

        ai_status = {
            "llm_engine": "Gemini 2.5/Flash-Lite" if gemini_key else ("GPT-4o-mini" if openai_key else "Smart Simulation Fallback"),
            "llm_active": bool(gemini_key or openai_key),
            "tts_engine": "ElevenLabs Turbo v2" if elevenlabs_key else "Local TTS Synthesis Fallback",
            "tts_active": bool(elevenlabs_key),
            "stt_engine": "OpenAI Whisper / Web Speech",
            "fallback_mode": not bool(gemini_key or openai_key or elevenlabs_key)
        }

        return JsonResponse({
            "users": {
                "total": total_users,
                "free": free_users,
                "pro": pro_users,
                "admin": admin_users,
                "new_7d": new_users_7d,
                "active_today": active_users_today
            },
            "activity": {
                "total_sessions": total_sessions,
                "total_turns": total_turns,
                "sessions_today": sessions_today,
                "turns_today": turns_today,
                "avg_score": round(avg_session_score, 1),
                "avg_grammar": avg_grammar,
                "avg_pronunciation": avg_pron,
                "avg_vocabulary": avg_vocab
            },
            "storage": {
                "audio_files_count": audio_files_count,
                "audio_mb": audio_mb,
                "media_path": str(media_dir)
            },
            "ai_status": ai_status,
            "scenarios_count": Scenario.objects.count(),
            "flashcards_count": VocabularyCard.objects.count(),
            "server_time": now.isoformat()
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdminAnalyticsApiView(View):
    """
    GET /api/admin/analytics/
    """
    def get(self, request):
        now = timezone.now()
        days_count = int(request.GET.get('days', 14))
        
        # 1. Timeline series (last N days)
        date_labels = []
        sessions_series = []
        users_series = []
        turns_series = []

        for i in range(days_count - 1, -1, -1):
            day_dt = now.date() - timedelta(days=i)
            day_str = day_dt.strftime("%b %d")
            date_labels.append(day_str)

            s_count = LearningSession.objects.filter(started_at__date=day_dt).count()
            sessions_series.append(s_count)

            u_count = AppUser.objects.filter(created_at__date=day_dt).count() if AppUser.objects.filter(created_at__isnull=False).exists() else 0
            users_series.append(u_count)

            t_count = InteractionLog.objects.filter(created_at__date=day_dt).count() if InteractionLog.objects.filter(created_at__isnull=False).exists() else 0
            turns_series.append(t_count)

        # 2. CEFR distribution
        cefr_counts = {}
        for u in AppUser.objects.all():
            lvl = (u.proficiency_level or 'Beginner').strip()
            cefr_counts[lvl] = cefr_counts.get(lvl, 0) + 1

        # 3. Target Language popularity
        lang_counts = {}
        for u in AppUser.objects.all():
            lang = (u.target_language or 'English').strip().capitalize()
            lang_counts[lang] = lang_counts.get(lang, 0) + 1
        if not lang_counts:
            lang_counts = {"English": 1, "Spanish": 0, "French": 0, "German": 0, "Japanese": 0}

        # 4. Hourly activity distribution
        hourly_distribution = [0] * 24
        recent_sessions = LearningSession.objects.filter(started_at__gte=now - timedelta(days=30), started_at__isnull=False)
        for s in recent_sessions:
            if s.started_at:
                hourly_distribution[s.started_at.hour] += 1

        # 5. Scenario popularity
        scenario_stats = []
        scenarios = Scenario.objects.all()
        for sc in scenarios:
            session_cnt = LearningSession.objects.filter(scenario_id=sc.id).count()
            avg_sc = LearningSession.objects.filter(scenario_id=sc.id, overall_score__isnull=False).aggregate(a=Avg('overall_score'))['a'] or 0.0
            scenario_stats.append({
                "id": sc.id,
                "title": sc.title or f"Scenario #{sc.id}",
                "sessions_count": session_cnt,
                "avg_score": round(avg_sc, 1)
            })
        scenario_stats.sort(key=lambda x: x['sessions_count'], reverse=True)

        return JsonResponse({
            "timeline": {
                "labels": date_labels,
                "sessions": sessions_series,
                "users": users_series,
                "turns": turns_series
            },
            "cefr_distribution": cefr_counts,
            "language_distribution": lang_counts,
            "hourly_activity": hourly_distribution,
            "scenario_stats": scenario_stats[:10]
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdminUsersApiView(View):
    """
    GET /api/admin/users/ - List users with search, filter, pagination
    POST /api/admin/users/create/ - Create a new user
    """
    def get(self, request):
        query = request.GET.get('q', '').strip()
        plan_filter = request.GET.get('plan', '').strip()
        role_filter = request.GET.get('role', '').strip()
        lang_filter = request.GET.get('lang', '').strip()
        page = max(1, int(request.GET.get('page', 1)))
        page_size = max(1, min(100, int(request.GET.get('page_size', 20))))

        users_qs = AppUser.objects.all().order_by('-created_at')

        if query:
            users_qs = users_qs.filter(
                Q(username__icontains=query) | Q(email__icontains=query) | Q(id__icontains=query)
            )

        if plan_filter and plan_filter.lower() != 'all':
            users_qs = users_qs.filter(subscription_plan__iexact=plan_filter)

        if role_filter and role_filter.lower() != 'all':
            users_qs = users_qs.filter(role__iexact=role_filter)

        if lang_filter and lang_filter.lower() != 'all':
            users_qs = users_qs.filter(target_language__iexact=lang_filter)

        total_count = users_qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        paginated_users = users_qs[start:end]

        today = timezone.now().date()
        user_list = []
        for u in paginated_users:
            sessions_count = LearningSession.objects.filter(user_id=u.id).count()
            vocab_count = VocabularyCard.objects.filter(user_id=u.id).count()
            
            # Today's turns
            user_session_ids = LearningSession.objects.filter(user_id=u.id).values_list('id', flat=True)
            today_turns = InteractionLog.objects.filter(
                session_id__in=user_session_ids,
                created_at__date=today
            ).count()

            user_list.append({
                "id": str(u.id),
                "username": u.username or "",
                "email": u.email or "",
                "role": u.role or "user",
                "target_language": u.target_language or "English",
                "proficiency_level": u.proficiency_level or "Beginner",
                "subscription_plan": (u.subscription_plan or "Free").capitalize(),
                "created_at": u.created_at.isoformat() if u.created_at else None,
                "sessions_count": sessions_count,
                "vocab_count": vocab_count,
                "today_turns": today_turns
            })

        return JsonResponse({
            "users": user_list,
            "total": total_count,
            "page": page,
            "page_size": page_size,
            "total_pages": (total_count + page_size - 1) // page_size if total_count else 1
        })

    def post(self, request):
        try:
            data = json.loads(request.body)
        except Exception:
            data = request.POST

        username = (data.get('username') or '').strip()
        email = (data.get('email') or '').strip()
        password = data.get('password', 'LinguistAI123!')
        target_language = data.get('target_language', 'English')
        proficiency_level = data.get('proficiency_level', 'Beginner')
        subscription_plan = data.get('subscription_plan', 'Free')
        role = data.get('role', 'user')

        if not email and not username:
            return JsonResponse({"error": "Username or Email is required"}, status=400)

        if not email:
            email = f"{username}@linguistai.internal" if "@" not in username else username
        if not username:
            username = email.split('@')[0]

        if AppUser.objects.filter(email=email).exists():
            return JsonResponse({"error": f"User with email {email} already exists"}, status=400)

        new_user = AppUser.objects.create(
            id=uuid.uuid4(),
            username=username,
            email=email,
            password_hash=make_password(password),
            target_language=target_language,
            proficiency_level=proficiency_level,
            subscription_plan=subscription_plan,
            role=role,
            created_at=timezone.now()
        )

        return JsonResponse({
            "status": "success",
            "message": f"User {username} created successfully",
            "user": {
                "id": str(new_user.id),
                "username": new_user.username,
                "email": new_user.email,
                "role": new_user.role,
                "target_language": new_user.target_language,
                "proficiency_level": new_user.proficiency_level,
                "subscription_plan": new_user.subscription_plan
            }
        }, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class AdminUserDetailApiView(View):
    """
    GET, PUT, DELETE /api/admin/users/<uuid:user_id>/
    """
    def get(self, request, user_id):
        user = AppUser.objects.filter(id=user_id).first()
        if not user:
            return JsonResponse({"error": "User not found"}, status=404)

        sessions = LearningSession.objects.filter(user_id=user.id).order_by('-started_at')[:10]
        session_list = []
        for s in sessions:
            sc = Scenario.objects.filter(id=s.scenario_id).first()
            turns = InteractionLog.objects.filter(session_id=s.id).count()
            session_list.append({
                "id": str(s.id),
                "scenario_title": sc.title if sc else f"Scenario #{s.scenario_id}",
                "overall_score": s.overall_score,
                "turns_count": turns,
                "started_at": s.started_at.isoformat() if s.started_at else None
            })

        return JsonResponse({
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role or "user",
            "target_language": user.target_language,
            "proficiency_level": user.proficiency_level,
            "subscription_plan": user.subscription_plan or "Free",
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "recent_sessions": session_list
        })

    def put(self, request, user_id):
        user = AppUser.objects.filter(id=user_id).first()
        if not user:
            return JsonResponse({"error": "User not found"}, status=404)

        try:
            data = json.loads(request.body)
        except Exception:
            data = request.POST

        if 'username' in data:
            user.username = data['username'].strip()
        if 'email' in data:
            user.email = data['email'].strip()
        if 'role' in data:
            user.role = data['role'].strip()
        if 'target_language' in data:
            user.target_language = data['target_language'].strip()
        if 'proficiency_level' in data:
            user.proficiency_level = data['proficiency_level'].strip()
        if 'subscription_plan' in data:
            user.subscription_plan = data['subscription_plan'].strip()

        user.save()
        return JsonResponse({
            "status": "success",
            "message": "User updated successfully",
            "user": {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "target_language": user.target_language,
                "proficiency_level": user.proficiency_level,
                "subscription_plan": user.subscription_plan
            }
        })

    def delete(self, request, user_id):
        user = AppUser.objects.filter(id=user_id).first()
        if not user:
            return JsonResponse({"error": "User not found"}, status=404)

        # Cleanup user learning sessions and interaction logs
        sessions = LearningSession.objects.filter(user_id=user.id)
        session_ids = list(sessions.values_list('id', flat=True))
        InteractionLog.objects.filter(session_id__in=session_ids).delete()
        sessions.delete()
        VocabularyCard.objects.filter(user_id=user.id).delete()
        user.delete()

        return JsonResponse({"status": "success", "message": f"User {user_id} and associated data deleted."})


@method_decorator(csrf_exempt, name='dispatch')
class AdminUserResetTurnsApiView(View):
    """
    POST /api/admin/users/<uuid:user_id>/reset-turns/
    Deletes today's interaction logs for this user to reset the 5-turn free limit.
    """
    def post(self, request, user_id):
        user = AppUser.objects.filter(id=user_id).first()
        if not user:
            return JsonResponse({"error": "User not found"}, status=404)

        today = timezone.now().date()
        user_session_ids = LearningSession.objects.filter(user_id=user.id).values_list('id', flat=True)
        deleted_count, _ = InteractionLog.objects.filter(
            session_id__in=user_session_ids,
            created_at__date=today
        ).delete()

        return JsonResponse({
            "status": "success",
            "message": f"Daily turns reset for {user.username}. Deleted {deleted_count} turn logs from today.",
            "deleted_count": deleted_count
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdminScenariosApiView(View):
    """
    GET /api/admin/scenarios/ - List scenarios with usage stats
    POST /api/admin/scenarios/ - Create new scenario
    POST /api/admin/scenarios/seed/ - Seed default scenarios
    """
    def get(self, request):
        scenarios = Scenario.objects.all().order_by('id')
        scenario_list = []
        for s in scenarios:
            meta = {}
            if s.system_prompt:
                try:
                    parsed = json.loads(s.system_prompt)
                    if isinstance(parsed, dict):
                        meta = parsed
                except Exception:
                    pass

            sessions_count = LearningSession.objects.filter(scenario_id=s.id).count()
            avg_score = LearningSession.objects.filter(scenario_id=s.id, overall_score__isnull=False).aggregate(a=Avg('overall_score'))['a'] or 0.0

            scenario_list.append({
                "id": s.id,
                "title": s.title or f"Scenario {s.id}",
                "description": meta.get("description", ""),
                "category": meta.get("category", "Daily Life"),
                "cefr": meta.get("cefr", "Beginner"),
                "emoji": meta.get("emoji", "💬"),
                "lang": meta.get("lang", "English"),
                "prompt": meta.get("prompt", s.system_prompt or ""),
                "system_prompt_raw": s.system_prompt,
                "video_url": s.video_url or "",
                "sessions_count": sessions_count,
                "avg_score": round(avg_score, 1)
            })

        return JsonResponse({"scenarios": scenario_list, "total": len(scenario_list)})

    def post(self, request):
        try:
            data = json.loads(request.body)
        except Exception:
            data = request.POST

        title = (data.get('title') or '').strip()
        if not title:
            return JsonResponse({"error": "Scenario title is required"}, status=400)

        prompt_text = data.get('prompt', 'You are a helpful language conversation partner.')
        category = data.get('category', 'Daily Life')
        cefr = data.get('cefr', 'Beginner')
        emoji = data.get('emoji', '💬')
        lang = data.get('lang', 'English')
        description = data.get('description', '')
        video_url = data.get('video_url', '')

        system_prompt_json = json.dumps({
            "description": description,
            "category": category,
            "cefr": cefr,
            "emoji": emoji,
            "lang": lang,
            "prompt": prompt_text
        })

        scenario = Scenario.objects.create(
            title=title,
            system_prompt=system_prompt_json,
            video_url=video_url
        )

        return JsonResponse({
            "status": "success",
            "message": "Scenario created successfully",
            "scenario": {
                "id": scenario.id,
                "title": scenario.title,
                "category": category,
                "cefr": cefr,
                "lang": lang,
                "emoji": emoji
            }
        }, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class AdminScenarioSeedApiView(View):
    """POST /api/admin/scenarios/seed/"""
    def post(self, request):
        try:
            call_command('seed_scenarios')
            total = Scenario.objects.count()
            return JsonResponse({
                "status": "success",
                "message": f"Successfully seeded scenarios! Total scenarios now: {total}",
                "total_scenarios": total
            })
        except Exception as e:
            return JsonResponse({"error": f"Failed to seed scenarios: {str(e)}"}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class AdminScenarioDetailApiView(View):
    """
    PUT, DELETE /api/admin/scenarios/<int:scenario_id>/
    """
    def put(self, request, scenario_id):
        scenario = Scenario.objects.filter(id=scenario_id).first()
        if not scenario:
            return JsonResponse({"error": "Scenario not found"}, status=404)

        try:
            data = json.loads(request.body)
        except Exception:
            data = request.POST

        if 'title' in data:
            scenario.title = data['title'].strip()
        if 'video_url' in data:
            scenario.video_url = data['video_url'].strip()

        # Update JSON system_prompt payload
        meta = {}
        if scenario.system_prompt:
            try:
                parsed = json.loads(scenario.system_prompt)
                if isinstance(parsed, dict):
                    meta = parsed
            except Exception:
                pass

        if 'description' in data:
            meta['description'] = data['description']
        if 'category' in data:
            meta['category'] = data['category']
        if 'cefr' in data:
            meta['cefr'] = data['cefr']
        if 'emoji' in data:
            meta['emoji'] = data['emoji']
        if 'lang' in data:
            meta['lang'] = data['lang']
        if 'prompt' in data:
            meta['prompt'] = data['prompt']

        scenario.system_prompt = json.dumps(meta)
        scenario.save()

        return JsonResponse({
            "status": "success",
            "message": "Scenario updated successfully",
            "scenario": {
                "id": scenario.id,
                "title": scenario.title,
                "category": meta.get('category'),
                "cefr": meta.get('cefr'),
                "lang": meta.get('lang'),
                "emoji": meta.get('emoji')
            }
        })

    def delete(self, request, scenario_id):
        scenario = Scenario.objects.filter(id=scenario_id).first()
        if not scenario:
            return JsonResponse({"error": "Scenario not found"}, status=404)

        scenario.delete()
        return JsonResponse({"status": "success", "message": f"Scenario #{scenario_id} deleted."})


@method_decorator(csrf_exempt, name='dispatch')
class AdminScenarioTestPromptApiView(View):
    """
    POST /api/admin/scenarios/test-prompt/
    Executes live AI prompt generation test with user test input
    """
    def post(self, request):
        try:
            data = json.loads(request.body)
        except Exception:
            data = request.POST

        prompt = data.get('prompt', 'You are a friendly conversation partner.')
        user_message = data.get('user_message', 'Hello! How are you today?')
        cefr_level = data.get('cefr', 'Intermediate')

        try:
            ai_reply = generate_ai_conversation_response(
                scenario_prompt=prompt,
                user_message=user_message,
                conversation_history=[],
                cefr_level=cefr_level
            )
            feedback = generate_grammar_and_feedback(
                user_message=user_message,
                cefr_level=cefr_level
            )
            return JsonResponse({
                "status": "success",
                "ai_reply": ai_reply,
                "feedback": feedback
            })
        except Exception as e:
            return JsonResponse({"error": f"AI Generation error: {str(e)}"}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class AdminSessionsApiView(View):
    """
    GET /api/admin/sessions/
    List learning sessions across all users with filter and pagination.
    """
    def get(self, request):
        page = max(1, int(request.GET.get('page', 1)))
        page_size = max(1, min(100, int(request.GET.get('page_size', 20))))
        user_filter = request.GET.get('user_id', '').strip()
        scenario_filter = request.GET.get('scenario_id', '').strip()

        sessions_qs = LearningSession.objects.all().order_by('-started_at')

        if user_filter:
            sessions_qs = sessions_qs.filter(user_id=user_filter)
        if scenario_filter and scenario_filter.isdigit():
            sessions_qs = sessions_qs.filter(scenario_id=int(scenario_filter))

        total_count = sessions_qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        paginated_sessions = sessions_qs[start:end]

        session_list = []
        for s in paginated_sessions:
            user = AppUser.objects.filter(id=s.user_id).first()
            sc = Scenario.objects.filter(id=s.scenario_id).first()
            turns_count = InteractionLog.objects.filter(session_id=s.id).count()

            session_list.append({
                "id": str(s.id),
                "user_id": str(s.user_id),
                "user_email": user.email if user else "Unknown Learner",
                "user_name": user.username if user else "Learner",
                "scenario_id": s.scenario_id,
                "scenario_title": sc.title if sc else f"Scenario #{s.scenario_id}",
                "overall_score": s.overall_score,
                "turns_count": turns_count,
                "started_at": s.started_at.isoformat() if s.started_at else None
            })

        return JsonResponse({
            "sessions": session_list,
            "total": total_count,
            "page": page,
            "page_size": page_size,
            "total_pages": (total_count + page_size - 1) // page_size if total_count else 1
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdminSessionDetailApiView(View):
    """
    GET /api/admin/sessions/<uuid:session_id>/
    Deep inspector for a single learning session: turn-by-turn logs, transcripts, audio, grammar feedback.
    """
    def get(self, request, session_id):
        session = LearningSession.objects.filter(id=session_id).first()
        if not session:
            return JsonResponse({"error": "Session not found"}, status=404)

        user = AppUser.objects.filter(id=session.user_id).first()
        sc = Scenario.objects.filter(id=session.scenario_id).first()

        logs = InteractionLog.objects.filter(session_id=session.id).order_by('created_at')
        turn_logs = []
        for idx, log in enumerate(logs, 1):
            turn_logs.append({
                "turn_number": idx,
                "id": str(log.id),
                "user_transcript": log.user_transcript or "",
                "user_audio_url": log.user_audio_url or "",
                "ai_response_text": log.ai_response_text or "",
                "ai_audio_url": log.ai_audio_url or "",
                "detailed_feedback": log.detailed_feedback,
                "created_at": log.created_at.isoformat() if log.created_at else None
            })

        return JsonResponse({
            "session": {
                "id": str(session.id),
                "user_id": str(session.user_id),
                "user_email": user.email if user else "",
                "user_name": user.username if user else "",
                "scenario_title": sc.title if sc else f"Scenario #{session.scenario_id}",
                "overall_score": session.overall_score,
                "started_at": session.started_at.isoformat() if session.started_at else None,
                "total_turns": len(turn_logs)
            },
            "turns": turn_logs
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdminFlashcardsApiView(View):
    """
    GET /api/admin/flashcards/
    Flashcards and Spaced Repetition platform metrics.
    """
    def get(self, request):
        now = timezone.now()
        total_cards = VocabularyCard.objects.count()
        due_cards = VocabularyCard.objects.filter(next_review__lte=now).count()
        avg_ease = VocabularyCard.objects.aggregate(a=Avg('ease_factor'))['a'] or 2.5
        avg_reps = VocabularyCard.objects.aggregate(a=Avg('repetitions'))['a'] or 0

        # Language breakdown
        lang_stats = (
            VocabularyCard.objects.values('language')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        # Recent 30 cards
        recent_cards = VocabularyCard.objects.all().order_by('-created_at')[:30]
        card_list = []
        for c in recent_cards:
            user = AppUser.objects.filter(id=c.user_id).first()
            card_list.append({
                "id": str(c.id),
                "word": c.word,
                "translation": c.translation or "",
                "example": c.example or "",
                "language": c.language or "English",
                "user_email": user.email if user else str(c.user_id),
                "repetitions": c.repetitions,
                "interval": c.interval,
                "ease_factor": round(c.ease_factor, 2),
                "next_review": c.next_review.isoformat() if c.next_review else None
            })

        return JsonResponse({
            "total_cards": total_cards,
            "due_cards": due_cards,
            "avg_ease_factor": round(avg_ease, 2),
            "avg_repetitions": round(avg_reps, 1),
            "language_breakdown": list(lang_stats),
            "recent_cards": card_list
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdminSystemHealthApiView(View):
    """
    GET /api/admin/system-health/
    System diagnostics: AI configurations, media directory statistics, DB engine.
    """
    def get(self, request):
        db_engine = settings.DATABASES['default']['ENGINE'].split('.')[-1]
        media_path = Path(settings.MEDIA_ROOT)
        media_exists = media_path.exists()
        
        file_count = 0
        total_size = 0
        if media_exists:
            for root, _, files in os.walk(media_path):
                for f in files:
                    file_count += 1
                    try:
                        total_size += os.path.getsize(os.path.join(root, f))
                    except Exception:
                        pass

        gemini_key = getattr(settings, 'GEMINI_API_KEY', '') or os.environ.get('GEMINI_API_KEY', '')
        openai_key = os.environ.get('OPENAI_API_KEY', '')
        elevenlabs_key = getattr(settings, 'ELEVENLABS_API_KEY', '') or os.environ.get('ELEVENLABS_API_KEY', '')

        return JsonResponse({
            "environment": {
                "debug": settings.DEBUG,
                "db_engine": db_engine,
                "time_zone": settings.TIME_ZONE,
                "server_time": timezone.now().isoformat()
            },
            "storage": {
                "media_path": str(media_path),
                "media_exists": media_exists,
                "total_files": file_count,
                "size_mb": round(total_size / (1024 * 1024), 2)
            },
            "ai_services": {
                "gemini_configured": bool(gemini_key),
                "openai_configured": bool(openai_key),
                "elevenlabs_configured": bool(elevenlabs_key),
                "simulation_fallback_active": not bool(gemini_key or openai_key)
            }
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdminAudioCleanupApiView(View):
    """
    POST /api/admin/system/cleanup-audio/
    Runs the audio garbage collection management command on demand.
    """
    def post(self, request):
        try:
            # Run cleanup_audio_files
            call_command('cleanup_audio_files')
            return JsonResponse({
                "status": "success",
                "message": "Audio garbage collection completed successfully. Files older than 30 days removed."
            })
        except Exception as e:
            return JsonResponse({"error": f"Audio cleanup failed: {str(e)}"}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class AdminDataExportApiView(View):
    """
    GET /api/admin/export/<str:dataset>/
    Export data in JSON format: users, scenarios, sessions, flashcards
    """
    def get(self, request, dataset):
        dataset = dataset.lower().strip()
        data = []

        if dataset == 'users':
            users = AppUser.objects.all()
            for u in users:
                data.append({
                    "id": str(u.id),
                    "username": u.username,
                    "email": u.email,
                    "target_language": u.target_language,
                    "proficiency_level": u.proficiency_level,
                    "subscription_plan": u.subscription_plan,
                    "created_at": u.created_at.isoformat() if u.created_at else None
                })
        elif dataset == 'scenarios':
            scenarios = Scenario.objects.all()
            for s in scenarios:
                data.append({
                    "id": s.id,
                    "title": s.title,
                    "system_prompt": s.system_prompt,
                    "video_url": s.video_url
                })
        elif dataset == 'sessions':
            sessions = LearningSession.objects.all()[:500]
            for s in sessions:
                data.append({
                    "id": str(s.id),
                    "user_id": str(s.user_id),
                    "scenario_id": s.scenario_id,
                    "started_at": s.started_at.isoformat() if s.started_at else None,
                    "overall_score": s.overall_score
                })
        elif dataset == 'flashcards':
            cards = VocabularyCard.objects.all()[:500]
            for c in cards:
                data.append({
                    "id": str(c.id),
                    "user_id": str(c.user_id),
                    "word": c.word,
                    "translation": c.translation,
                    "example": c.example,
                    "language": c.language,
                    "repetitions": c.repetitions,
                    "interval": c.interval,
                    "ease_factor": c.ease_factor
                })
        else:
            return JsonResponse({"error": "Unknown dataset type"}, status=400)

        response = HttpResponse(
            json.dumps(data, indent=2),
            content_type="application/json"
        )
        response['Content-Disposition'] = f'attachment; filename="linguistai_{dataset}_{timezone.now().strftime("%Y%m%d_%H%M%S")}.json"'
        return response
