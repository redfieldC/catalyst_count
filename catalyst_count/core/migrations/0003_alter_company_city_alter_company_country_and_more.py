# Generated by Django 5.0.6 on 2024-05-23 10:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_remove_company_locality_company_city_company_state"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="city",
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name="company",
            name="country",
            field=models.CharField(default="Unknown", max_length=250),
        ),
        migrations.AlterField(
            model_name="company",
            name="size_range",
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name="company",
            name="state",
            field=models.CharField(max_length=250),
        ),
    ]
