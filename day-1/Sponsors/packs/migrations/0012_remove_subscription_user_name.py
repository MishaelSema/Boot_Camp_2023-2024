# Generated by Django 5.0.6 on 2024-06-05 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('packs', '0011_subscription_user_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='user_name',
        ),
    ]
