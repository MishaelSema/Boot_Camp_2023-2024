# Generated by Django 5.0.6 on 2024-06-07 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packs', '0016_alter_subscription_pack'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='amount_per_month',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
