# Generated by Django 4.2.13 on 2024-07-30 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_alter_board_is_deleted_alter_comment_is_deleted_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='labels',
        ),
    ]