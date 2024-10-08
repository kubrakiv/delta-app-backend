# Generated by Django 4.2.6 on 2023-12-30 23:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("profile", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="role",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="profiles",
                to="profile.role",
            ),
        ),
    ]
