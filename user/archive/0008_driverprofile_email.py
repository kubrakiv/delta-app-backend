# Generated by Django 4.2.6 on 2024-05-08 22:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profile", "0007_driverprofile_middle_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="driverprofile",
            name="email",
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
    ]