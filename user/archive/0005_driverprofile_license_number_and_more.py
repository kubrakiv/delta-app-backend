# Generated by Django 4.2.6 on 2024-05-05 19:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profile", "0004_driverprofile_birth_date_driverprofile_country_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="driverprofile",
            name="license_number",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="driverprofile",
            name="license_series",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
