# Generated by Django 4.2.13 on 2024-06-23 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0002_alter_workspacesmembership_access_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workspace',
            name='is_deleted',
            field=models.BooleanField(db_index=True, default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='workspacesmembership',
            name='is_deleted',
            field=models.BooleanField(db_index=True, default=False, editable=False),
        ),
    ]
