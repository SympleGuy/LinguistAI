import json
import uuid
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.core.management import call_command

from myapp.models import User as AppUser, Scenario, LearningSession, InteractionLog


class AuthViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("api_register")
        self.login_url = reverse("api_login")
        self.me_url = reverse("api_me")
        self.logout_url = reverse("api_logout")

    def test_user_registration_and_login_flow(self):
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

