# Generated by Django 5.0.6 on 2024-05-23 09:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="company",
            name="locality",
        ),
        migrations.AddField(
            model_name="company",
            name="city",
            field=models.CharField(default="UNKNOWN", max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="company",
            name="state",
            field=models.CharField(default="UNKNOWN", max_length=20),
            preserve_default=False,
        ),
    ]