from django.contrib import admin
from django.utils.html import format_html
import json
from .models import User as AppUser, Scenario, LearningSession, InteractionLog, VocabularyCard

admin.site.site_header = "LinguistAI Native Admin"
admin.site.site_title = "LinguistAI Admin"
admin.site.index_title = "LinguistAI Database & Models Management"


@admin.register(AppUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role_badge', 'target_language', 'proficiency_level', 'subscription_badge', 'created_at')
    list_filter = ('role', 'subscription_plan', 'target_language', 'proficiency_level', 'created_at')
    search_fields = ('username', 'email', 'id')
    readonly_fields = ('id', 'created_at')
    ordering = ('-created_at',)

    def role_badge(self, obj):
        r = (obj.role or 'user').lower()
        if r == 'admin':
            return format_html('<span style="background:#6366f1; color:#fff; padding:3px 8px; border-radius:4px; font-weight:700; font-size:11px;">ADMIN</span>')
        return format_html('<span style="background:#475569; color:#fff; padding:3px 8px; border-radius:4px; font-size:11px;">LEARNER</span>')
    role_badge.short_description = 'Role'

    def subscription_badge(self, obj):
        plan = (obj.subscription_plan or 'Free').capitalize()
        color = '#10b981' if plan.lower() == 'pro' else '#6b7280'
        return format_html(
            '<span style="background:{}; color:#fff; padding:3px 8px; border-radius:4px; font-weight:600; font-size:11px;">{}</span>',
            color, plan
        )
    subscription_badge.short_description = 'Plan'


@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category_tag', 'cefr_tag', 'language_tag', 'video_url')
    search_fields = ('title', 'system_prompt')
    list_filter = ()
    ordering = ('id',)

    def _parse_prompt(self, obj):
        if not obj.system_prompt:
            return {}
        try:
            return json.loads(obj.system_prompt)
        except Exception:
            return {}

    def category_tag(self, obj):
        meta = self._parse_prompt(obj)
        cat = meta.get('category', 'General')
        return format_html('<span style="background:#e0e7ff; color:#3730a3; padding:2px 6px; border-radius:4px; font-size:11px;">{}</span>', cat)
    category_tag.short_description = 'Category'

    def cefr_tag(self, obj):
        meta = self._parse_prompt(obj)
        cefr = meta.get('cefr', 'All')
        return format_html('<span style="background:#fef3c7; color:#92400e; padding:2px 6px; border-radius:4px; font-size:11px;">{}</span>', cefr)
    cefr_tag.short_description = 'CEFR Level'

    def language_tag(self, obj):
        meta = self._parse_prompt(obj)
        lang = meta.get('lang', 'English')
        return format_html('<span style="background:#dcfce7; color:#166534; padding:2px 6px; border-radius:4px; font-size:11px;">{}</span>', lang)
    language_tag.short_description = 'Language'


@admin.register(LearningSession)
class LearningSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'scenario_id', 'overall_score_badge', 'started_at')
    list_filter = ('started_at',)
    search_fields = ('id', 'user_id')
    readonly_fields = ('id', 'started_at')
    ordering = ('-started_at',)

    def overall_score_badge(self, obj):
        if obj.overall_score is None:
            return "-"
        score = obj.overall_score
        color = '#10b981' if score >= 80 else ('#f59e0b' if score >= 60 else '#ef4444')
        return format_html(
            '<span style="background:{}; color:#fff; padding:3px 8px; border-radius:4px; font-weight:bold; font-size:11px;">{:.1f}%</span>',
            color, score
        )
    overall_score_badge.short_description = 'Score'


@admin.register(InteractionLog)
class InteractionLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'session_id', 'transcript_snippet', 'ai_response_snippet', 'created_at')
    search_fields = ('id', 'session_id', 'user_transcript', 'ai_response_text')
    readonly_fields = ('id', 'created_at', 'formatted_feedback')
    ordering = ('-created_at',)

    def transcript_snippet(self, obj):
        text = obj.user_transcript or ""
        return (text[:60] + '...') if len(text) > 60 else text
    transcript_snippet.short_description = 'User Transcript'

    def ai_response_snippet(self, obj):
        text = obj.ai_response_text or ""
        return (text[:60] + '...') if len(text) > 60 else text
    ai_response_snippet.short_description = 'AI Response'

    def formatted_feedback(self, obj):
        if not obj.detailed_feedback:
            return "No feedback recorded"
        try:
            formatted = json.dumps(obj.detailed_feedback, indent=2)
            return format_html('<pre style="background:#1e293b; color:#f8fafc; padding:10px; border-radius:6px; max-height:300px; overflow:auto;">{}</pre>', formatted)
        except Exception:
            return str(obj.detailed_feedback)
    formatted_feedback.short_description = 'Detailed Feedback JSON'


@admin.register(VocabularyCard)
class VocabularyCardAdmin(admin.ModelAdmin):
    list_display = ('word', 'translation', 'language', 'user_id', 'repetitions', 'interval', 'ease_factor', 'next_review')
    list_filter = ('language', 'created_at')
    search_fields = ('word', 'translation', 'user_id')
    readonly_fields = ('id', 'created_at')
    ordering = ('-created_at',)


admin.site.site_header = "LinguistAI Admin Portal"
admin.site.site_title = "LinguistAI Admin"
admin.site.index_title = "LinguistAI Platform Administration"
