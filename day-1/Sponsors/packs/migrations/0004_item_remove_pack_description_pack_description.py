# Generated by Django 5.0.6 on 2024-06-04 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packs', '0003_remove_pack_tariff_pack_amount_per_month'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='pack',
            name='description',
        ),
        migrations.AddField(
            model_name='pack',
            name='description',
            field=models.ManyToManyField(to='packs.item'),
        ),
    ]
