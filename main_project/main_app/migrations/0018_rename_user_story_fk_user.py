# Generated by Django 5.0.1 on 2024-03-18 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0017_story'),
    ]

    operations = [
        migrations.RenameField(
            model_name='story',
            old_name='User',
            new_name='fk_user',
        ),
    ]
