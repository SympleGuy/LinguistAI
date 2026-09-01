from django.db import models
import uuid


class User(models.Model):
    """
    User model matching specification in 0001_initial.py with RBAC role support
    """
    ROLE_CHOICES = [
        ('user', 'Learner / User'),
        ('admin', 'Admin'),
    ]

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)
    username = models.CharField(blank=True, max_length=255, null=True)
    email = models.EmailField(blank=True, max_length=255, null=True)
    password_hash = models.CharField(blank=True, max_length=255, null=True)  # Stores hashed password from Supabase
    target_language = models.CharField(blank=True, max_length=255, null=True)
    proficiency_level = models.CharField(blank=True, max_length=255, null=True)
    subscription_plan = models.CharField(blank=True, max_length=255, null=True)
    role = models.CharField(blank=True, max_length=50, default='user', choices=ROLE_CHOICES)
    created_at = models.DateTimeField(blank=True, null=True)


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'users'

    def __str__(self):
        return self.username or f"User {self.id}"


class Scenario(models.Model):
    """
    Scenario model matching exactly the specification in 0001_initial.py
    """
    id = models.AutoField(primary_key=True, serialize=False)
    title = models.CharField(blank=True, max_length=255, null=True)
    system_prompt = models.TextField(blank=True, null=True)
    video_url = models.CharField(blank=True, max_length=500, null=True)

    class Meta:
        verbose_name = 'Scenario'
        verbose_name_plural = 'Scenarios'
        db_table = 'scenarios'

    def __str__(self):
        return self.title or f"Scenario {self.id}"


class LearningSession(models.Model):
    """
    LearningSession model matching exactly the specification in 0001_initial.py
    """
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)
    user_id = models.UUIDField()  # Reference to User.id
    scenario_id = models.IntegerField()  # Reference to Scenario.id
    started_at = models.DateTimeField(blank=True, null=True)
    overall_score = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = 'Learning Session'
        verbose_name_plural = 'Learning Sessions'
        db_table = 'learning_sessions'
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['started_at']),
        ]

    def __str__(self):
        return f"Session {self.id} for User {self.user_id}, Scenario {self.scenario_id}"


class InteractionLog(models.Model):
    """
    InteractionLog model matching exactly the specification in 0001_initial.py
    """
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)
    session_id = models.UUIDField()  # Reference to LearningSession.id
    user_audio_url = models.CharField(blank=True, max_length=500, null=True)
    user_transcript = models.TextField(blank=True, null=True)
    ai_audio_url = models.CharField(blank=True, max_length=500, null=True)
    ai_response_text = models.TextField(blank=True, null=True)
    detailed_feedback = models.JSONField(blank=True, null=True)  # JSONField for feedback
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Interaction Log'
        verbose_name_plural = 'Interaction Logs'
        db_table = 'interaction_logs'
        indexes = [
            models.Index(fields=['session_id']),
            models.Index(fields=['created_at']),
        ]


    def __str__(self):
        return f"Interaction {self.id} for Session {self.session_id}"

from django.utils import timezone

class VocabularyCard(models.Model):
    """
    VocabularyCard model for Anki spaced repetition
    """
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user_id = models.UUIDField()
    word = models.CharField(max_length=255)
    translation = models.CharField(max_length=255, blank=True, null=True)
    example = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=50, default='English')
    
    # SuperMemo-2 Algorithm Fields
    next_review = models.DateTimeField(default=timezone.now)
    interval = models.IntegerField(default=0)  # in days
    ease_factor = models.FloatField(default=2.5)
    repetitions = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Vocabulary Card'
        verbose_name_plural = 'Vocabulary Cards'
        db_table = 'vocabulary_cards'
        indexes = [
            models.Index(fields=['user_id', 'language', 'next_review']),
        ]

    def __str__(self):
        return f"{self.word} ({self.user_id})"
