import json
import uuid
from unittest.mock import patch, MagicMock
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.utils import timezone
from django.core.management import call_command
from django.http import HttpResponse

from myapp.models import User as AppUser, Scenario, LearningSession, InteractionLog
from myapp.middleware import ApiAuthenticationMiddleware, GlobalExceptionHandlerMiddleware


class AuthViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("api_register")
        self.login_url = reverse("api_login")
        self.me_url = reverse("api_me")
        self.logout_url = reverse("api_logout")

    @patch("myapp.views.supabase")
    @patch("myapp.views.supabase_admin")
    def test_user_registration_and_login_flow(self, mock_admin, mock_supabase):
        # Mock Supabase Auth
        mock_auth_user = MagicMock()
        mock_auth_user.id = str(uuid.uuid4())
        mock_supabase.auth.sign_up.return_value = MagicMock(user=mock_auth_user)

        # 1. Register new user
        reg_payload = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "SecurePassword123",
            "proficiency_level": "Intermediate",
            "target_language": "French"
        }
        res = self.client.post(self.register_url, data=json.dumps(reg_payload), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        user_id = data["user"]["id"]

        # 2. Check /api/auth/me/
        res_me = self.client.get(self.me_url)
        self.assertEqual(res_me.status_code, 200)
        self.assertTrue(res_me.json()["authenticated"])

        # 3. Logout
        res_logout = self.client.post(self.logout_url, content_type="application/json")
        self.assertEqual(res_logout.status_code, 200)

        # 4. Login
        login_payload = {
            "email": "testuser@example.com",
            "password": "SecurePassword123"
        }
        res_login = self.client.post(self.login_url, data=json.dumps(login_payload), content_type="application/json")
        self.assertEqual(res_login.status_code, 200)
        self.assertEqual(res_login.json()["user"]["id"], user_id)


class ScenarioViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.scenario = Scenario.objects.create(
            id=1,
            title="Ordering Coffee in Paris",
            system_prompt=json.dumps({
                "description": "Practice ordering cafe au lait.",
                "category": "Food & Dining",
                "cefr": "Beginner",
                "emoji": "☕",
                "lang": "French",
                "prompt": "You are a friendly Parisian barista."
            })
        )

    def test_list_and_detail_scenarios(self):
        res = self.client.get(reverse("scenarios_list"))
        self.assertEqual(res.status_code, 200)
        scenarios = res.json()
        self.assertTrue(len(scenarios) > 0)
        self.assertEqual(scenarios[0]["title"], "Ordering Coffee in Paris")

        res_detail = self.client.get(reverse("scenario_detail", kwargs={"scenario_id": 1}))
        self.assertEqual(res_detail.status_code, 200)
        self.assertEqual(res_detail.json()["category"], "Food & Dining")


class LearningSessionAndResponseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = AppUser.objects.create(
            username="sessionuser@example.com",
            password_hash="pbkdf2_sha256$hashed",
            target_language="French",
            proficiency_level="Beginner",
            subscription_plan="Free",
            created_at=timezone.now()
        )
        self.scenario = Scenario.objects.create(
            id=1,
            title="Café Ordering",
            system_prompt="You are a French barista."
        )
        # Authenticate session
        session = self.client.session
        session["supabase_user_id"] = str(self.user.id)
        session.save()

    def test_start_session_and_submit_response(self):
        # Start session
        start_payload = {
            "user_id": str(self.user.id),
            "scenario_id": 1
        }
        res_start = self.client.post(
            reverse("start_session"),
            data=json.dumps(start_payload),
            content_type="application/json"
        )
        self.assertEqual(res_start.status_code, 200)
        session_id = res_start.json()["session_id"]

        # Submit text response
        resp_payload = {
            "user_transcript": "Bonjour, un café s'il vous plaît!"
        }
        res_resp = self.client.post(
            reverse("submit_response", kwargs={"session_id": session_id}),
            data=json.dumps(resp_payload),
            content_type="application/json"
        )
        self.assertEqual(res_resp.status_code, 200)
        resp_data = res_resp.json()
        self.assertIn("ai_response", resp_data)
        self.assertIn("feedback", resp_data)

        # Verify InteractionLog stored in database
        logs = InteractionLog.objects.filter(session_id=session_id)
        self.assertEqual(logs.count(), 1)
        self.assertEqual(logs.first().user_transcript, "Bonjour, un café s'il vous plaît!")


class TurnLimitTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.free_user = AppUser.objects.create(
            username="freeuser@example.com",
            subscription_plan="Free",
            created_at=timezone.now()
        )
        self.scenario = Scenario.objects.create(id=2, title="General Practice")
        self.session = LearningSession.objects.create(
            user_id=self.free_user.id,
            scenario_id=self.scenario.id,
            started_at=timezone.now()
        )
        session = self.client.session
        session["supabase_user_id"] = str(self.free_user.id)
        session.save()

    def test_five_turn_daily_limit_enforcement(self):
        url = reverse("submit_response", kwargs={"session_id": str(self.session.id)})

        # Perform 5 turns (should succeed)
        for i in range(5):
            res = self.client.post(
                url,
                data=json.dumps({"user_transcript": f"Turn number {i+1}"}),
                content_type="application/json"
            )
            self.assertEqual(res.status_code, 200)

        # Perform 6th turn (should be blocked with HTTP 403)
        res_sixth = self.client.post(
            url,
            data=json.dumps({"user_transcript": "Turn number 6"}),
            content_type="application/json"
        )
        self.assertEqual(res_sixth.status_code, 403)
        data = res_sixth.json()
        self.assertTrue(data.get("limit_reached"))
        self.assertEqual(data.get("daily_limit"), 5)


class GarbageCollectionCommandTestCase(TestCase):
    def test_cleanup_command(self):
        call_command("cleanup_audio_files", "--days", 30)


class UserProfileUpdateTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = AppUser.objects.create(
            username="profiletest",
            email="profiletest@example.com",
            target_language="English",
            proficiency_level="Beginner",
            created_at=timezone.now()
        )
        session = self.client.session
        session["supabase_user_id"] = str(self.user.id)
        session.save()

    @patch("myapp.views.supabase_admin", None)
    @patch("myapp.views.supabase", None)
    def test_update_profile(self):
        url = reverse("user_profile_update", kwargs={"user_id": str(self.user.id)})
        payload = {
            "target_language": "Spanish",
            "proficiency_level": "Advanced",
            "username": "profiletest_updated"
        }
        res = self.client.post(url, data=json.dumps(payload), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["user"]["target_language"], "Spanish")
        self.assertEqual(data["user"]["proficiency_level"], "Advanced")

        # Verify DB updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.target_language, "Spanish")
        self.assertEqual(self.user.proficiency_level, "Advanced")


class MiddlewareSecurityTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = AppUser.objects.create(
            username="middlewareuser",
            email="middleware@example.com",
            subscription_plan="Free",
            created_at=timezone.now()
        )
        self.scenario = Scenario.objects.create(id=10, title="Middleware Test Scenario")

    def test_unauthenticated_protected_api_returns_401(self):
        """Unauthenticated requests to protected endpoints return 401 Unauthorized"""
        start_payload = {"user_id": str(self.user.id), "scenario_id": 10}
        res = self.client.post(
            reverse("start_session"),
            data=json.dumps(start_payload),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 401)
        data = res.json()
        self.assertEqual(data.get("code"), 401)
        self.assertIn("Unauthorized", data.get("error"))

    def test_public_api_endpoints_accessible_without_auth(self):
        """Public API endpoints like scenarios and login do not require session"""
        res_scenarios = self.client.get(reverse("scenarios_list"))
        self.assertEqual(res_scenarios.status_code, 200)

    def test_authenticated_api_request_allowed(self):
        """Authenticated requests with session are allowed to proceed"""
        session = self.client.session
        session["supabase_user_id"] = str(self.user.id)
        session.save()

        start_payload = {"user_id": str(self.user.id), "scenario_id": 10}
        res = self.client.post(
            reverse("start_session"),
            data=json.dumps(start_payload),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 200)

    def test_global_exception_handler_middleware(self):
        """Global exception handler catches errors and returns 500 JSON without traceback"""
        middleware = GlobalExceptionHandlerMiddleware(lambda req: None)
        request = self.factory.get("/api/test-error/")
        exception = ValueError("Simulated crash")
        response = middleware.process_exception(request, exception)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(data.get("code"), 500)
        self.assertIn("Internal server error", data.get("error"))


class UserAnalyticsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = AppUser.objects.create(
            username="analyticstest",
            email="analytics@example.com",
            target_language="French",
            proficiency_level="Intermediate",
            subscription_plan="Free",
            created_at=timezone.now()
        )
        self.scenario = Scenario.objects.create(id=20, title="Analytics Scenario")
        self.session = LearningSession.objects.create(
            user_id=self.user.id,
            scenario_id=self.scenario.id,
            started_at=timezone.now()
        )
        self.log = InteractionLog.objects.create(
            session_id=self.session.id,
            user_transcript="Bonjour, comment ca va?",
            ai_response_text="Bonjour! Je vais tres bien.",
            detailed_feedback={
                "grammar_score": 88,
                "pronunciation_score": 85,
                "vocabulary_score": 82,
                "corrections": [{"explanation": "Missing accent on ça"}]
            },
            created_at=timezone.now()
        )
        # Authenticate session
        session = self.client.session
        session["supabase_user_id"] = str(self.user.id)
        session.save()

    def test_get_analytics_success(self):
        url = reverse("user_analytics", kwargs={"user_id": str(self.user.id)})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["user_id"], str(self.user.id))
        self.assertIn("days", data)
        self.assertIn("grammar_series", data)
        self.assertIn("pronunciation_series", data)
        self.assertEqual(len(data["days"]), 7)
        self.assertEqual(data["total_sessions"], 1)
        self.assertEqual(data["total_turns"], 1)
        self.assertIn("top_corrections", data)

    def test_get_analytics_nonexistent_user_returns_404(self):
        fake_uuid = str(uuid.uuid4())
        session = self.client.session
        session["supabase_user_id"] = fake_uuid
        session.save()

        url = reverse("user_analytics", kwargs={"user_id": fake_uuid})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 404)


class OAuthSyncTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.oauth_url = reverse("api_oauth_sync")

    def test_sync_new_oauth_user_success(self):
        fake_supabase_id = str(uuid.uuid4())
        payload = {
            "supabase_user_id": fake_supabase_id,
            "email": "googletester@example.com",
            "username": "Google Tester"
        }
        res = self.client.post(self.oauth_url, data=json.dumps(payload), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["user"]["email"], "googletester@example.com")
        self.assertEqual(data["user"]["username"], "Google Tester")

        # Verify session is established
        self.assertEqual(self.client.session.get("supabase_user_id"), str(data["user"]["id"]))

        # Verify user is saved in DB
        db_user = AppUser.objects.filter(email="googletester@example.com").first()
        self.assertIsNotNone(db_user)
        self.assertEqual(db_user.username, "Google Tester")

    def test_sync_existing_oauth_user_success(self):
        existing_user = AppUser.objects.create(
            username="existinggoogle",
            email="existing@example.com",
            target_language="Spanish",
            proficiency_level="Advanced",
            created_at=timezone.now()
        )
        payload = {
            "supabase_user_id": str(existing_user.id),
            "email": "existing@example.com",
            "username": "existinggoogle"
        }
        res = self.client.post(self.oauth_url, data=json.dumps(payload), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["user"]["target_language"], "Spanish")
        self.assertEqual(data["user"]["proficiency_level"], "Advanced")

    def test_sync_missing_identity_fails(self):
        payload = {}
        res = self.client.post(self.oauth_url, data=json.dumps(payload), content_type="application/json")
        self.assertEqual(res.status_code, 400)


class AdminDashboardViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = AppUser.objects.create(
            username="adminlearner",
            email="adminlearner@example.com",
            target_language="French",
            proficiency_level="Intermediate",
            subscription_plan="Free",
            created_at=timezone.now()
        )
        # Establish session for test client
        session = self.client.session
        session["supabase_user_id"] = str(self.user.id)
        session["is_admin"] = True
        session.save()

        self.scenario = Scenario.objects.create(
            title="Ordering at a Bakery",
            system_prompt=json.dumps({
                "description": "Bakery practice",
                "category": "Food & Dining",
                "cefr": "Beginner",
                "emoji": "🥐",
                "lang": "French",
                "prompt": "You are a baker."
            })
        )
        self.session = LearningSession.objects.create(
            user_id=self.user.id,
            scenario_id=self.scenario.id,
            started_at=timezone.now(),
            overall_score=88.5
        )
        self.log = InteractionLog.objects.create(
            session_id=self.session.id,
            user_transcript="Je voudrais un croissant s'il vous plait.",
            ai_response_text="Bien sur, voila un croissant chaud!",
            detailed_feedback={
                "grammar_score": 92,
                "pronunciation_score": 85,
                "vocabulary_score": 90,
                "corrections": [],
                "suggestions": ["Great sentence structure!"]
            },
            created_at=timezone.now()
        )

    def test_admin_dashboard_renders(self):
        res = self.client.get(reverse("admin_dashboard"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "LinguistAI")
        self.assertContains(res, "Admin Portal")

    def test_admin_metrics_api(self):
        res = self.client.get(reverse("admin_metrics"))
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("users", data)
        self.assertIn("activity", data)
        self.assertIn("storage", data)
        self.assertIn("ai_status", data)
        self.assertGreaterEqual(data["users"]["total"], 1)
        self.assertGreaterEqual(data["activity"]["total_sessions"], 1)

    def test_admin_analytics_api(self):
        res = self.client.get(reverse("admin_analytics") + "?days=7")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("timeline", data)
        self.assertIn("cefr_distribution", data)
        self.assertIn("language_distribution", data)
        self.assertEqual(len(data["timeline"]["labels"]), 7)

    def test_admin_users_crud_and_turn_reset(self):
        # 1. List users
        res = self.client.get(reverse("admin_users"))
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreaterEqual(data["total"], 1)

        # 2. Create user
        new_payload = {
            "username": "newadminuser",
            "email": "newadmin@example.com",
            "target_language": "German",
            "proficiency_level": "A2",
            "subscription_plan": "Pro"
        }
        res_create = self.client.post(
            reverse("admin_users_create"),
            data=json.dumps(new_payload),
            content_type="application/json"
        )
        self.assertEqual(res_create.status_code, 201)
        new_user_id = res_create.json()["user"]["id"]

        # 3. Update user
        update_payload = {"subscription_plan": "Free", "target_language": "Japanese"}
        res_update = self.client.put(
            reverse("admin_user_detail", kwargs={"user_id": new_user_id}),
            data=json.dumps(update_payload),
            content_type="application/json"
        )
        self.assertEqual(res_update.status_code, 200)
        self.assertEqual(res_update.json()["user"]["target_language"], "Japanese")

        # 4. Reset turns
        res_reset = self.client.post(
            reverse("admin_user_reset_turns", kwargs={"user_id": self.user.id})
        )
        self.assertEqual(res_reset.status_code, 200)
        self.assertIn("Daily turns reset", res_reset.json()["message"])

        # 5. Delete user
        res_del = self.client.delete(
            reverse("admin_user_detail", kwargs={"user_id": new_user_id})
        )
        self.assertEqual(res_del.status_code, 200)
        self.assertFalse(AppUser.objects.filter(id=new_user_id).exists())

    def test_admin_scenarios_crud(self):
        # 1. List scenarios
        res = self.client.get(reverse("admin_scenarios"))
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(res.json()["total"], 1)

        # 2. Create scenario
        create_payload = {
            "title": "Booking a Train in Munich",
            "emoji": "🚆",
            "category": "Travel",
            "cefr": "Intermediate",
            "lang": "German",
            "description": "Practice buying train tickets.",
            "prompt": "You are a Deutsche Bahn ticket agent."
        }
        res_create = self.client.post(
            reverse("admin_scenarios"),
            data=json.dumps(create_payload),
            content_type="application/json"
        )
        self.assertEqual(res_create.status_code, 201)
        sc_id = res_create.json()["scenario"]["id"]

        # 3. Update scenario
        res_update = self.client.put(
            reverse("admin_scenario_detail", kwargs={"scenario_id": sc_id}),
            data=json.dumps({"title": "Booking an Express Train in Munich"}),
            content_type="application/json"
        )
        self.assertEqual(res_update.status_code, 200)
        self.assertEqual(res_update.json()["scenario"]["title"], "Booking an Express Train in Munich")

        # 4. Delete scenario
        res_del = self.client.delete(
            reverse("admin_scenario_detail", kwargs={"scenario_id": sc_id})
        )
        self.assertEqual(res_del.status_code, 200)
        self.assertFalse(Scenario.objects.filter(id=sc_id).exists())

    def test_admin_sessions_and_inspector(self):
        # List sessions
        res = self.client.get(reverse("admin_sessions"))
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(res.json()["total"], 1)

        # Inspect session
        res_detail = self.client.get(
            reverse("admin_session_detail", kwargs={"session_id": self.session.id})
        )
        self.assertEqual(res_detail.status_code, 200)
        data = res_detail.json()
        self.assertEqual(data["session"]["scenario_title"], "Ordering at a Bakery")
        self.assertEqual(len(data["turns"]), 1)
        self.assertEqual(data["turns"][0]["detailed_feedback"]["grammar_score"], 92)

    def test_admin_system_health_and_export(self):
        # System health
        res_health = self.client.get(reverse("admin_system_health"))
        self.assertEqual(res_health.status_code, 200)
        self.assertIn("ai_services", res_health.json())

        # Export users JSON
        res_export = self.client.get(reverse("admin_data_export", kwargs={"dataset": "users"}))
        self.assertEqual(res_export.status_code, 200)
        self.assertEqual(res_export["Content-Type"], "application/json")
        exported_users = json.loads(res_export.content)
        self.assertTrue(any(u["email"] == "adminlearner@example.com" for u in exported_users))

    def test_user_role_assignment_and_management_command(self):
        # 1. Verify default role is user
        self.assertEqual(self.user.role, "user")

        # 2. Promote to admin via management command
        call_command("set_user_role", self.user.email, "admin")
        self.user.refresh_from_db()
        self.assertEqual(self.user.role, "admin")

        # 3. Demote back to user via management command
        call_command("set_user_role", self.user.email, "user")
        self.user.refresh_from_db()
        self.assertEqual(self.user.role, "user")




