# Generated by Django 4.2.13 on 2024-06-12 05:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Workspace',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(blank=True, db_index=True, editable=False, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, editable=False, null=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkspacesMembership',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(blank=True, db_index=True, editable=False, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, editable=False, null=True)),
                ('access_level', models.CharField(choices=[('owner', 'Owner'), ('member', 'Member')], default='member')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workspace_membership', to=settings.AUTH_USER_MODEL)),
                ('workspace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membership', to='workspaces.workspace')),
            ],
            options={
                'unique_together': {('workspace', 'member')},
            },
        ),
        migrations.AddField(
            model_name='workspace',
            name='member',
            field=models.ManyToManyField(related_name='membered_workspace', through='workspaces.WorkspacesMembership', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='workspace',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workspaces', to=settings.AUTH_USER_MODEL),
        ),
    ]
