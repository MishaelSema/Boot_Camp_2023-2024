# Generated by Django 5.0.6 on 2024-06-07 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('packs', '0013_subscription_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='items',
        ),
    ]