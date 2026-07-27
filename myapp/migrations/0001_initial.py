from django.db import migrations, models
import uuid

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('password_hash', models.CharField(blank=True, max_length=255, null=True)),
                ('target_language', models.CharField(blank=True, max_length=255, null=True)),
                ('proficiency_level', models.CharField(blank=True, max_length=255, null=True)),
                ('subscription_plan', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Scenario',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('system_prompt', models.TextField(blank=True, null=True)),
                ('video_url', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'verbose_name': 'Scenario',
                'verbose_name_plural': 'Scenarios',
                'db_table': 'scenarios',
            },
        ),
        migrations.CreateModel(
            name='LearningSession',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user_id', models.UUIDField()),
                ('scenario_id', models.IntegerField()),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('overall_score', models.FloatField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Learning Session',
                'verbose_name_plural': 'Learning Sessions',
                'db_table': 'learning_sessions',
            },
        ),
        migrations.CreateModel(
            name='InteractionLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('session_id', models.UUIDField()),
                ('user_audio_url', models.CharField(blank=True, max_length=500, null=True)),
                ('user_transcript', models.TextField(blank=True, null=True)),
                ('ai_audio_url', models.CharField(blank=True, max_length=500, null=True)),
                ('ai_response_text', models.TextField(blank=True, null=True)),
                ('detailed_feedback', models.JSONField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Interaction Log',
                'verbose_name_plural': 'Interaction Logs',
                'db_table': 'interaction_logs',
            },
        ),
    ]